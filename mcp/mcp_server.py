# mcp/mcp_server.py - Self-Learning MCP Server
from flask import Flask, request, jsonify
import subprocess
import os
import sys
import json
from datetime import datetime

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Add parent directory for utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Dynamic imports - will be loaded dynamically
from dynamic_loader import tool_loader
from tool_generator import tool_generator

# Import self-learning controller
from self_learning.self_learning_controller import SelfLearningController

def calculate_confidence(user_input):
    """
    Three-stage confidence calculation:
    [1] Clarity Score (0-50%): How well is the command phrased?
    [2] ROM Match (0-40%): Have we seen this before in existing tools?
    [3] GPT Boost (0-40%): Can GPT clarify unclear commands?
    """
    import difflib
    import re
    
    # [1] CLARITY SCORE (0-50%): Command structure and clarity
    clarity_score = calculate_clarity_score(user_input)
    
    # [2] ROM MATCH (0-40%): Similarity to existing capabilities
    rom_score = calculate_rom_match_score(user_input)
    
    initial_confidence = clarity_score + rom_score
    
    return {
        "clarity_score": clarity_score,
        "rom_score": rom_score,
        "initial_confidence": initial_confidence,
        "needs_gpt_boost": initial_confidence < 90
    }

def calculate_clarity_score(user_input):
    """Calculate how clearly the command is phrased (0-50%)"""
    score = 0
    user_lower = user_input.lower().strip()
    
    # Length appropriateness (0-15%)
    if 3 <= len(user_input.split()) <= 8:
        score += 15  # Good length
    elif len(user_input.split()) <= 2:
        score += 5   # Too short
    elif len(user_input.split()) > 15:
        score += 5   # Too long
    else:
        score += 10  # Acceptable
    
    # Action word presence (0-20%)
    action_words = ['open', 'close', 'create', 'delete', 'make', 'set', 'get', 'show', 'play', 'stop', 
                   'send', 'turn', 'increase', 'decrease', 'enable', 'disable', 'start', 'take']
    for word in action_words:
        if word in user_lower:
            score += 20
            break
    else:
        score += 5  # No clear action word
    
    # Object/target presence (0-10%)
    target_words = ['volume', 'brightness', 'photo', 'folder', 'file', 'music', 'email', 'notification',
                   'bluetooth', 'wifi', 'app', 'browser', 'weather', 'calendar', 'screenshot']
    for word in target_words:
        if word in user_lower:
            score += 10
            break
    else:
        score += 3  # No clear target
    
    # Grammar/coherence (0-5%)
    if any(word in user_lower for word in ['please', 'can you', 'could you']):
        score += 5  # Polite phrasing
    elif user_lower.endswith('?'):
        score += 3  # Question format
    else:
        score += 2  # Command format
    
    return min(score, 50)  # Cap at 50%

def calculate_rom_match_score(user_input):
    """Calculate similarity to existing ROM/capabilities (0-40%)"""
    import difflib
    import os
    import json
    import re
    
    user_lower = user_input.lower()
    max_score = 0
    
    # Check ROM file for learned patterns
    try:
        rom_file = '/Users/mahendrabahubali/chotu/memory/rom.json'
        if os.path.exists(rom_file):
            with open(rom_file, 'r') as f:
                rom_entries = json.load(f)
            
            for entry in rom_entries:
                # Check YouTube automation patterns
                if entry.get('learning_category') == 'web_automation_youtube':
                    command_patterns = entry.get('command_patterns', [])
                    for pattern in command_patterns:
                        # Convert pattern to regex and check match
                        pattern_regex = pattern.replace('*', '.*').lower()
                        if re.search(pattern_regex, user_lower):
                            print(f"🎯 ROM Match: '{pattern}' matches '{user_input}'")
                            max_score = max(max_score, 38)  # High score for exact pattern match
                        elif any(word in user_lower for word in pattern.lower().split() if word not in ['*', 'on', 'and', 'the']):
                            # Partial keyword match
                            max_score = max(max_score, 25)
                
                # Check other automation patterns
                if 'command_patterns' in entry:
                    patterns = entry.get('command_patterns', [])
                    for pattern in patterns:
                        similarity = difflib.SequenceMatcher(None, user_lower, pattern.lower()).ratio()
                        if similarity > 0.6:
                            max_score = max(max_score, int(similarity * 35))
    except Exception as e:
        print(f"⚠️ Could not check ROM: {e}")
    
    # Check web learnings for site patterns
    try:
        web_learnings_file = '/Users/mahendrabahubali/chotu/memory/web_learnings.json'
        if os.path.exists(web_learnings_file):
            with open(web_learnings_file, 'r') as f:
                web_learnings = json.load(f)
            
            site_patterns = web_learnings.get('site_patterns', {})
            for site, data in site_patterns.items():
                if data.get('automation_available'):
                    patterns = data.get('command_patterns', [])
                    for pattern in patterns:
                        pattern_regex = pattern.replace('*', '.*').lower()
                        if re.search(pattern_regex, user_lower):
                            print(f"🌐 Web Learning Match: '{pattern}' for {site}")
                            max_score = max(max_score, 35)
    except Exception as e:
        print(f"⚠️ Could not check web learnings: {e}")
    
    # Fallback: Check tool capabilities
    if max_score == 0:
        capabilities = tool_loader.get_all_capabilities()
        
        # Build patterns from existing tools
        patterns = []
        for tool_name, functions in capabilities.items():
            # Add tool names
            patterns.append(tool_name.replace('_', ' '))
            # Add function names
            for func_name in functions:
                if func_name not in ['datetime', 'timedelta', 'subprocess', 'os', 'json']:
                    patterns.append(func_name.replace('_', ' '))
        
        if patterns:
            # Find best match
            pattern_lower = [p.lower() for p in patterns]
            matches = difflib.get_close_matches(user_lower, pattern_lower, n=1, cutoff=0.3)
            
            if matches:
                similarity = difflib.SequenceMatcher(None, user_lower, matches[0]).ratio()
                max_score = max(max_score, int(similarity * 40))  # Scale to 0-40%
            
            # Check for keyword overlap
            user_words = set(user_lower.split())
            for pattern in pattern_lower:
                pattern_words = set(pattern.split())
                overlap = len(user_words.intersection(pattern_words))
                if overlap > 0:
                    overlap_ratio = overlap / max(len(user_words), len(pattern_words))
                    max_score = max(max_score, int(overlap_ratio * 25))  # Partial match score
    
    return min(max_score, 40)  # Cap at 40%

