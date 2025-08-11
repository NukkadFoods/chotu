#!/usr/bin/env python3
"""
🎯 SESSION-AWARE YOUTUBE AUTOMATION 
==================================
Prevents multiple tabs and handles follow-up commands intelligently
"""

import time
import sys
import os

# Add path for imports
sys.path.insert(0, '/Users/mahendrabahubali/chotu')

def session_aware_youtube_play(query: str, enhanced_command: str = None) -> dict:
    """
    Session-aware YouTube automation that handles follow-up commands
    
    Args:
        query: The search query or command
        enhanced_command: Context-enhanced version of the command
        
    Returns:
        dict: Result of the operation
    """
    
    print(f"🎯 SESSION-AWARE YOUTUBE AUTOMATION")
    print(f"📝 Original: '{query}'")
    if enhanced_command and enhanced_command != query:
        print(f"🧠 Enhanced: '{enhanced_command}'")
    print("=" * 50)
    
    try:
        # Import context memory and YouTube handler
        from memory.context_memory import get_context_memory, enhance_command_with_context
        from utils.youtube_command_handler import process_youtube_command
        
        # Get enhanced command with context
        context_memory = get_context_memory()
        final_command = enhanced_command or enhance_command_with_context(query)
        
        print(f"🎯 Final command: '{final_command}'")
        
        # Process the YouTube command
        result = process_youtube_command(query, final_command)
        
        # Add command to context memory
        context_memory.add_command(query, "youtube", result)
        
        # Enhanced result with context info
        result.update({
            "context_enhanced": final_command != query,
            "session_aware": True,
            "original_query": query,
            "final_query": final_command
        })
        
        return result
        
    except ImportError as e:
        print(f"⚠️ Context system not available: {e}")
        print("🔄 Falling back to direct enhanced automation...")
        
        # Fallback to direct enhanced automation
        try:
            from mcp.tools.enhanced_youtube_automation import enhanced_youtube_play
            return enhanced_youtube_play(query, stop_current=False)
        except ImportError:
            print("❌ Enhanced automation also not available")
            return {
                "success": False,
                "error": "YouTube automation not available",
                "query": query
            }
    
    except Exception as e:
        print(f"❌ Session-aware automation failed: {e}")
        
        # Final fallback
        try:
            from mcp.tools.enhanced_youtube_automation import enhanced_youtube_play
            print("🔄 Using direct enhanced automation as fallback...")
            return enhanced_youtube_play(query, stop_current=False)
        except:
            return {
                "success": False,
                "error": f"All YouTube automation methods failed: {e}",
                "query": query
            }

def session_aware_youtube_stop() -> dict:
    """Stop current YouTube video with session awareness"""
    
    try:
        from mcp.tools.enhanced_youtube_automation import enhanced_youtube_stop
        return enhanced_youtube_stop()
    except:
        return {
            "success": False,
            "error": "YouTube stop not available"
        }

def session_aware_youtube_status() -> dict:
    """Get YouTube session status"""
    
    try:
        from memory.context_memory import get_context_memory
        from utils.youtube_command_handler import get_youtube_handler
        
        context = get_context_memory()
        handler = get_youtube_handler()
        
        return {
            "success": True,
            "context_summary": context.get_context_summary(),
            "session_info": handler.get_session_info()
        }
    except:
        return {
            "success": False,
            "error": "Status check not available"
        }

if __name__ == "__main__":
    # Test session-aware YouTube automation
    print("🧪 Testing Session-Aware YouTube Automation")
    print("=" * 50)
    
    # Test 1: Initial command
    print("\n🎵 Test 1: Initial YouTube command")
    result1 = session_aware_youtube_play("play Hanuman Chalisa Gulshan Grover on YouTube")
    print(f"Success: {result1.get('success')}")
    print(f"Context Enhanced: {result1.get('context_enhanced')}")
    
    time.sleep(2)
    
    # Test 2: Follow-up command
    print("\n🎵 Test 2: Follow-up command")
    result2 = session_aware_youtube_play("play the first search result")
    print(f"Success: {result2.get('success')}")
    print(f"Context Enhanced: {result2.get('context_enhanced')}")
    print(f"Final Query: {result2.get('final_query')}")
    
    # Test 3: Status check
    print("\n📊 Test 3: Session status")
    status = session_aware_youtube_status()
    print(f"Status: {status}")
    
    print("\n✅ Session-aware testing completed!")
