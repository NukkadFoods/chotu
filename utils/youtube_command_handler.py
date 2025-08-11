#!/usr/bin/env python3
"""
🎯 CHOTU YOUTUBE COMMAND HANDLER
===============================
Intelligent YouTube command processing with context awareness
"""

import re
import time
from typing import Dict, Any, Tuple, Optional

class YouTubeCommandHandler:
    """Handles YouTube commands with context awareness and session management"""
    
    def __init__(self):
        self.session_active = False
        self.current_video_info = None
        self.last_search_query = None
        self.browser_tab_count = 0
        
    def parse_youtube_command(self, command: str, enhanced_command: str = None) -> Dict[str, Any]:
        """Parse YouTube command and determine the appropriate action"""
        
        # Use enhanced command if available (from context memory)
        working_command = enhanced_command or command
        command_lower = working_command.lower()
        
        print(f"🎯 Parsing YouTube command: '{working_command}'")
        
        # Determine action type
        action = self._determine_action(command_lower)
        
        # Extract search query
        search_query = self._extract_search_query(command_lower, action)
        
        # Determine session strategy
        session_strategy = self._determine_session_strategy(command_lower, action)
        
        return {
            "action": action,
            "search_query": search_query,
            "session_strategy": session_strategy,
            "original_command": command,
            "enhanced_command": enhanced_command,
            "confidence": self._calculate_confidence(command_lower, action, search_query)
        }
    
    def _determine_action(self, command: str) -> str:
        """Determine what YouTube action to take"""
        
        # Stop/pause actions
        if any(word in command for word in ["stop", "pause", "halt", "end"]):
            return "stop"
        
        # Play specific result actions
        if any(pattern in command for pattern in [
            "first result", "first one", "top result", "first video",
            "play first", "click first", "select first", "open first"
        ]):
            return "play_first_result"
        
        # General play actions
        if any(word in command for word in ["play", "start", "open", "watch"]):
            return "play"
        
        # Search actions
        if any(word in command for word in ["search", "find", "look for"]):
            return "search"
        
        # Default to play for YouTube context
        return "play"
    
    def _extract_search_query(self, command: str, action: str) -> Optional[str]:
        """Extract search query from command"""
        
        # For first result commands, use last search query if available
        if action == "play_first_result" and self.last_search_query:
            print(f"🔄 Using previous search query: '{self.last_search_query}'")
            return self.last_search_query
        
        # Common extraction patterns
        patterns = [
            # "play X on youtube"
            r"play\s+(.+?)\s+on\s+youtube",
            r"play\s+(.+?)\s+youtube",
            
            # "search for X"
            r"search\s+(?:for\s+)?(.+)",
            r"find\s+(.+)",
            r"look\s+for\s+(.+)",
            
            # "play X" (general)
            r"play\s+(.+)",
            r"start\s+(.+)",
            r"open\s+(.+)",
            r"watch\s+(.+)",
            
            # YouTube specific
            r"youtube\s+(.+)",
            r"on\s+youtube\s+(.+)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, command, re.IGNORECASE)
            if match:
                query = match.group(1).strip()
                
                # Clean up the query
                query = self._clean_search_query(query)
                
                if query and len(query) > 2:  # Valid query
                    self.last_search_query = query  # Store for follow-ups
                    return query
        
        return None
    
    def _clean_search_query(self, query: str) -> str:
        """Clean and normalize search query"""
        
        # Remove common YouTube-related words at the end
        cleanup_patterns = [
            r"\s+on\s+youtube$",
            r"\s+youtube$", 
            r"\s+video$",
            r"\s+song$",
            r"\s+music$"
        ]
        
        cleaned = query
        for pattern in cleanup_patterns:
            cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)
        
        # Remove extra whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
        return cleaned
    
    def _determine_session_strategy(self, command: str, action: str) -> str:
        """Determine how to handle browser session"""
        
        # If explicitly asking for first result, use same tab
        if action == "play_first_result":
            return "same_tab"
        
        # If we have active session and it's a new search, decide based on context
        if self.session_active:
            # Check for "stop current" indicators
            if any(phrase in command for phrase in [
                "stop current", "stop this", "new video", "different video"
            ]):
                return "stop_and_new"
            
            # Default: use same tab to avoid multiple tabs
            return "same_tab"
        
        # No active session - create new
        return "new_session"
    
    def _calculate_confidence(self, command: str, action: str, search_query: Optional[str]) -> float:
        """Calculate confidence score for command interpretation"""
        
        confidence = 0.5  # Base confidence
        
        # Action confidence
        if action in ["play", "search"]:
            confidence += 0.3
        elif action == "stop":
            confidence += 0.4
        elif action == "play_first_result":
            confidence += 0.4
        
        # Query confidence
        if search_query:
            if len(search_query) > 10:
                confidence += 0.2
            elif len(search_query) > 5:
                confidence += 0.1
        
        # YouTube-specific terms
        if "youtube" in command:
            confidence += 0.2
        
        # Clear intent words
        clear_words = ["play", "search", "find", "watch", "video", "music", "song"]
        if any(word in command for word in clear_words):
            confidence += 0.1
        
        return min(1.0, confidence)
    
    def execute_youtube_command(self, parsed_command: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the parsed YouTube command"""
        
        action = parsed_command["action"]
        search_query = parsed_command["search_query"] 
        session_strategy = parsed_command["session_strategy"]
        
        print(f"🎬 Executing YouTube action: {action}")
        print(f"🔍 Search query: {search_query}")
        print(f"🏷️ Session strategy: {session_strategy}")
        
        try:
            # Import the enhanced automation
            from mcp.tools.enhanced_youtube_automation import enhanced_youtube_play, enhanced_youtube_stop, enhanced_youtube_status
            
            if action == "stop":
                result = enhanced_youtube_stop()
                self.session_active = False
                
            elif action in ["play", "search", "play_first_result"]:
                if not search_query:
                    return {
                        "success": False,
                        "error": "No search query found in command",
                        "suggestion": "Try: 'play [song/video name] on YouTube'"
                    }
                
                # Determine if we should stop current video
                stop_current = (session_strategy in ["stop_and_new", "new_session"])
                
                result = enhanced_youtube_play(search_query, stop_current=stop_current)
                
                if result.get("success"):
                    self.session_active = True
                    self.current_video_info = {
                        "query": search_query,
                        "title": result.get("video_title"),
                        "url": result.get("url"),
                        "timestamp": time.time()
                    }
            
            else:
                return {
                    "success": False,
                    "error": f"Unknown action: {action}"
                }
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": f"YouTube automation failed: {e}",
                "fallback_available": True
            }
    
    def get_session_info(self) -> Dict[str, Any]:
        """Get current YouTube session information"""
        
        return {
            "session_active": self.session_active,
            "current_video": self.current_video_info,
            "last_search": self.last_search_query,
            "browser_tabs": self.browser_tab_count
        }

# Global YouTube handler instance
_youtube_handler = YouTubeCommandHandler()

def get_youtube_handler() -> YouTubeCommandHandler:
    """Get global YouTube command handler"""
    return _youtube_handler

def process_youtube_command(command: str, enhanced_command: str = None) -> Dict[str, Any]:
    """Main function to process YouTube commands"""
    
    handler = get_youtube_handler()
    
    # Parse the command
    parsed = handler.parse_youtube_command(command, enhanced_command)
    
    # Execute the command
    result = handler.execute_youtube_command(parsed)
    
    # Add parsing info to result
    result.update({
        "parsed_command": parsed,
        "session_info": handler.get_session_info()
    })
    
    return result

if __name__ == "__main__":
    # Test the YouTube command handler
    print("🧪 Testing YouTube Command Handler")
    print("=" * 40)
    
    handler = YouTubeCommandHandler()
    
    test_commands = [
        "play Hanuman Chalisa Gulshan Grover on YouTube",
        "play the first search result",
        "search for cricket highlights",
        "stop the current video",
        "play some music",
        "find Kasoor movie songs"
    ]
    
    for i, cmd in enumerate(test_commands, 1):
        print(f"\n🔍 Test {i}: '{cmd}'")
        parsed = handler.parse_youtube_command(cmd)
        
        print(f"   Action: {parsed['action']}")
        print(f"   Query: {parsed['search_query']}")
        print(f"   Strategy: {parsed['session_strategy']}")
        print(f"   Confidence: {parsed['confidence']:.2f}")
    
    print("\n✅ YouTube Command Handler testing completed!")