def gpt_boost_understanding(user_input, initial_confidence):
    """Use GPT to boost understanding for unclear commands (0-40%)"""
    if initial_confidence >= 90:
        return 0, user_input, True  # No boost needed, clear command
    
    try:
        from tools.gpt_planner import call_gpt_context
        
        prompt = f"""
Analyze this user command and determine if it's a valid request:
Command: "{user_input}"

If it's a valid request, respond with ONLY the clarified intent in simple action words.
If it's unclear, nonsensical, or not a real command, respond with "UNCLEAR"

Examples:
"uh turn on" → "enable bluetooth"
"make dir Projects" → "create folder Projects"
"show me weather" → "get weather information"
"xyz" → "UNCLEAR"
"blahblah" → "UNCLEAR"
"asdfgh" → "UNCLEAR"

Clarified intent:"""
        
        clarified_intent = call_gpt_context(prompt).strip().strip('"')
        
        # Check if GPT determined command is unclear
        if clarified_intent.upper() == "UNCLEAR" or "unclear" in clarified_intent.lower():
            return 0, user_input, False  # No boost, command is unclear
        
        # Calculate boost based on clarification quality
        if len(clarified_intent) > 0 and clarified_intent != user_input:
            # Good clarification
            boost = 30
            if any(word in clarified_intent.lower() for word in ['set', 'get', 'create', 'open', 'enable']):
                boost = 40  # Excellent clarification with clear action
            return boost, clarified_intent, True
        else:
            return 10, user_input, True  # Minimal boost but still valid
            
    except Exception as e:
        print(f"❌ GPT boost failed: {e}")
        return 0, user_input, True  # Default to valid if GPT fails

# Initialize dynamic tool loading
tool_loader.load_all_tools()

# Initialize self-learning controller
self_learning_controller = SelfLearningController()

app = Flask(__name__)

# Task queue for failed requests
pending_tasks = []

