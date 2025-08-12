# chotu.py - Advanced J.A.R.V.I.S.-Inspired AI Agent
import json
import time
import threading
from datetime import datetime
from utils.voice_input import listen_voice
from utils.voice_output import speak
from utils.confidence_engine import calculate_confidence
from utils.gpt_interface import call_gpt
from utils.nlp_processor import NLPProcessor
from utils.wake_word_detector import WakeWordDetector
from memory.memory_manager import load_ram, save_ram, load_rom, save_rom
from memory.context_manager import ContextManager
from memory.intelligent_context_resolver import resolve_ambiguous_command, get_clarification_question
from memory.context_validator import validate_context_resolution

# Import autonomous system
try:
    from chotu_autonomous import ChouAutonomous
    AUTONOMOUS_AVAILABLE = True
    print("🤖 Autonomous system loaded successfully!")
except ImportError as e:
    print(f"⚠️  Autonomous system not available: {e}")
    AUTONOMOUS_AVAILABLE = False

# MCP Server URL
MCP_URL = "http://localhost:8000/execute"

class ChoutuAI:
    """Advanced J.A.R.V.I.S.-inspired AI Agent"""
    
    def __init__(self):
        self.nlp = NLPProcessor()
        self.context_manager = ContextManager()
        self.wake_detector = WakeWordDetector()
        self.is_active = False
        self.conversation_mode = False
        self.mcp_server_thread = None
        
        # Initialize autonomous system if available
        if AUTONOMOUS_AVAILABLE:
            try:
                self.autonomous_system = ChouAutonomous()
                print("🤖 Autonomous task execution system initialized")
            except Exception as e:
                print(f"⚠️  Failed to initialize autonomous system: {e}")
                self.autonomous_system = None
        else:
            self.autonomous_system = None
        
        print("🤖 Chotu AI Agent initialized")
        print("🧠 Advanced features: NLP, Context Memory, Wake Word Detection")
        if self.autonomous_system:
            print("🦾 Autonomous task execution: ENABLED")
        
    def start_mcp_server(self):
        """Start the MCP server in background"""
        import subprocess
        import time
        import os
        import requests
        
        # Check if MCP server is already running
        try:
            response = requests.get("http://localhost:8000/status", timeout=2)
            if response.status_code == 200:
                status = response.json()
                tool_count = status.get("tools_loaded", 0)
                print(f"✅ MCP server already running with {tool_count} tools loaded")
                speak(f"Self-learning server already ready with {tool_count} tools available!")
                return True
        except:
            # Server not running, continue to start it
            pass
        
        def run_mcp():
            try:
                # Get the directory of the current script
                current_dir = os.path.dirname(os.path.abspath(__file__))
                mcp_dir = os.path.join(current_dir, "mcp")
                
                print("🔧 Starting MCP server...")
                speak("Starting self-learning server...")
                
                # Start the MCP server from the mcp directory
                subprocess.run([
                    "python3", "mcp_server.py"
                ], cwd=mcp_dir)
                
            except Exception as e:
                print(f"❌ Failed to start MCP server: {e}")
        
        # Start MCP server in background thread
        self.mcp_server_thread = threading.Thread(target=run_mcp, daemon=True)
        self.mcp_server_thread.start()
        
        # Wait for server to start with progressive checking
        print("🔄 Waiting for MCP server to start...")
        server_ready = False
        max_attempts = 10  # Try for up to 10 seconds
        
        for attempt in range(max_attempts):
            try:
                response = requests.get("http://localhost:8000/status", timeout=2)
                if response.status_code == 200:
                    status = response.json()
                    tool_count = status.get("tools_loaded", 0)
                    print(f"✅ MCP server running with {tool_count} tools loaded")
                    speak(f"Self-learning server ready with {tool_count} tools available!")
                    server_ready = True
                    break
                else:
                    print("⚠️  MCP server started but status unclear")
                    speak("Self-learning server started")
                    server_ready = True
                    break
            except Exception as e:
                if attempt < max_attempts - 1:  # Don't print error on last attempt
                    time.sleep(1)  # Wait 1 second between attempts
                    continue
                else:
                    # Only show warning on final attempt
                    print("ℹ️  MCP server starting in background - this is normal")
                    speak("Self-learning server starting up")
                    server_ready = True  # Continue anyway
                    break
        
        return server_ready
    
    def is_autonomous_command(self, command):
        """Check if the command should be handled by autonomous system"""
        autonomous_keywords = [
            'open chrome', 'open browser', 'start browser',
            'navigate to', 'go to website', 'browse to', 'go to',
            'click on', 'scroll down', 'scroll up',
            'type', 'enter text', 'search for', 'search',
            'fill form', 'submit form', 'download',
            'take screenshot', 'automate', 'perform task',
            'amazon.com', 'google.com', 'youtube.com',  # Common sites
            'find on page', 'click button', 'fill field'
        ]
        
        command_lower = command.lower()
        
        # Check for search patterns specifically
        search_patterns = [
            'search', 'find', 'look for', 'amazon.com', 'google.com',
            'navigate', 'go to', 'browse', 'visit'
        ]
        
        # If command contains search terms with a website, it's autonomous
        if any(pattern in command_lower for pattern in search_patterns):
            return True
            
        return any(keyword in command_lower for keyword in autonomous_keywords)
    
    def handle_autonomous_command(self, command):
        """Handle command using autonomous system"""
        if not self.autonomous_system:
            speak("Autonomous system is not available")
            return
        
        try:
            print(f"🤖 Processing autonomous command: {command}")
            speak("Executing autonomous task...")
            
            # Process the command through autonomous system using asyncio
            import asyncio
            
            # Check if we're already in an event loop
            try:
                loop = asyncio.get_running_loop()
                # We're in an event loop, need to run in a new thread
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, self.autonomous_system.process_user_input(command))
                    result = future.result(timeout=30)  # 30 second timeout
            except RuntimeError:
                # No event loop running, we can use asyncio.run directly
                result = asyncio.run(self.autonomous_system.process_user_input(command))
            
            # The autonomous system returns a string response, not a dict
            if result and not result.startswith("❌"):
                # Success - result contains the success message
                speak("Task completed successfully")
                print(f"✅ Autonomous task completed: {result}")
                
                # Add to context for future reference
                self.context_manager.add_interaction(command, result, success=True)
                
            else:
                # Error - result contains error message
                error_msg = result if result else "Failed to execute autonomous task"
                speak(f"Task failed: {error_msg}")
                print(f"❌ Autonomous task failed: {error_msg}")
                
        except Exception as e:
            error_msg = f"Autonomous system error: {str(e)}"
            speak(error_msg)
            print(f"❌ {error_msg}")
    
    def wake_word_callback(self, command):
        """Callback when wake word is detected"""
        speak("Yes, I'm listening")
        
        if command:
            # Process the command immediately
            self.process_command(command)
        else:
            # Listen for a new command
            user_input = self.wake_detector.listen_for_command()
            if user_input:
                self.process_command(user_input)
            else:
                speak("I didn't catch that. Say 'Hey Chotu' again if you need me.")
    
    def process_command(self, user_input):
        """Process a user command with advanced NLP and context"""
        
        # Check if this is an autonomous task command first
        if self.autonomous_system and self.is_autonomous_command(user_input):
            print("🤖 Detected autonomous task command")
            return self.handle_autonomous_command(user_input)
        
        # STEP 1: Intelligent Context Resolution for Ambiguous Commands
        context_resolution = resolve_ambiguous_command(user_input)
        
        if context_resolution['needs_clarification']:
            # Ask for clarification if context is unclear
            clarification = get_clarification_question(
                context_resolution['alternatives'], 
                user_input
            )
            speak(clarification)
            print(f"🤔 Context unclear: {context_resolution['reasoning']}")
            return
        
        # Use resolved command if context was successfully determined
        if context_resolution['resolved'] and context_resolution['confidence'] >= 60:
            resolved_input = context_resolution['resolved_command']
            
            # STEP 1.5: Validate if the resolved context actually makes logical sense
            validation_result = validate_context_resolution(
                user_input,
                resolved_input,
                context_resolution,
                context_resolution.get('alternatives', [])
            )
            
            print(f"🔍 Context Validation Results:")
            print(f"   Original: '{user_input}' → Resolved: '{resolved_input}'")
            print(f"   Valid: {validation_result['valid']}")
            print(f"   Reasoning: {validation_result['reasoning']}")
            
            if validation_result['valid']:
                # Context makes sense, use it
                user_input = validation_result['final_command']
                print(f"✅ Using validated command: '{user_input}'")
                speak(f"I understand you want to {user_input}")
                
            elif validation_result['needs_clarification']:
                # Context doesn't make sense, ask for clarification
                clarification = validation_result.get('clarification_question', 
                    f"I found '{resolved_input}' in recent context, but that doesn't make logical sense. What did you want me to do?")
                
                print(f"🤔 Logical validation failed: {validation_result['reasoning']}")
                speak(clarification)
                return
                
            else:
                # Use the suggested action if available
                if validation_result.get('suggested_action'):
                    user_input = validation_result['suggested_action']
                    print(f"🔧 Using suggested action: '{user_input}'")
                    speak(f"I think you meant {user_input}")
                else:
                    print(f"❌ No valid interpretation found: {validation_result['reasoning']}")
                    speak("I'm not sure what you want me to do. Could you be more specific?")
                    return
        
        # STEP 2: Continue with enhanced NLP and context analysis
        # Analyze input with NLP
        nlp_context = self.nlp.generate_response_context(user_input)
        
        # Get relevant context from memory
        memory_context = self.context_manager.get_relevant_context(user_input)
        
        # Create enhanced RAM entry
        ram = {
            "raw_input": user_input,
            "timestamp": datetime.now().isoformat(),
            "nlp_analysis": nlp_context,
            "memory_context": memory_context,
            "context_resolution": context_resolution,
            "processing_mode": "intelligent_context"
        }
        save_ram(ram)
        
        # Enhanced confidence calculation
        base_confidence = calculate_confidence(user_input)
        
        # Boost confidence based on successful context resolution
        if context_resolution['resolved']:
            base_confidence += context_resolution['confidence'] // 3  # Add up to 33 points
        
        # Boost confidence based on NLP analysis
        if nlp_context['intent'] != 'general':
            base_confidence += 20
        
        # Boost confidence based on context
        if "similar interactions" in memory_context:
            base_confidence += 15
        
        # Cap confidence at 100
        confidence = min(base_confidence, 100)
        
        print(f"📊 Final Confidence: {confidence}% | Intent: {nlp_context['intent']} | Sentiment: {nlp_context['sentiment']}")
        
        # Process based on confidence and intent
        if confidence >= 85:
            self.handle_high_confidence(ram, confidence, nlp_context)
        elif confidence >= 40:
            self.handle_medium_confidence(ram, confidence, nlp_context)
        else:
            self.handle_low_confidence(user_input)
    
    def handle_high_confidence(self, ram, confidence, nlp_context):
        """Handle high confidence commands"""
        print("✅ High confidence. Processing with advanced routing.")
        
        ram["confidence"] = confidence
        ram["interpreted_intent"] = self.get_enhanced_intent(ram["raw_input"], nlp_context)
        save_ram(ram)
        
        response = self.send_to_mcp(ram)
        
        # Add to context
        self.context_manager.add_interaction(
            ram["raw_input"], 
            response, 
            success=True
        )
    
    def handle_medium_confidence(self, ram, confidence, nlp_context):
        """Handle medium confidence commands with GPT assistance"""
        print("🤔 Medium confidence. Using advanced GPT analysis.")
        
        # Create enhanced prompt with NLP and intelligent context resolution
        context_info = ram.get('context_resolution', {})
        
        gpt_prompt = f"""
        You are Chotu, an advanced AI assistant like J.A.R.V.I.S. with intelligent context resolution capabilities.
        
        Current User Command: '{ram['raw_input']}'
        NLP Analysis: {nlp_context}
        Extended Conversation Context (Last 9 Interactions): {ram['memory_context']}
        
        INTELLIGENT CONTEXT RESOLUTION RESULTS:
        - Resolved Command: '{context_info.get('resolved_command', 'No resolution')}'
        - Context Confidence: {context_info.get('confidence', 0)}%
        - Context Source: {context_info.get('context_source', 'none')}
        - Reasoning: {context_info.get('reasoning', 'No context reasoning available')}
        
        ENHANCED CONTEXT ANALYSIS WITH MULTI-LAYER MEMORY:
        1. I have access to RAM (current session), ROM (long-term learned patterns), and 9 recent interactions
        2. For ambiguous commands like "increase it", I check all memory layers to find what "it" refers to
        3. I analyze conversation flow, recently mentioned subjects, and user patterns
        4. I provide confidence scores and reasoning for context resolution
        
        CONTEXT RESOLUTION EXAMPLES:
        - If user recently discussed brightness and says "increase it" → "increase brightness"
        - If they opened Chrome and say "close it" → "close chrome" 
        - If they set volume to 50% and say "make it louder" → "increase volume"
        - If context is unclear, I ask clarifying questions rather than guessing
        
        CRITICAL: Use the context resolution results above to inform your interpretation. 
        If context resolution confidence is ≥60%, trust the resolved command.
        If context resolution confidence is <60%, ask for clarification.
        
        Respond in JSON format:
        {{
            "understood_intent": "specific action to take based on context resolution",
            "confidence": 90,
            "context_reasoning": "How I determined what the user meant using memory layers",
            "tools_needed": ["specific.tool.names"],
            "parameters": {{"key": "value"}},
            "response_tone": "professional",
            "uses_context_resolution": true
        }}
        """
        
        try:
            gpt_response = call_gpt(gpt_prompt)
            gpt_json = json.loads(gpt_response)
            ram.update(gpt_json)
            save_ram(ram)
            
            if ram.get("confidence", 0) >= 75:
                response = self.send_to_mcp(ram)
                self.context_manager.add_interaction(ram["raw_input"], response, True)
            else:
                speak("I'm not entirely sure about that. Could you be more specific?")
                
        except Exception as e:
            print(f"❌ GPT processing error: {e}")
            speak("I encountered an error processing that request.")
    
    def handle_low_confidence(self, user_input):
        """Handle low confidence commands"""
        responses = [
            "I didn't quite catch that. Could you repeat it?",
            "I'm not sure I understood. Can you rephrase that?",
            "Could you be more specific about what you'd like me to do?"
        ]
        
        import random
        speak(random.choice(responses))
    
    def get_enhanced_intent(self, command, nlp_context):
        """Get enhanced intent using NLP analysis and ROM"""
        # First check ROM
        rom = load_rom()
        for entry in rom:
            if "input_pattern" in entry and entry["input_pattern"].lower() in command.lower():
                return entry["intent"]
        
        # Use NLP analysis
        intent = nlp_context['intent']
        parameters = nlp_context.get('parameters', {})
        
        # Check if command contains specific values (numbers, percentages)
        import re
        has_specific_value = re.search(r'\d+%?', command)
        
        # For system control with specific values, preserve the original command
        if intent == 'system_control' and has_specific_value:
            print(f"🔧 Preserving original command with specific value: '{command}'")
            return command.lower()
        elif intent == 'system_control' and parameters:
            return f"{parameters.get('action', 'control')} {parameters.get('control_type', 'system')}"
        elif intent == 'app_control' and parameters:
            return f"{parameters.get('action', 'open')} {parameters.get('app_name', 'application')}"
        
        return command
    
    def send_to_mcp(self, ram_data):
        """Send command to MCP server with enhanced error handling"""
        import requests
        try:
            # Send the full RAM data to the MCP server's execute endpoint
            # Increased timeout for stealth browser operations (YouTube automation can take 60+ seconds)
            res = requests.post(MCP_URL, json=ram_data, timeout=25)
            
            if res.status_code == 200:
                result = res.json()
                response_text = result.get("output", result.get("message", "Task completed."))
                
                # Check if tool was generated or used
                if result.get("learned"):
                    speak(f"I learned something new! {response_text}")
                else:
                    speak(response_text)
                
                # Learn from success
                self.learn_from_success(ram_data)
                return response_text
            else:
                error_msg = f"MCP server responded with status {res.status_code}"
                speak(error_msg)
                return error_msg
            
        except requests.Timeout:
            error_msg = "Task is still running in background. Please wait for completion."
            speak(error_msg)
            return error_msg
        except requests.ConnectionError:
            error_msg = "Cannot connect to MCP server. Please start it first."
            speak(error_msg)
            return error_msg
        except Exception as e:
            error_msg = f"Failed to execute task: {str(e)}"
            speak(error_msg)
            print(f"❌ MCP Error: {e}")
            return error_msg
    
    def learn_from_success(self, ram):
        """Enhanced learning with context"""
        rom = load_rom()
        if any(r.get("raw_input") == ram["raw_input"] for r in rom):
            return  # Already learned
        
        prompt = f"""
        Create a comprehensive ROM entry for this successful command. Return ONLY valid JSON, no explanation text.
        
        Raw Input: {ram['raw_input']}
        Intent: {ram.get('interpreted_intent', 'Unknown')}
        NLP Analysis: {ram.get('nlp_analysis', {})}
        Tools Used: {ram.get('tools_needed', [])}
        
        Return this exact JSON format:
        {{
            "input_pattern": "{ram['raw_input'].lower()}",
            "intent": "{ram.get('interpreted_intent', 'run command')}",
            "action_flow": ["specific", "steps", "taken"],
            "confidence_boost": 100,
            "security_profile": "trusted",
            "context_tags": ["tag1", "tag2"],
            "success_count": 1
        }}
        """
        
        try:
            response = call_gpt(prompt)
            # Clean up the response to ensure it's valid JSON
            response = response.strip()
            if response.startswith('```json'):
                response = response[7:]
            if response.endswith('```'):
                response = response[:-3]
            response = response.strip()
            
            # Extract JSON from any explanatory text
            if '{' in response and '}' in response:
                start = response.find('{')
                end = response.rfind('}') + 1
                response = response[start:end]
            
            # Try to parse JSON
            if response and response.startswith('{'):
                new_entry = json.loads(response)
                rom.append(new_entry)
                save_rom(rom)
                print("📘 Enhanced experience saved to ROM.")
            else:
                print("⚠️  GPT response not in JSON format, skipping learning.")
                print(f"    Response: {response[:100]}...")
        except Exception as e:
            print(f"⚠️  Failed to learn from task: {e}")
    
    def start_voice_mode(self):
        """Start voice-controlled mode"""
        print("🎙️  Starting voice mode...")
        self.is_active = True
        
        while self.is_active:
            user_input = listen_voice()
            if not user_input:
                continue
                
            if user_input.lower() in ["exit", "quit", "goodbye", "shut down"]:
                speak("Shutting down Chotu. Goodbye!")
                break
                
            self.process_command(user_input)
    
    def start_wake_word_mode(self):
        """Start wake word detection mode"""
        print("👂 Starting wake word mode...")
        self.wake_detector.start_listening(self.wake_word_callback)
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Shutting down...")
            self.wake_detector.stop_listening_for_wake_word()
    
    def start_interactive_mode(self):
        """Start voice mode directly"""
        speak("Hello! I'm Chotu, your advanced self-learning AI assistant.")
        print("\n🤖 Chotu AI Agent - Enhanced with Self-Learning MCP Server")
        print("🎙️  Starting voice mode automatically...")
        print("\n✨ Enhanced Features:")
        print("   • 3-stage confidence system")
        print("   • Dynamic tool generation")
        print("   • Self-learning capabilities")
        print("   • macOS system integration")
        if self.autonomous_system:
            print("   • Autonomous task execution with stealth browser")
            print("   • Computer vision and automated interactions")
        print("\n💬 Say commands directly or 'exit' to quit")
        if self.autonomous_system:
            print("🤖 Try: 'open chrome', 'navigate to google.com', 'take screenshot'")
        
        # Start voice mode directly
        self.start_voice_mode()
    
    def start_text_mode(self):
        """Start text-based interaction mode"""
        print("💬 Text mode started. Type 'exit' to quit.")
        
        while True:
            user_input = input("You: ").strip()
            if user_input.lower() in ["exit", "quit"]:
                print("👋 Goodbye!")
                break
            
            if user_input:
                self.process_command(user_input)

def main():
    """Main entry point"""
    print("🟢 Initializing Chotu AI Agent...")
    chotu = ChoutuAI()
    
    # Start MCP server first
    print("🚀 Starting enhanced MCP server...")
    if chotu.start_mcp_server():
        print("✅ MCP server is ready!")
    else:
        print("⚠️  MCP server status unknown, but continuing...")
    
    # Start interactive mode
    chotu.start_interactive_mode()

if __name__ == "__main__":
    main()
