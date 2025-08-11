#!/usr/bin/env python3
"""
🧠 CHOTU CONTEXT MEMORY SYSTEM
==============================
Manages conversation context and follow-up command recognition
"""

import json
import time
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

class ContextMemory:
    """Manages conversation context for better follow-up command handling"""
    
    def __init__(self):
        self.conversation_history: List[Dict] = []
        self.current_context: Dict = {}
        self.last_action: Optional[Dict] = None
        self.session_start = time.time()
        
    def add_command(self, command: str, intent: str, result: Optional[Dict] = None):
        """Add a command to conversation history"""
        
        entry = {
            "timestamp": time.time(),
            "command": command.lower(),
            "intent": intent,
            "result": result or {},
            "datetime": datetime.now().isoformat()
        }
        
        self.conversation_history.append(entry)
        self.last_action = entry
        
        # Keep only last 20 commands to avoid memory bloat
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
        
        # Update current context
        self._update_context(entry)
    
    def _update_context(self, entry: Dict):
        """Update current context based on latest command"""
        
        command = entry["command"]
        intent = entry["intent"]
        
        # YouTube context detection
        if any(keyword in command for keyword in ["youtube", "play", "video", "music", "song"]):
            self.current_context.update({
                "domain": "youtube",
                "last_search": self._extract_search_query(command),
                "last_youtube_command": command,
                "youtube_session_active": True,
                "timestamp": entry["timestamp"]
            })
        
        # System context detection
        elif any(keyword in command for keyword in ["battery", "system", "status", "wifi"]):
            self.current_context.update({
                "domain": "system",
                "last_system_command": command,
                "timestamp": entry["timestamp"]
            })
    
    def _extract_search_query(self, command: str) -> Optional[str]:
        """Extract search query from YouTube command"""
        
        # Patterns to extract search terms
        patterns = [
            r"play\s+(.+?)\s+on\s+youtube",
            r"play\s+(.+)",
            r"search\s+for\s+(.+)",
            r"find\s+(.+)",
            r"youtube\s+(.+)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, command, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None
    
    def is_follow_up_command(self, command: str) -> bool:
        """Determine if current command is a follow-up to previous command"""
        
        if not self.last_action:
            return False
        
        # Check if command was issued within reasonable time frame (5 minutes)
        time_diff = time.time() - self.last_action["timestamp"]
        if time_diff > 300:  # 5 minutes
            return False
        
        command_lower = command.lower()
        
        # YouTube follow-up patterns
        youtube_followups = [
            "play it", "play this", "play that", "start it", "open it",
            "play the first", "first result", "first one", "top result",
            "play the video", "start the video", "click it", "select it",
            "go to first", "choose first", "pick first", "use first",
            "play first search result", "open first result"
        ]
        
        # Check for exact follow-up patterns
        for pattern in youtube_followups:
            if pattern in command_lower:
                return True
        
        # Check for contextual references
        contextual_words = ["it", "this", "that", "first", "top", "result"]
        if any(word in command_lower.split() for word in contextual_words):
            return True
        
        return False
    
    def get_enhanced_command(self, command: str) -> str:
        """Enhance follow-up command with previous context"""
        
        if not self.is_follow_up_command(command):
            return command
        
        command_lower = command.lower()
        
        # YouTube follow-up enhancement
        if self.current_context.get("domain") == "youtube":
            last_search = self.current_context.get("last_search")
            
            if last_search and any(pattern in command_lower for pattern in [
                "play it", "play this", "play that", "start it", 
                "first", "result", "open it", "click it", "select it"
            ]):
                enhanced_command = f"play {last_search} first result on youtube"
                print(f"🧠 Context Enhanced: '{command}' → '{enhanced_command}'")
                return enhanced_command
        
        return command
    
    def get_context_summary(self) -> Dict[str, Any]:
        """Get current context summary"""
        
        return {
            "current_domain": self.current_context.get("domain"),
            "last_search": self.current_context.get("last_search"),
            "youtube_active": self.current_context.get("youtube_session_active", False),
            "last_command": self.last_action["command"] if self.last_action else None,
            "commands_count": len(self.conversation_history),
            "session_duration": round(time.time() - self.session_start, 1)
        }
    
    def clear_context(self):
        """Clear current context (useful for new sessions)"""
        
        self.current_context = {}
        self.last_action = None
    
    def save_to_file(self, filepath: str):
        """Save context memory to file"""
        
        data = {
            "conversation_history": self.conversation_history,
            "current_context": self.current_context,
            "last_action": self.last_action,
            "session_start": self.session_start
        }
        
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"⚠️ Failed to save context memory: {e}")
    
    def load_from_file(self, filepath: str):
        """Load context memory from file"""
        
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            self.conversation_history = data.get("conversation_history", [])
            self.current_context = data.get("current_context", {})
            self.last_action = data.get("last_action")
            self.session_start = data.get("session_start", time.time())
            
        except Exception as e:
            print(f"⚠️ Failed to load context memory: {e}")

# Global context memory instance
_context_memory = ContextMemory()

def get_context_memory() -> ContextMemory:
    """Get global context memory instance"""
    return _context_memory

def enhance_command_with_context(command: str) -> str:
    """Main function to enhance commands with context"""
    
    context = get_context_memory()
    enhanced = context.get_enhanced_command(command)
    
    # Add to history
    context.add_command(command, "general")
    
    return enhanced

if __name__ == "__main__":
    # Test the context memory system
    print("🧪 Testing Context Memory System")
    print("=" * 40)
    
    context = ContextMemory()
    
    # Test 1: YouTube sequence
    print("\n🎵 Test 1: YouTube command sequence")
    context.add_command("play Hanuman Chalisa Gulshan Grover on YouTube", "youtube")
    print(f"Context: {context.get_context_summary()}")
    
    # Follow-up command
    follow_up = "play the first search result"
    enhanced = context.get_enhanced_command(follow_up)
    print(f"Original: '{follow_up}'")
    print(f"Enhanced: '{enhanced}'")
    print(f"Is follow-up: {context.is_follow_up_command(follow_up)}")
    
    # Test 2: Different follow-ups
    test_commands = [
        "play it",
        "start the video", 
        "click first result",
        "select first one",
        "open first result"
    ]
    
    print(f"\n🔍 Test 2: Follow-up pattern recognition")
    for cmd in test_commands:
        enhanced = context.get_enhanced_command(cmd)
        is_followup = context.is_follow_up_command(cmd)
        print(f"'{cmd}' → Enhanced: {enhanced != cmd}, Follow-up: {is_followup}")
    
    print("\n✅ Context Memory testing completed!")