@app.route('/execute', methods=['POST'])
def execute_task():
    """Self-learning task execution"""
    ram = request.json
    
    # Extract intent from multiple possible fields with priority
    intent = (
        ram.get("interpreted_intent", "") or 
        ram.get("intent", "") or 
        ram.get("raw_input", "")
    ).lower().strip()
    
    nlp_analysis = ram.get("nlp_analysis", {})
    original_request = ram.get("raw_input", intent) or intent
    
    print(f"🎯 MCP received request:")
    print(f"   Intent: '{intent}'")
    print(f"   Original: '{original_request}'")
    print(f"   NLP: {nlp_analysis}")
    
    try:
        # First, try to execute with existing capabilities using the best available intent
        best_intent = original_request if original_request else intent
        result = try_existing_capabilities(best_intent, nlp_analysis)
        
        if result and not result.startswith("❌") and result != "Unknown command":
            # Success with existing capabilities
            return jsonify({
                "output": result,
                "intent_processed": best_intent,
                "nlp_analysis": nlp_analysis.get('intent', 'unknown'),
                "timestamp": datetime.now().isoformat(),
                "success": True,
                "learned": False
            })
        
        # Failed with existing capabilities - use three-stage confidence system
        confidence_data = calculate_confidence(original_request)
        clarity = confidence_data["clarity_score"]
        rom_match = confidence_data["rom_score"] 
        initial_confidence = confidence_data["initial_confidence"]
        
        print(f"🤔 Unknown command detected: {original_request}")
        print(f"📊 Clarity: {clarity}% | ROM Match: {rom_match}% | Initial: {initial_confidence}%")
        
        # Stage 1: Check if we have high confidence AND existing capability
        if initial_confidence >= 90:
            print("✅ High initial confidence - checking existing capabilities")
            result = try_existing_capabilities(original_request, nlp_analysis)
            if result and not result.startswith("❌") and result != "Unknown command":
                return jsonify({
                    "output": result,
                    "intent_processed": original_request,
                    "timestamp": datetime.now().isoformat(),
                    "success": True,
                    "learned": False,
                    "confidence_breakdown": confidence_data
                })
        
        # Stage 2: Use GPT to boost understanding for unclear commands
        gpt_boost = 0
        clarified_intent = original_request
        is_valid_command = True
        
        if initial_confidence < 90:
            print("🔄 Using GPT to boost understanding...")
            gpt_boost, clarified_intent, is_valid_command = gpt_boost_understanding(original_request, initial_confidence)
            print(f"🧠 GPT Boost: +{gpt_boost}% | Clarified: '{clarified_intent}' | Valid: {is_valid_command}")
        
        final_confidence = initial_confidence + gpt_boost
        print(f"📈 Final Confidence: {final_confidence}%")
        
        # Check if GPT determined the command is unclear/invalid
        if not is_valid_command:
            return jsonify({
                "output": "❓ That command doesn't seem clear or valid. Can you rephrase what you'd like me to do?",
                "intent_processed": original_request,
                "timestamp": datetime.now().isoformat(),
                "success": False,
                "learned": False,
                "confidence_breakdown": {
                    **confidence_data,
                    "gpt_boost": gpt_boost,
                    "final_confidence": final_confidence,
                    "gpt_validation": "UNCLEAR"
                },
                "request_clarification": True
            })
        
        # Stage 3: Decision making based on final confidence
        if final_confidence < 30:
            # Very low confidence - ask user to rephrase
            return jsonify({
                "output": "❓ I didn't understand that clearly. Can you rephrase your request?",
                "intent_processed": original_request,
                "timestamp": datetime.now().isoformat(),
                "success": False,
                "learned": False,
                "confidence_breakdown": {
                    **confidence_data,
                    "gpt_boost": gpt_boost,
                    "final_confidence": final_confidence
                },
                "request_clarification": True
            })
            
        elif 30 <= final_confidence < 90:
            # Medium confidence - try existing capabilities, then learn if needed
            print(f"� Medium confidence ({final_confidence}%) - checking capabilities then learning")
            
            # Try with clarified intent
            result = try_existing_capabilities(clarified_intent, nlp_analysis)
            if result and not result.startswith("❌") and result != "Unknown command":
                return jsonify({
                    "output": result,
                    "intent_processed": clarified_intent,
                    "timestamp": datetime.now().isoformat(),
                    "success": True,
                    "learned": False,
                    "confidence_breakdown": {
                        **confidence_data,
                        "gpt_boost": gpt_boost,
                        "final_confidence": final_confidence
                    }
                })
            
            # No existing capability - trigger AUTONOMOUS learning
            print("🧠 No existing capability found - triggering AUTONOMOUS learning mode")
            current_capabilities = tool_loader.get_all_capabilities()
            
            # Enhanced learning with self-learning controller
            learning_context = {
                "failed_command": clarified_intent,
                "user_feedback": original_request,
                "confidence_data": confidence_data,
                "existing_capabilities": current_capabilities,
                "nlp_analysis": nlp_analysis,
                "error_context": "Command not found in existing capabilities"
            }
            
            # Use autonomous self-learning controller
            autonomous_result = self_learning_controller.handle_new_request(
                clarified_intent, 
                learning_context
            )
            
            if autonomous_result.get("status") == "success":
                print("🎯 Autonomous learning succeeded - reloading and retrying")
                tool_loader.load_all_tools()
                retry_result = try_existing_capabilities(clarified_intent, nlp_analysis)
                
                if retry_result and not retry_result.startswith("❌") and retry_result != "Unknown command":
                    return jsonify({
                        "output": f"🧠 I learned something new with autonomous AI! {retry_result}",
                        "intent_processed": clarified_intent,
                        "timestamp": datetime.now().isoformat(),
                        "success": True,
                        "learned": True,
                        "learning_type": "autonomous",
                        "learning_details": autonomous_result,
                        "confidence_breakdown": {
                            **confidence_data,
                            "gpt_boost": gpt_boost,
                            "final_confidence": final_confidence
                        }
                    })
            
            # Fallback to intelligent learning if autonomous learning didn't work completely
            if tool_generator.intelligent_learn(learning_context):
                print("🎯 Intelligent learning succeeded - reloading and retrying")
                tool_loader.load_all_tools()
                retry_result = try_existing_capabilities(clarified_intent, nlp_analysis)
                
                if retry_result and not retry_result.startswith("❌") and retry_result != "Unknown command":
                    return jsonify({
                        "output": f"🧠 I learned something new! {retry_result}",
                        "intent_processed": clarified_intent,
                        "timestamp": datetime.now().isoformat(),
                        "success": True,
                        "learned": True,
                        "learning_type": "intelligent",
                        "confidence_breakdown": {
                            **confidence_data,
                            "gpt_boost": gpt_boost,
                            "final_confidence": final_confidence
                        }
                    })
                else:
                    print("🔄 First learning attempt didn't work - trying adaptive learning")
                    # Fallback to adaptive learning if intelligent learning didn't work
                    if tool_generator.adaptive_learn_from_failure(learning_context, retry_result):
                        tool_loader.load_all_tools()
                        final_result = try_existing_capabilities(clarified_intent, nlp_analysis)
                        if final_result and not final_result.startswith("❌") and final_result != "Unknown command":
                            return jsonify({
                                "output": f"🎯 I figured it out through adaptive learning! {final_result}",
                                "intent_processed": clarified_intent,
                                "timestamp": datetime.now().isoformat(),
                                "success": True,
                                "learned": True,
                                "learning_type": "adaptive",
                                "confidence_breakdown": {
                                    **confidence_data,
                                    "gpt_boost": gpt_boost,
                                    "final_confidence": final_confidence
                                }
                            })
            
            # If intelligent learning fails, fall back to basic learning
            print("🔧 Intelligent learning failed - falling back to basic learning")
            if tool_generator.learn_new_capability(clarified_intent, current_capabilities):
                tool_loader.load_all_tools()
                retry_result = try_existing_capabilities(clarified_intent, nlp_analysis)
                
                if retry_result and not retry_result.startswith("❌"):
                    return jsonify({
                        "output": f"🧠 Learned new capability! {retry_result}",
                        "intent_processed": clarified_intent,
                        "timestamp": datetime.now().isoformat(),
                        "success": True,
                        "learned": True,
                        "new_capability": True,
                        "learning_type": "basic",
                        "confidence_breakdown": {
                            **confidence_data,
                            "gpt_boost": gpt_boost,
                            "final_confidence": final_confidence
                        }
                    })
            
            # Learning failed - fallback
            try:
                from tools.gpt_planner import generate_and_run
                fallback_result = generate_and_run(clarified_intent)
            except:
                fallback_result = f"Learning failed for: {clarified_intent}"
            
            return jsonify({
                "output": f"🤖 Learning Failed - GPT Fallback: {fallback_result}",
                "intent_processed": clarified_intent,
                "timestamp": datetime.now().isoformat(),
                "success": True,
                "learned": False,
                "learning_attempted": True,
                "confidence_breakdown": {
                    **confidence_data,
                    "gpt_boost": gpt_boost,
                    "final_confidence": final_confidence
                }
            })
            
        else:  # final_confidence >= 90
            # High confidence - execute immediately
            print(f"✅ High confidence ({final_confidence}%) - executing immediately")
            result = try_existing_capabilities(clarified_intent, nlp_analysis)
            
            # Be honest about unknown commands - don't give false success
            if result == "Unknown command":
                print(f"❌ No handler found for: {clarified_intent}")
                return jsonify({
                    "output": f"❌ I don't know how to handle '{clarified_intent}' yet. Let me try to learn this capability.",
                    "intent_processed": clarified_intent,
                    "timestamp": datetime.now().isoformat(),
                    "success": False,
                    "learned": False,
                    "needs_learning": True,
                    "confidence_breakdown": {
                        **confidence_data,
                        "gpt_boost": gpt_boost,
                        "final_confidence": final_confidence
                    }
                })
            
            return jsonify({
                "output": result,
                "intent_processed": clarified_intent,
                "timestamp": datetime.now().isoformat(),
                "success": True,
                "learned": False,
                "confidence_breakdown": {
                    **confidence_data,
                    "gpt_boost": gpt_boost,
                    "final_confidence": final_confidence
                }
            })
        
    except Exception as e:
        error_msg = f"Execution failed: {str(e)}"
        return jsonify({
            "output": error_msg,
            "intent_processed": intent,
            "success": False,
            "error": str(e)
        }), 500

