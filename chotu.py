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
        
        print("🤖 Chotu AI Agent initialized")
        print("🧠 Advanced features: NLP, Context Memory, Wake Word Detection")
        
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
        
        # Wait for server to start
        time.sleep(3)
        
        # Test server connection
        try:
            response = requests.get("http://localhost:8000/status", timeout=5)
            if response.status_code == 200:
                status = response.json()
                tool_count = status.get("tools_loaded", 0)
                print(f"✅ MCP server running with {tool_count} tools loaded")
                speak(f"Self-learning server ready with {tool_count} tools available!")
                return True
            else:
                print("⚠️  MCP server started but status unclear")
                speak("Self-learning server started")
                return True
        except Exception as e:
            print(f"⚠️  Could not verify MCP server status: {e}")
            speak("Self-learning server may be starting up")
            return False
    
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
            "processing_mode": "advanced"
        }
        save_ram(ram)
        
        # Enhanced confidence calculation
        base_confidence = calculate_confidence(user_input)
        
        # Boost confidence based on NLP analysis
        if nlp_context['intent'] != 'general':
            base_confidence += 20
        
        # Boost confidence based on context
        if "similar interactions" in memory_context:
            base_confidence += 15
        
        # Cap confidence at 100
        confidence = min(base_confidence, 100)
        
        print(f"📊 Confidence: {confidence}% | Intent: {nlp_context['intent']} | Sentiment: {nlp_context['sentiment']}")
        
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
        
        # Create enhanced prompt with NLP and context
        gpt_prompt = f"""
        You are Chotu, an advanced AI assistant like J.A.R.V.I.S. with strong conversational memory.
        
        Current User Command: '{ram['raw_input']}'
        NLP Analysis: {nlp_context}
        Extended Conversation Context (Last 9 Interactions): {ram['memory_context']}
        
        CRITICAL CONTEXT ANALYSIS RULES:
        1. ALWAYS analyze the last 9 conversation interactions before interpreting ambiguous commands
        2. If user says "it" / "this" / "that" - scan the 9 recent interactions to find what they're referring to
        3. Pay special attention to subjects mentioned in the conversation flow
        4. "no [command]" means they want to correct/change the previous action
        5. "decrease it" / "increase it" / "make it X" - determine what "it" refers to from the 9-interaction context
        6. Look for patterns: if they recently discussed brightness, volume, apps, etc.
        
        ENHANCED CONTEXT EXAMPLES:
        - If any of the 9 recent interactions mention "brightness" and user says "decrease it" → they mean "decrease brightness"
        - If they recently set volume and say "increase it" → they mean "increase volume"  
        - If they say "no, decrease it" after brightness command → they want to decrease brightness instead
        - If they opened an app recently and say "close it" → they want to close that app
        
        With access to 9 recent interactions, analyze the conversation flow carefully and respond in JSON format:
        {{
            "understood_intent": "specific action to take (e.g., 'decrease brightness by 10%')",
            "confidence": 90,
            "context_reasoning": "Based on the 9 recent interactions, I see user was discussing [subject] in interactions #X and #Y, so 'it' refers to [subject]",
            "tools_needed": ["specific.tool.names"],
            "parameters": {{"key": "value"}},
            "response_tone": "professional"
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
            res = requests.post(MCP_URL, json=ram_data, timeout=30)
            
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
            error_msg = "Request timed out. MCP server might be slow."
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
        Create a comprehensive ROM entry for this successful command:
        Raw Input: {ram['raw_input']}
        Intent: {ram.get('interpreted_intent', 'Unknown')}
        NLP Analysis: {ram.get('nlp_analysis', {})}
        Tools Used: {ram.get('tools_needed', [])}
        
        Return JSON:
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
            
            # Try to parse JSON
            if response and response.startswith('{'):
                new_entry = json.loads(response)
                rom.append(new_entry)
                save_rom(rom)
                print("📘 Enhanced experience saved to ROM.")
            else:
                print("⚠️  GPT response not in JSON format, skipping learning.")
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
        print("\n💬 Say commands directly or 'exit' to quit")
        
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
