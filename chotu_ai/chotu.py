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
MCP_URL = "http://localhost:5000/execute"

class ChoutuAI:
    """Advanced J.A.R.V.I.S.-inspired AI Agent"""
    
    def __init__(self):
        self.nlp = NLPProcessor()
        self.context_manager = ContextManager()
        self.wake_detector = WakeWordDetector()
        self.is_active = False
        self.conversation_mode = False
        
        print("🤖 Chotu AI Agent initialized")
        print("🧠 Advanced features: NLP, Context Memory, Wake Word Detection")
    
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
        You are Chotu, an advanced AI assistant like J.A.R.V.I.S.
        
        User command: '{ram['raw_input']}'
        NLP Analysis: {nlp_context}
        Memory Context: {ram['memory_context']}
        
        Interpret this command and respond in JSON format:
        {{
            "understood_intent": "specific action to take",
            "confidence": 85,
            "tools_needed": ["specific.tool.names"],
            "parameters": {{"key": "value"}},
            "security_notes": "any security considerations",
            "response_tone": "professional|casual|friendly"
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
        
        # Create specific intent based on NLP
        if intent == 'system_control' and parameters:
            return f"{parameters.get('action', 'control')} {parameters.get('control_type', 'system')}"
        elif intent == 'app_control' and parameters:
            return f"{parameters.get('action', 'open')} {parameters.get('app_name', 'application')}"
        
        return command
    
    def send_to_mcp(self, ram_data):
        """Send command to MCP server with enhanced error handling"""
        import requests
        try:
            res = requests.post(MCP_URL, json=ram_data, timeout=10)
            result = res.json().get("output", "Task completed.")
            speak(result)
            
            # Learn from success
            self.learn_from_success(ram_data)
            return result
            
        except requests.Timeout:
            error_msg = "Request timed out. MCP server might be slow."
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
            new_entry = json.loads(response)
            rom.append(new_entry)
            save_rom(rom)
            print("📘 Enhanced experience saved to ROM.")
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
        """Start interactive mode selection"""
        speak("Hello! I'm Chotu, your advanced AI assistant.")
        print("\n🤖 Chotu AI Agent - Advanced Mode")
        print("1. Voice Mode (continuous listening)")
        print("2. Wake Word Mode (say 'Hey Chotu')")
        print("3. Text Mode (type commands)")
        
        while True:
            choice = input("\nSelect mode (1/2/3) or 'quit': ").strip()
            
            if choice == '1':
                self.start_voice_mode()
                break
            elif choice == '2':
                self.start_wake_word_mode()
                break
            elif choice == '3':
                self.start_text_mode()
                break
            elif choice.lower() == 'quit':
                print("👋 Goodbye!")
                break
            else:
                print("Invalid choice. Please select 1, 2, 3, or 'quit'.")
    
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
    chotu.start_interactive_mode()

if __name__ == "__main__":
    main()