def try_existing_capabilities(intent, nlp_analysis):
    """Try to execute with existing capabilities"""
    try:
        # YouTube Automation - Check memory first (more specific matching)
        if any(keyword in intent.lower() for keyword in ["youtube", "video", "play", "music", "song"]) or \
           ("youtube" in intent.lower() and "search" in intent.lower()) or \
           ("play" in intent.lower() and any(media in intent.lower() for media in ["music", "song", "video"])):
            return handle_youtube_automation_command(intent)
        
        # Web Browser + Search Commands (Chrome, Safari, Firefox + search query)
        elif (any(browser in intent.lower() for browser in ["chrome", "safari", "firefox"]) and 
              "search" in intent.lower() and 
              not any(media in intent.lower() for media in ["youtube", "video", "music", "song"])):
            return handle_web_browser_search_command(intent)
        
        # Context-aware follow-up commands
        elif any(phrase in intent.lower() for phrase in ["first link", "top result", "click first", "open first"]):
            return handle_contextual_followup_command(intent)
        
        # System Control
        if "volume" in intent.lower():
            return handle_volume_command(intent)
        elif "brightness" in intent.lower():
            return handle_brightness_command(intent)
        elif "bluetooth" in intent.lower():
            return handle_bluetooth_command(intent)
        
        # Productivity Commands
        elif "screenshot" in intent.lower() or "capture screen" in intent.lower():
            return handle_screenshot_command(intent)
        elif "system info" in intent.lower() or "system information" in intent.lower():
            return handle_system_info_command(intent)
        elif "battery" in intent.lower():
            return handle_battery_command(intent)
        
        # Application Commands  
        elif any(word in intent.lower() for word in ["open", "launch", "start"]) and any(app in intent.lower() for app in ["safari", "chrome", "firefox", "app"]):
            return handle_app_command(intent)
        
        # Context-aware system control - check for percentage commands that might refer to recent system controls
        import re
        percentage_match = re.search(r'(\d+)%?', intent)
        if percentage_match and any(word in intent.lower() for word in ['set', 'adjust', 'change']):
            # This might be a follow-up command referring to a recent system control
            # For now, assume brightness context (most common use case)
            level = int(percentage_match.group(1))
            print(f"🔧 Context-aware: interpreting '{intent}' as brightness command with level {level}%")
            return handle_brightness_command(f"set brightness to {level}%")
        
        # Check dynamic tools
        capabilities = tool_loader.get_all_capabilities()
        
        # Specific capability matching
        if "create" in intent and ("folder" in intent or "directory" in intent):
            if "folder_operations" in capabilities:
                func = tool_loader.get_tool_function("folder_operations", "create_folder")
                if func:
                    try:
                        # Extract folder name from intent
                        import re
                        folder_match = re.search(r'(?:folder|directory)\s+(?:called|named)?\s*([a-zA-Z0-9_-]+)', intent)
                        if folder_match:
                            folder_name = folder_match.group(1)
                        else:
                            folder_name = "NewFolder"
                        
                        result = func(folder_name)
                        return f"✅ {result}"
                    except Exception as e:
                        return f"❌ Folder creation failed: {e}"
        
        # Try to find matching function by pattern
        matches = tool_loader.find_function_by_pattern(intent)
        if matches:
            tool_name, func_name = matches[0]
            func = tool_loader.get_tool_function(tool_name, func_name)
            if func:
                try:
                    result = func()
                    return f"✅ {result}"
                except Exception as e:
                    return f"❌ Tool execution failed: {e}"
        
        # Application control using enhanced apps module
        if "open" in intent or "launch" in intent or "start" in intent:
            # Try our enhanced app opening function
            if "apps" in capabilities:
                func = tool_loader.get_tool_function("apps", "open_app")
                if func:
                    try:
                        # Extract app name from intent
                        import re
                        # Remove action words to get app name
                        app_name = intent.lower()
                        for action in ['open', 'launch', 'start', 'the', 'browser']:
                            app_name = app_name.replace(action, '').strip()
                        
                        if app_name:
                            result = func(app_name)
                            return result
                    except Exception as e:
                        return f"❌ App opening failed: {e}"
            
        # File operations
        if "folder" in intent or "directory" in intent:
            if "create" in intent or "make" in intent:
                return "❌ Create folder capability not implemented yet"
        
        return "Unknown command"
        
    except Exception as e:
        return f"❌ Error in existing capabilities: {e}"

def handle_volume_command(intent):
    """Handle volume-related commands"""
    try:
        from tools.system import set_volume
        import re
        
        volume_match = re.search(r'(\d+)%?', intent)
        if volume_match:
            level = int(volume_match.group(1))
            return set_volume(level)
        elif "up" in intent or "increase" in intent:
            return set_volume(80)
        elif "down" in intent or "decrease" in intent:
            return set_volume(30)
        elif "mute" in intent:
            return set_volume(0)
        else:
            return "Volume command unclear"
    except Exception as e:
        return f"❌ Volume error: {e}"

def handle_brightness_command(intent):
    """Handle brightness-related commands"""
    try:
        from tools.system import set_brightness, increase_brightness, decrease_brightness
        import re
        
        # First priority: Check for specific brightness level (number)
        brightness_match = re.search(r'(\d+)%?', intent)
        if brightness_match:
            level = int(brightness_match.group(1))
            print(f"🔧 Found brightness level: {level}% in command: '{intent}'")
            return set_brightness(level)
        
        # Second priority: Generic increase/decrease without specific level
        if "up" in intent or "increase" in intent:
            print(f"🔧 Generic brightness increase for command: '{intent}'")
            return increase_brightness()
        elif "down" in intent or "decrease" in intent:
            print(f"🔧 Generic brightness decrease for command: '{intent}'")
            return decrease_brightness()
        else:
            print(f"🔧 Default brightness increase for unclear command: '{intent}'")
            return increase_brightness()
    except Exception as e:
        return f"❌ Brightness error: {e}"

def handle_bluetooth_command(intent):
    """Handle Bluetooth-related commands - INCLUDING device listing"""
    try:
        from tools.system import enable_bluetooth, disable_bluetooth, toggle_bluetooth
        
        # Check for device listing commands - handle them directly
        device_keywords = ['devices', 'list', 'show', 'get', 'find', 'paired', 'connected', 'scan', 'search']
        if any(keyword in intent.lower() for keyword in device_keywords):
            print(f"� Device listing command detected: '{intent}' - calling list_bluetooth_devices()")
            return list_bluetooth_devices()
        
        # Handle enable/disable/toggle commands (clean punctuation first)
        clean_intent = intent.lower().strip().rstrip('.').rstrip('!')
        if any(word in clean_intent for word in ["disable", "turn off", "off"]):
            return disable_bluetooth()
        elif any(word in clean_intent for word in ["enable", "turn on", "on"]):
            return enable_bluetooth()
        elif "toggle" in clean_intent or clean_intent.strip() == "bluetooth":
            return toggle_bluetooth()
        else:
            # Any other bluetooth command should go to learning
            print(f"🔄 Unknown bluetooth command: '{intent}' - passing to learning system")
            return "Unknown command"
    except Exception as e:
        return f"❌ Bluetooth error: {e}"

def list_bluetooth_devices():
    """List paired and connected Bluetooth devices using blueutil"""
    try:
        import subprocess
        
        # Get paired devices
        paired_result = subprocess.run(['blueutil', '--paired'], capture_output=True, text=True)
        connected_result = subprocess.run(['blueutil', '--connected'], capture_output=True, text=True)
        
        if paired_result.returncode != 0:
            return "❌ Failed to get Bluetooth device list. Make sure blueutil is installed: brew install blueutil"
        
        paired_devices = paired_result.stdout.strip()
        connected_devices = connected_result.stdout.strip()
        
        response = "📱 Bluetooth Devices:\n"
        
        if connected_devices:
            response += f"🟢 Connected:\n{connected_devices}\n\n"
        else:
            response += "🟢 Connected: None\n\n"
            
        if paired_devices:
            response += f"🔗 Paired:\n{paired_devices}"
        else:
            response += "🔗 Paired: None"
            
        return response
        
    except Exception as e:
        return f"❌ Error listing Bluetooth devices: {e}"

