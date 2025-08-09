#!/usr/bin/env python3
"""
Chotu AI Agent Demo & Test Suite - Advanced Version
"""

import json
import sys
import os
sys.path.append(os.path.dirname(__file__))

from memory.memory_manager import save_rom, load_rom
from utils.voice_output import speak
from utils.nlp_processor import NLPProcessor

def create_advanced_demo_rom():
    """Create advanced demo ROM entries for Chotu to start with"""
    demo_rom = [
        {
            "input_pattern": "open safari",
            "intent": "open safari",
            "action_flow": ["browser.open"],
            "confidence_boost": 100,
            "security_profile": "trusted",
            "context_tags": ["browser", "web"],
            "success_count": 1
        },
        {
            "input_pattern": "open code",
            "intent": "open vs code",
            "action_flow": ["apps.open"],
            "confidence_boost": 100,
            "security_profile": "trusted",
            "context_tags": ["development", "editor"],
            "success_count": 1
        },
        {
            "input_pattern": "turn up volume",
            "intent": "volume up",
            "action_flow": ["system.volume"],
            "confidence_boost": 100,
            "security_profile": "trusted",
            "context_tags": ["audio", "system"],
            "success_count": 1
        },
        {
            "input_pattern": "increase brightness",
            "intent": "brightness up",
            "action_flow": ["system.brightness"],
            "confidence_boost": 100,
            "security_profile": "trusted",
            "context_tags": ["display", "system"],
            "success_count": 1
        },
        {
            "input_pattern": "what's the weather",
            "intent": "weather",
            "action_flow": ["weather.current"],
            "confidence_boost": 95,
            "security_profile": "trusted",
            "context_tags": ["information", "weather"],
            "success_count": 1
        },
        {
            "input_pattern": "take a screenshot",
            "intent": "screenshot",
            "action_flow": ["productivity.screenshot"],
            "confidence_boost": 95,
            "security_profile": "trusted",
            "context_tags": ["productivity", "capture"],
            "success_count": 1
        },
        {
            "input_pattern": "what's my next meeting",
            "intent": "next meeting",
            "action_flow": ["calendar.next"],
            "confidence_boost": 90,
            "security_profile": "trusted",
            "context_tags": ["calendar", "productivity"],
            "success_count": 1
        }
    ]
    
    save_rom(demo_rom)
    print("✅ Advanced demo ROM created with enhanced commands")

def test_nlp_processor():
    """Test the NLP processor"""
    print("\n🧠 Testing NLP Processor...")
    nlp = NLPProcessor()
    
    test_commands = [
        "Open Safari browser",
        "Turn up the volume please",
        "What's the weather like today?",
        "Take a screenshot of my screen",
        "Schedule a meeting for tomorrow"
    ]
    
    for command in test_commands:
        analysis = nlp.generate_response_context(command)
        print(f"Command: '{command}'")
        print(f"  Intent: {analysis['intent']}")
        print(f"  Entities: {analysis.get('entities', {})}")
        print(f"  Sentiment: {analysis['sentiment']}")
        print()

def test_voice_output():
    """Test the enhanced voice output system"""
    print("🔊 Testing enhanced voice output...")
    messages = [
        "Hello! I am Chotu, your advanced J.A.R.V.I.S.-inspired AI assistant.",
        "I now have enhanced capabilities including natural language processing, context memory, and wake word detection.",
        "I can help you with system control, calendar management, weather information, and much more!"
    ]
    
    for msg in messages:
        speak(msg)

def show_enhanced_features():
    """Display the enhanced features"""
    print("\n� CHOTU AI - ENHANCED FEATURES:")
    print("=" * 60)
    print("🧠 INTELLIGENCE:")
    print("   ✓ Advanced NLP Processing")
    print("   ✓ Context-Aware Memory")
    print("   ✓ Intent Recognition")
    print("   ✓ Sentiment Analysis")
    print("   ✓ Entity Extraction")
    print()
    print("🎙️ VOICE INTERFACE:")
    print("   ✓ Wake Word Detection ('Hey Chotu')")
    print("   ✓ Continuous Listening Mode")
    print("   ✓ Enhanced Speech Recognition")
    print("   ✓ Natural Text-to-Speech")
    print()
    print("🛠️ CAPABILITIES:")
    print("   ✓ System Control (Volume, Brightness)")
    print("   ✓ Application Management")
    print("   ✓ Calendar Integration")
    print("   ✓ Weather Information")
    print("   ✓ Productivity Tools")
    print("   ✓ File Operations")
    print("   ✓ Screenshot Capture")
    print("   ✓ Reminder Creation")
    print()
    print("🧠 LEARNING:")
    print("   ✓ Context-Based Learning")
    print("   ✓ Pattern Recognition")
    print("   ✓ Confidence Adaptation")
    print("   ✓ User Preference Memory")

def show_command_examples():
    """Show example commands"""
    print("\n🎯 ENHANCED COMMAND EXAMPLES:")
    print("=" * 50)
    print("System Control:")
    print("  • 'Turn up the volume'")
    print("  • 'Increase brightness'")
    print("  • 'Take a screenshot'")
    print("  • 'Show system information'")
    print()
    print("Productivity:")
    print("  • 'What's my next meeting?'")
    print("  • 'Create a reminder to call John'")
    print("  • 'Show my calendar for today'")
    print("  • 'Turn on do not disturb'")
    print()
    print("Information:")
    print("  • 'What's the weather like?'")
    print("  • 'What time is it?'")
    print("  • 'Show running applications'")
    print()
    print("Natural Conversation:")
    print("  • 'Hey Chotu, open my code editor'")
    print("  • 'Good morning, how are you?'")
    print("  • 'Thanks for the help!'")
    print()
    print("Wake Word Examples:")
    print("  • 'Hey Chotu' (activates listening)")
    print("  • 'Chotu, turn up volume'")
    print("  • 'Jarvis, what's the weather?'")

def main():
    print("🤖 CHOTU AI AGENT - ADVANCED DEMO & SETUP")
    print("=" * 60)
    
    # Show enhanced features
    show_enhanced_features()
    
    # Create advanced ROM
    create_advanced_demo_rom()
    
    # Test NLP
    test_nlp_processor()
    
    # Test voice output
    test_voice_output()
    
    # Show command examples
    show_command_examples()
    
    print("\n🚀 SETUP INSTRUCTIONS:")
    print("1. Dependencies: pip install -r requirements.txt")
    print("2. Start MCP Server: python3 mcp/mcp_server.py")
    print("3. Start Chotu: python3 chotu.py")
    print("4. Choose interaction mode:")
    print("   - Voice Mode (continuous)")
    print("   - Wake Word Mode ('Hey Chotu')")
    print("   - Text Mode (typing)")
    print()
    print("✨ Chotu now learns context and gets smarter with every interaction!")
    print("🎯 Try natural language: 'Hey Chotu, what's the weather and my next meeting?'")

if __name__ == "__main__":
    main()