def handle_screenshot_command(intent):
    """Handle screenshot-related commands"""
    try:
        # Try productivity tool first
        capabilities = tool_loader.get_all_capabilities()
        if "productivity" in capabilities:
            func = tool_loader.get_tool_function("productivity", "take_screenshot")
            if func:
                return func()
        
        # Fallback to system command
        import subprocess
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        result = subprocess.run(['screencapture', '-x', filename], capture_output=True)
        if result.returncode == 0:
            return f"✅ Screenshot saved as {filename}"
        else:
            return "❌ Failed to take screenshot"
    except Exception as e:
        return f"❌ Screenshot error: {e}"

def handle_system_info_command(intent):
    """Handle system info commands"""
    try:
        # Try productivity tool first
        capabilities = tool_loader.get_all_capabilities()
        if "productivity" in capabilities:
            func = tool_loader.get_tool_function("productivity", "get_system_info")
            if func:
                return func()
        
        # Fallback to basic system info
        import subprocess
        import platform
        
        info = []
        info.append(f"💻 System: {platform.system()} {platform.release()}")
        info.append(f"🏗️ Machine: {platform.machine()}")
        info.append(f"🐍 Python: {platform.python_version()}")
        
        # Try to get macOS version
        try:
            result = subprocess.run(['sw_vers', '-productVersion'], capture_output=True, text=True)
            if result.returncode == 0:
                info.append(f"🍎 macOS: {result.stdout.strip()}")
        except:
            pass
            
        return "✅ System Information:\n" + "\n".join(info)
    except Exception as e:
        return f"❌ System info error: {e}"

def handle_battery_command(intent):
    """Handle battery-related commands"""
    try:
        # Try battery_monitor tool first
        capabilities = tool_loader.get_all_capabilities()
        if "battery_monitor" in capabilities:
            func = tool_loader.get_tool_function("battery_monitor", "get_battery_status")
            if func:
                return func()
        
        # Fallback to system command
        import subprocess
        result = subprocess.run(['pmset', '-g', 'batt'], capture_output=True, text=True)
        if result.returncode == 0:
            output = result.stdout
            if "%" in output:
                # Extract battery percentage
                for line in output.split('\n'):
                    if '%' in line:
                        return f"🔋 Battery Status: {line.strip()}"
            return f"🔋 Battery Status:\n{output.strip()}"
        else:
            return "❌ Could not get battery status"
    except Exception as e:
        return f"❌ Battery error: {e}"

def handle_app_command(intent):
    """Handle app opening commands"""
    try:
        import re
        
        # Extract app name with better patterns
        app_patterns = [
            r'open\s+([a-zA-Z0-9\s]+?)(?:\s+and|$)',  # "open Chrome and..." -> "Chrome"
            r'launch\s+([a-zA-Z0-9\s]+?)(?:\s+and|$)', 
            r'start\s+([a-zA-Z0-9\s]+?)(?:\s+and|$)'
        ]
        
        app_name = None
        for pattern in app_patterns:
            match = re.search(pattern, intent, re.IGNORECASE)
            if match:
                app_name = match.group(1).strip()
                break
        
        # If no pattern matched, try simple extraction
        if not app_name:
            words = intent.lower().split()
            if 'open' in words:
                idx = words.index('open')
                if idx + 1 < len(words):
                    app_name = words[idx + 1]
            elif 'launch' in words:
                idx = words.index('launch')
                if idx + 1 < len(words):
                    app_name = words[idx + 1]
        
        if not app_name:
            return "❌ Could not identify app name"
        
        # Clean up app name
        app_name = app_name.strip()
        
        print(f"🎯 Extracted app name: '{app_name}' from intent: '{intent}'")
        
        # Try open_application tool
        capabilities = tool_loader.get_all_capabilities()
        if "open_application" in capabilities:
            func = tool_loader.get_tool_function("open_application", "open_application")
            if func:
                return func(app_name)
        
        # Fallback to system command
        import subprocess
        result = subprocess.run(['open', '-a', app_name], capture_output=True, text=True)
        if result.returncode == 0:
            return f"✅ Opened {app_name}"
        else:
            return f"❌ Failed to open {app_name}: {result.stderr}"
    except Exception as e:
        return f"❌ App opening error: {e}"

def handle_web_browser_search_command(intent):
    """Handle web browser search commands like 'open Chrome and search Amazon'"""
    try:
        import re
        import subprocess
        import urllib.parse
        import time
        
        print(f"🌐 Web browser search triggered for: '{intent}'")
        
        # Store last search context for follow-up commands
        global last_search_context
        if 'last_search_context' not in globals():
            last_search_context = {}
        
        # Extract browser name
        browser_map = {
            'chrome': 'Google Chrome',
            'safari': 'Safari', 
            'firefox': 'Firefox'
        }
        
        browser = None
        intent_lower = intent.lower()
        for browser_key, browser_name in browser_map.items():
            if browser_key in intent_lower:
                browser = browser_name
                break
        
        if not browser:
            browser = 'Google Chrome'  # Default
        
        # Extract search query
        search_patterns = [
            r'search\s+(.+?)(?:\s+on|\s+in|\s+with|$)',  # "search Amazon on..."
            r'(?:open|launch)\s+\w+\s+and\s+search\s+(.+)',  # "open Chrome and search Amazon"
            r'(?:google|search\s+for)\s+(.+)',  # "google Amazon"
        ]
        
        search_query = None
        for pattern in search_patterns:
            match = re.search(pattern, intent_lower)
            if match:
                search_query = match.group(1).strip()
                break
        
        if not search_query:
            # Extract everything after "search"
            if "search" in intent_lower:
                parts = intent_lower.split("search", 1)
                if len(parts) > 1:
                    search_query = parts[1].strip()
                    # Clean up common words
                    search_query = re.sub(r'^(for|on|in|with)\s+', '', search_query)
        
        if not search_query:
            return f"❌ Could not extract search query from: {intent}"
        
        print(f"🔍 Browser: {browser}, Query: '{search_query}'")
        
        # Create Google search URL
        encoded_query = urllib.parse.quote(search_query)
        search_url = f"https://www.google.com/search?q={encoded_query}"
        
        # Store context for follow-up commands
        last_search_context = {
            'type': 'web_search',
            'browser': browser,
            'query': search_query,
            'search_url': search_url,
            'timestamp': time.time()
        }
        
        # Open browser with search URL using WebDriver for automation compatibility
        try:
            # Import the web automation coordinator for WebDriver-based opening
            import importlib.util
            import os
            
            # Get the path to the web automation coordinator
            current_dir = os.path.dirname(os.path.abspath(__file__))
            coordinator_path = os.path.join(current_dir, 'tools', 'web_automation', 'coordinator.py')
            
            if os.path.exists(coordinator_path) and browser == 'Google Chrome':
                # Use WebDriver Chrome for automated browsing
                print("🤖 Using WebDriver Chrome for automation compatibility...")
                
                # Load the module dynamically
                spec = importlib.util.spec_from_file_location("coordinator", coordinator_path)
                coordinator_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(coordinator_module)
                
                # Get the coordinator class
                WebAutomationCoordinator = coordinator_module.WebAutomationCoordinator
                
                # Create coordinator instance with visible browser (not headless)
                coordinator = WebAutomationCoordinator(headless=False)
                coordinator._ensure_browser_ready()
                
                if coordinator.commander and coordinator.commander.driver:
                    # Navigate to the search URL
                    coordinator.commander.driver.get(search_url)
                    print(f"🔍 WebDriver Chrome opened with search: '{search_query}'")
                    
                    # Store the coordinator instance for later use
                    last_search_context['webdriver_coordinator'] = coordinator
                    
                    return f"✅ Opened automated Chrome and searched for '{search_query}'"
                else:
                    raise Exception("Failed to initialize WebDriver Chrome")
            else:
                # Fallback to regular browser opening for Safari/Firefox or if WebDriver not available
                if browser == 'Safari':
                    result = subprocess.run(['open', '-a', 'Safari', search_url], capture_output=True, text=True)
                elif browser == 'Firefox':
                    result = subprocess.run(['open', '-a', 'Firefox', search_url], capture_output=True, text=True)
                else:  # Chrome fallback
                    result = subprocess.run(['open', '-a', 'Google Chrome', search_url], capture_output=True, text=True)
                
                if result.returncode == 0:
                    return f"✅ Opened {browser} and searched for '{search_query}'"
                else:
                    return f"❌ Failed to open {browser}: {result.stderr}"
                    
        except Exception as e:
            print(f"⚠️ WebDriver opening failed: {e}")
            # Fallback to regular Chrome
            result = subprocess.run(['open', '-a', 'Google Chrome', search_url], capture_output=True, text=True)
            if result.returncode == 0:
                return f"✅ Opened {browser} and searched for '{search_query}' (fallback)"
            else:
                return f"❌ Failed to open {browser}: {result.stderr}"
            
    except Exception as e:
        return f"❌ Web browser search error: {e}"

def handle_contextual_followup_command(intent):
    """Handle context-aware follow-up commands like 'open first link'"""
    try:
        import time
        
        print(f"🔗 Contextual follow-up triggered for: '{intent}'")
        
        # Check if we have recent search context
        global last_search_context
        if 'last_search_context' not in globals() or not last_search_context:
            return "❌ No recent search context found. Please search for something first."
        
        # Check if context is recent (within 5 minutes)
        current_time = time.time()
        if current_time - last_search_context.get('timestamp', 0) > 300:  # 5 minutes
            return "❌ Search context too old. Please perform a new search first."
        
        # For now, let's trigger autonomous learning for this capability
        print("🧠 Triggering autonomous learning for web interaction...")
        
        # Try to use existing web automation tools with WebDriver
        try:
            # Check if we have a stored WebDriver coordinator from the previous search
            if last_search_context.get('webdriver_coordinator'):
                print("🤖 Using existing WebDriver session for context-aware clicking...")
                coordinator = last_search_context['webdriver_coordinator']
                search_query = last_search_context.get('query', 'unknown')
                
                # Use the direct click first search result method
                result = coordinator.click_first_search_result(search_query)
                
                if result.get('success'):
                    return f"✅ {result.get('message', 'Successfully clicked first search result using WebDriver')}"
                else:
                    print("🔄 WebDriver click failed, trying keyboard navigation fallback...")
                    # Fall through to keyboard navigation fallback
            
            # If no existing WebDriver session, create a new one
            # Import the web automation coordinator that uses WebDriver
            import importlib.util
            import os
            
            # Get the path to the web automation coordinator
            current_dir = os.path.dirname(os.path.abspath(__file__))
            coordinator_path = os.path.join(current_dir, 'tools', 'web_automation', 'coordinator.py')
            
            if os.path.exists(coordinator_path):
                # Load the module dynamically
                spec = importlib.util.spec_from_file_location("coordinator", coordinator_path)
                coordinator_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(coordinator_module)
                
                # Get the coordinator class
                WebAutomationCoordinator = coordinator_module.WebAutomationCoordinator
                
                # Create coordinator instance with visible browser (not headless)
                coordinator = WebAutomationCoordinator(headless=False)
                
                # Construct command based on context
                search_query = last_search_context.get('query', 'unknown')
                browser = last_search_context.get('browser', 'Google Chrome')
                
                print(f"🤖 Using WebDriver automation for: {intent}")
                print(f"🔍 Search query: {search_query}")
                
                # Use the direct click first search result method
                result = coordinator.click_first_search_result(search_query)
                
                if result.get('success'):
                    return f"✅ {result.get('message', 'Successfully clicked first search result using WebDriver')}"
                else:
                    print("🔄 WebDriver failed, trying keyboard navigation fallback...")
                    # Fall through to keyboard navigation fallback
            else:
                raise ImportError("Web automation coordinator not found")
                
        except Exception as e:
            print(f"⚠️ WebDriver automation not available: {e}")
            
            # Fallback to the enhanced web link automation
            import importlib.util
            import os
            
            # Get the path to the web_link_automation tool
            current_dir = os.path.dirname(os.path.abspath(__file__))
            tool_path = os.path.join(current_dir, 'tools', 'web_link_automation.py')
            
            if os.path.exists(tool_path):
                # Load the module dynamically
                spec = importlib.util.spec_from_file_location("web_link_automation", tool_path)
                web_link_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(web_link_module)
                
                # Get the function
                click_first_search_result = web_link_module.click_first_search_result
                
                # Construct command based on context
                search_query = last_search_context.get('query', 'unknown')
                browser = last_search_context.get('browser', 'Google Chrome')
                
                print(f"🤖 Using fallback automation for: {intent}")
                result = click_first_search_result(browser, search_query, wait_time=2)
                
                if result.get('success'):
                    return f"✅ {result.get('message', 'Successfully clicked first link')}"
                else:
                    return f"⚠️ {result.get('message', 'Could not click first link')}"
            else:
                # Final fallback: Use enhanced web browsing
                return handle_enhanced_web_browsing_followup(intent, last_search_context)
            
    except Exception as e:
        return f"❌ Contextual follow-up error: {e}"

def handle_enhanced_web_browsing_followup(intent, context):
    """Enhanced web browsing with Selenium for follow-up actions"""
    try:
        print("🌟 Using enhanced web browsing for contextual follow-up...")
        
        # This would trigger the autonomous learning system to create
        # a sophisticated web interaction tool
        search_query = context.get('query', 'unknown')
        browser = context.get('browser', 'Google Chrome')
        
        # For now, provide a helpful message and trigger learning
        message = f"""
🧠 Learning new capability: Web page interaction
📋 Context: User searched for '{search_query}' and wants to click the first link
🔧 This would require:
   1. Selenium WebDriver automation
   2. Page element detection
   3. Safe click automation
   4. Error handling for popups/ads
   
⚡ Triggering autonomous learning to create this capability...
"""
        
        print(message)
        
        # Return a helpful response for now
        return f"🔄 I'm learning how to click links on web pages. For now, please manually click the first search result for '{search_query}' in {browser}. I'll have this capability soon!"
        
    except Exception as e:
        return f"❌ Enhanced web browsing error: {e}"

def handle_youtube_automation_command(intent):
    """Handle YouTube automation commands using memory patterns"""
    try:
        import os
        import json
        import re
        import subprocess
        
        print(f"🎥 YouTube automation triggered for: '{intent}'")
        
        # Check memory for YouTube patterns
        memory_file = '/Users/mahendrabahubali/chotu/memory/web_learnings.json'
        rom_file = '/Users/mahendrabahubali/chotu/memory/rom.json'
        
        # Load YouTube automation patterns from memory
        youtube_patterns = []
        try:
            if os.path.exists(memory_file):
                with open(memory_file, 'r') as f:
                    web_learnings = json.load(f)
                    youtube_data = web_learnings.get('site_patterns', {}).get('youtube.com', {})
                    if youtube_data.get('automation_available'):
                        youtube_patterns = youtube_data.get('command_patterns', [])
                        print(f"📚 Found {len(youtube_patterns)} YouTube patterns in memory")
        except Exception as e:
            print(f"⚠️ Could not load web learnings: {e}")
        
        # Check if current command matches known patterns
        intent_lower = intent.lower()
        pattern_matched = False
        
        for pattern in youtube_patterns:
            # Convert pattern to regex (replace * with .*)
            pattern_regex = pattern.replace('*', '.*')
            if re.search(pattern_regex, intent_lower):
                pattern_matched = True
                print(f"✅ Matched pattern: '{pattern}'")
                break
        
        # Use enhanced YouTube automation with proper query extraction
        try:
            # Import enhanced YouTube automation functions with better path handling
            import sys
            import os
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            sys.path.append(project_root)
            
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            from mcp.tools.web_automation_tool import _extract_youtube_query
            from mcp.tools.enhanced_youtube_automation import enhanced_youtube_play
            
            # Extract search query using enhanced extraction
            search_query = _extract_youtube_query(intent)
            print(f"🎯 Enhanced query extraction: '{search_query}'")
            
            # Use enhanced YouTube automation
            print(f"🚀 Using enhanced YouTube automation with query: '{search_query}'")
            result = enhanced_youtube_play(search_query, stop_current=True)
            
            if result.get('success'):
                video_title = result.get('video_title', search_query)
                return f"✅ Successfully played '{video_title}' on YouTube with enhanced automation"
            else:
                error_msg = result.get('error', 'Unknown error')
                print(f"❌ Enhanced YouTube automation failed: {error_msg}")
                # Fallback to old method
                return handle_youtube_fallback_old_method(intent)
                
        except Exception as e:
            print(f"⚠️ Enhanced automation not available, using fallback: {e}")
            return handle_youtube_fallback_old_method(intent)
            
    except Exception as e:
        print(f"❌ YouTube automation error: {e}")
        return f"❌ YouTube automation error: {e}"

def handle_youtube_fallback_old_method(intent):
    """Fallback to old YouTube automation method"""
    
    import re
    import subprocess
    
    intent_lower = intent.lower()
    
    # Extract search query from command - improved patterns
    search_query = ""
    
    # Enhanced pattern matching for different command types
    search_patterns = [
        r'(?:open youtube and play|play on youtube)\s+(.+)',           # "open youtube and play [song]" 
        r'play\s+(.+?)\s+(?:on\s+)?youtube',                          # "play [song] on youtube"
        r'search\s+(.+?)\s+on\s+youtube',                             # "search [query] on youtube"
        r'youtube\s+search\s+(.+)',                                   # "youtube search [query]"
        r'find\s+(.+?)\s+on\s+youtube',                               # "find [query] on youtube"
        r'search\s+and\s+play\s+(.+?)\s+on\s+youtube',               # "search and play [song] on youtube"
        r'(?:youtube|play)\s+(.+)',                                   # Generic "youtube [query]" or "play [query]"
    ]
    
    for pattern in search_patterns:
        match = re.search(pattern, intent_lower)
        if match:
            search_query = match.group(1).strip()
            # Clean up common trailing words
            search_query = re.sub(r'\s+(on\s+youtube|youtube)$', '', search_query)
            print(f"� Extracted search query: '{search_query}'")
            break
    
    # If no specific search query found, use the entire intent minus command words
    if not search_query:
        # Remove common command words but preserve content
        cleaned = intent_lower
        remove_words = ['open', 'youtube', 'and', 'play', 'search', 'find']
        for word in remove_words:
            cleaned = re.sub(r'\b' + word + r'\b', '', cleaned)
        search_query = ' '.join(cleaned.split()).strip()
        
        # If still empty, use a sensible default
        if not search_query or len(search_query) < 2:
            search_query = "music"
        
        print(f"🎯 Cleaned search query: '{search_query}'")
    
    print(f"🎯 Final search query: '{search_query}'")
    
    # Execute YouTube automation
    automation_script = '/Users/mahendrabahubali/chotu/chotu_youtube_player.py'
    
    if os.path.exists(automation_script):
        print(f"🚀 Executing old YouTube automation with query: '{search_query}'")
        
        # Run the YouTube automation script
        try:
            result = subprocess.run([
                'python3', automation_script, 
                '--search', search_query,
                '--headless', 'false'  # Show browser for debugging
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print("✅ YouTube automation completed successfully")
                return f"✅ Successfully played '{search_query}' on YouTube with ad-skipping enabled"
            else:
                print(f"❌ YouTube automation failed: {result.stderr}")
                return f"❌ YouTube automation failed: {result.stderr}"
                
        except subprocess.TimeoutExpired:
            return "⏰ YouTube automation timed out (60s)"
        except Exception as e:
            return f"❌ Error executing YouTube automation: {e}"
    else:
        print(f"❌ YouTube automation script not found: {automation_script}")
        # Fallback: try to open YouTube in browser
        return handle_youtube_fallback(search_query)

def handle_youtube_fallback(search_query):
    """Fallback YouTube handling when automation script is not available"""
    try:
        import subprocess
        import urllib.parse
        
        # Encode search query for URL
        encoded_query = urllib.parse.quote(search_query)
        youtube_url = f"https://www.youtube.com/results?search_query={encoded_query}"
        
        # Open YouTube in default browser
        result = subprocess.run(['open', youtube_url], capture_output=True, text=True)
        
        if result.returncode == 0:
            return f"✅ Opened YouTube search for '{search_query}' in browser"
        else:
            return f"❌ Failed to open YouTube: {result.stderr}"
            
    except Exception as e:
        return f"❌ YouTube fallback error: {e}"

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint with dynamic capabilities"""
    current_capabilities = tool_loader.get_all_capabilities()
    return jsonify({
        "status": "healthy",
        "message": "Chotu Self-Learning MCP Server is running",
        "dynamic_capabilities": current_capabilities,
        "total_tools": len(current_capabilities),
        "pending_tasks": len(pending_tasks),
        "learning_enabled": True
    })

@app.route('/capabilities', methods=['GET'])
def get_capabilities():
    """Return all available capabilities (static + dynamic)"""
    return jsonify(tool_loader.get_all_capabilities())

@app.route('/learn', methods=['POST'])
def manual_learn():
    """Manually trigger learning for a specific capability"""
    data = request.json
    user_request = data.get('request', '')
    
    if not user_request:
        return jsonify({"error": "No request provided"}), 400
    
    current_capabilities = tool_loader.get_all_capabilities()
    
    success = tool_generator.learn_new_capability(user_request, current_capabilities)
    
    if success:
        tool_loader.load_all_tools()
        return jsonify({
            "success": True,
            "message": f"Successfully learned new capability for: {user_request}",
            "new_capabilities": tool_loader.get_all_capabilities()
        })
    else:
        return jsonify({
            "success": False,
            "message": f"Failed to learn capability for: {user_request}"
        }), 500

@app.route('/reload', methods=['POST'])
def reload_tools():
    """Manually reload all tools"""
    count = tool_loader.load_all_tools()
    return jsonify({
        "success": True,
        "message": f"Reloaded {count} tools",
        "capabilities": tool_loader.get_all_capabilities()
    })

@app.route('/pending', methods=['GET'])
def get_pending_tasks():
    """Get list of pending/failed tasks"""
    return jsonify({
        "pending_tasks": pending_tasks,
        "count": len(pending_tasks)
    })

@app.route('/learning_log', methods=['GET'])
def get_learning_log():
    """Get the learning history"""
    try:
        with open('learning_log.json', 'r') as f:
            log_data = json.load(f)
        return jsonify(log_data)
    except FileNotFoundError:
        return jsonify({"learned_tools": [], "message": "No learning history yet"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ========== AUTONOMOUS SELF-LEARNING ENDPOINTS ==========

@app.route('/autonomous_learn', methods=['POST'])
def autonomous_learn():
    """Trigger autonomous learning for a new capability"""
    data = request.json
    intent = data.get('intent', '')
    context = data.get('context', {})
    
    if not intent:
        return jsonify({"error": "No intent provided"}), 400
    
    print(f"🧠 Autonomous learning triggered for: {intent}")
    
    try:
        result = self_learning_controller.handle_new_request(intent, context)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Autonomous learning failed: {str(e)}"
        }), 500

@app.route('/learning_stats', methods=['GET'])
def get_learning_statistics():
    """Get learning performance statistics"""
    try:
        stats = self_learning_controller.get_learning_statistics()
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/create_checkpoint', methods=['POST'])
def create_checkpoint():
    """Create a system checkpoint"""
    data = request.json
    checkpoint_name = data.get('name', f'checkpoint_{int(time.time())}')
    
    try:
        success = self_learning_controller.create_system_checkpoint(checkpoint_name)
        if success:
            return jsonify({
                "success": True,
                "message": f"Checkpoint '{checkpoint_name}' created successfully"
            })
        else:
            return jsonify({
                "success": False,
                "message": "Failed to create checkpoint"
            }), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/rollback_checkpoint', methods=['POST'])
def rollback_checkpoint():
    """Rollback to a previous checkpoint"""
    data = request.json
    checkpoint_path = data.get('checkpoint_path', '')
    
    if not checkpoint_path:
        return jsonify({"error": "No checkpoint path provided"}), 400
    
    try:
        success = self_learning_controller.rollback_to_checkpoint(checkpoint_path)
        if success:
            # Reload tools after rollback
            tool_loader.load_all_tools()
            return jsonify({
                "success": True,
                "message": f"Successfully rolled back to checkpoint: {checkpoint_path}"
            })
        else:
            return jsonify({
                "success": False,
                "message": "Failed to rollback to checkpoint"
            }), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/validate_system', methods=['GET'])
def validate_system():
    """Validate system integrity"""
    try:
        integrity_report = self_learning_controller.updater.validate_integrity()
        return jsonify(integrity_report)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    import time
    print("🧠 Starting Autonomous Self-Learning Chotu MCP Server...")
    print("🔧 Initializing dynamic tool loading...")
    
    # Load all existing tools
    count = tool_loader.load_all_tools()
    print(f"✅ Loaded {count} existing tools")
    
    # Display self-learning capabilities
    stats = self_learning_controller.get_learning_statistics()
    print(f"🎯 Autonomous Learning System Ready")
    print(f"   Success Rate: {stats['success_rate']:.1f}%")
    print(f"   Tools Generated: {stats['tools_generated']}")
    print(f"   Safety Mode: {'ON' if stats['safety_mode'] else 'OFF'}")
    print(f"   Max Tools: {stats['max_tools']}")
    
    print("🚀 Server ready - Can learn new capabilities autonomously!")
    print("📡 Autonomous Learning endpoints:")
    print("   POST /autonomous_learn - Trigger autonomous learning")
    print("   GET /learning_stats - View learning statistics") 
    print("   POST /create_checkpoint - Create system checkpoint")
    print("   POST /rollback_checkpoint - Rollback to checkpoint")
    print("   GET /validate_system - Validate system integrity")
    print("📡 Legacy endpoints:")
    print("   POST /learn - Manually teach new capability")
    print("   GET /learning_log - View learning history")
    print("   POST /reload - Reload all tools")
    
    app.run(host='localhost', port=8000, debug=True)
