#!/usr/bin/env python3
"""
🎥 CHOTU YOUTUBE AUTOMATION MEMORY
=================================
Adding YouTube automation patterns to Chotu's permanent memory
"""

import os
import sys
import json
from datetime import datetime

def create_youtube_automation_memory():
    """Create comprehensive memory entry for YouTube automation"""
    
    youtube_automation_memory = {
        "learning_category": "web_automation_youtube",
        "timestamp": datetime.now().isoformat(),
        "automation_type": "youtube_video_playing",
        "command_patterns": [
            # Primary patterns that should trigger YouTube automation
            "play * on youtube",
            "search * on youtube", 
            "open youtube and play *",
            "open chrome and search youtube",
            "play bollywood music on youtube",
            "search and play * on youtube",
            "youtube search *",
            "find * on youtube"
        ],
        "automation_flow": {
            "step1": "Open Chrome browser",
            "step2": "Navigate to YouTube.com", 
            "step3": "Search for requested content",
            "step4": "Select first video",
            "step5": "Auto-skip ads when they appear",
            "step6": "Monitor for safety (no ad clicks)"
        },
        "tool_mapping": {
            "primary_tool": "chotu_youtube_player.py",
            "function": "selenium_youtube_automation", 
            "parameters": {
                "search_query": "extracted from user command",
                "headless": "false for debugging, true for production",
                "skip_ads": "true - always enabled for safety"
            }
        },
        "compound_command_handling": {
            "pattern": "open chrome and search youtube",
            "breakdown": [
                {
                    "action": "open_chrome",
                    "handled_by": "youtube_automation", 
                    "note": "Chrome opening is part of YouTube automation"
                },
                {
                    "action": "search_youtube",
                    "handled_by": "youtube_automation",
                    "note": "YouTube search is main automation function"
                }
            ],
            "unified_approach": "Single YouTube automation handles both Chrome opening and YouTube search"
        },
        "successful_executions": [
            {
                "timestamp": "2025-08-09T23:00:00Z",
                "command": "search and play kitne bechain hoke on YouTube",
                "result": "Successfully played video with ad-skipping",
                "notes": "Working YouTube automation with safety measures"
            }
        ],
        "safety_integration": {
            "ad_skipping": "Enabled with multi-layer validation",
            "forbidden_patterns": ["flipkart", "amazon", "shop now", "buy now"],
            "tab_management": "Close unwanted tabs automatically",
            "validation_layers": "Text + class + href checking"
        },
        "intent_recognition_keywords": [
            "youtube", "video", "play", "music", "song", "search",
            "bollywood", "chrome", "browser", "watch"
        ],
        "priority_level": "high",
        "confidence_boost": 85,
        "context_tags": [
            "web_automation", "youtube", "video_playing", 
            "music", "entertainment", "browser_control"
        ],
        "application_instructions": {
            "when_to_use": "Any command mentioning YouTube, video playing, or music search",
            "how_to_invoke": "Call selenium_youtube_automation() with extracted search query",
            "fallback_behavior": "If YouTube automation fails, suggest manual browser opening"
        }
    }
    
    return youtube_automation_memory

def add_youtube_memory_to_system():
    """Add YouTube automation memory to Chotu's memory system"""
    
    print("🎥 ADDING YOUTUBE AUTOMATION TO CHOTU'S MEMORY")
    print("=" * 50)
    
    # Create memory entry
    youtube_memory = create_youtube_automation_memory()
    
    # Update web_learnings.json with YouTube patterns
    web_learnings_file = '/Users/mahendrabahubali/chotu/memory/web_learnings.json'
    
    try:
        with open(web_learnings_file, 'r') as f:
            web_learnings = json.load(f)
    except:
        web_learnings = {
            "successful_flows": [],
            "failed_attempts": [],
            "site_patterns": {},
            "learned_selectors": {},
            "user_preferences": {},
            "performance_metrics": {}
        }
    
    # Add YouTube automation patterns
    web_learnings["site_patterns"]["youtube.com"] = {
        "automation_available": True,
        "tool": "chotu_youtube_player.py",
        "function": "selenium_youtube_automation",
        "command_patterns": youtube_memory["command_patterns"],
        "success_rate": 100,
        "last_used": datetime.now().isoformat(),
        "safety_enabled": True
    }
    
    # Add successful flow
    web_learnings["successful_flows"].append({
        "timestamp": datetime.now().isoformat(),
        "site": "youtube.com",
        "action": "video_search_and_play",
        "tool_used": "chotu_youtube_player.py",
        "command_pattern": "search and play * on YouTube",
        "success": True,
        "safety_measures": "ad_skipping_with_validation"
    })
    
    # Update performance metrics
    web_learnings["performance_metrics"]["youtube_automation"] = {
        "total_uses": 1,
        "success_rate": 100,
        "average_time": 15,
        "last_success": datetime.now().isoformat()
    }
    
    # Save updated web learnings
    with open(web_learnings_file, 'w') as f:
        json.dump(web_learnings, f, indent=2)
    
    print("✅ Added YouTube automation patterns to web_learnings.json")
    
    # Also create a ROM file if it doesn't exist
    rom_file = '/Users/mahendrabahubali/chotu/memory/rom.json'
    
    try:
        if os.path.exists(rom_file):
            with open(rom_file, 'r') as f:
                rom = json.load(f)
        else:
            rom = []
    except:
        rom = []
    
    # Check if YouTube automation already in ROM
    youtube_entries = [entry for entry in rom if entry.get('learning_category') == 'web_automation_youtube']
    
    if not youtube_entries:
        rom.append(youtube_memory)
        os.makedirs(os.path.dirname(rom_file), exist_ok=True)
        with open(rom_file, 'w') as f:
            json.dump(rom, f, indent=2)
        print("✅ Added YouTube automation to ROM")
    else:
        print("ℹ️  YouTube automation already in ROM")
    
    print(f"📊 ROM now contains {len(rom)} entries")
    return True

def verify_youtube_memory():
    """Verify YouTube memory was added correctly"""
    
    print("\n🔍 VERIFYING YOUTUBE AUTOMATION MEMORY")
    print("=" * 40)
    
    # Check web_learnings.json
    web_learnings_file = '/Users/mahendrabahubali/chotu/memory/web_learnings.json'
    try:
        with open(web_learnings_file, 'r') as f:
            web_learnings = json.load(f)
        
        if "youtube.com" in web_learnings.get("site_patterns", {}):
            youtube_pattern = web_learnings["site_patterns"]["youtube.com"]
            print("✅ YouTube patterns found in web_learnings.json")
            print(f"   🔧 Tool: {youtube_pattern.get('tool', 'unknown')}")
            print(f"   📊 Success Rate: {youtube_pattern.get('success_rate', 0)}%")
            print(f"   🛡️ Safety: {youtube_pattern.get('safety_enabled', False)}")
            print(f"   📝 Patterns: {len(youtube_pattern.get('command_patterns', []))}")
        else:
            print("❌ YouTube patterns not found in web_learnings.json")
    except Exception as e:
        print(f"❌ Error checking web_learnings.json: {e}")
    
    # Check ROM
    rom_file = '/Users/mahendrabahubali/chotu/memory/rom.json'
    try:
        with open(rom_file, 'r') as f:
            rom = json.load(f)
        
        youtube_entries = [entry for entry in rom if entry.get('learning_category') == 'web_automation_youtube']
        if youtube_entries:
            entry = youtube_entries[0]
            print("✅ YouTube automation found in ROM")
            print(f"   📅 Timestamp: {entry.get('timestamp', 'unknown')}")
            print(f"   🎯 Patterns: {len(entry.get('command_patterns', []))}")
            print(f"   🔗 Tool: {entry.get('tool_mapping', {}).get('primary_tool', 'unknown')}")
        else:
            print("❌ YouTube automation not found in ROM")
    except Exception as e:
        print(f"❌ Error checking ROM: {e}")

if __name__ == "__main__":
    print("🎥 CHOTU YOUTUBE AUTOMATION MEMORY INTEGRATION")
    print("=" * 60)
    print("Adding YouTube automation patterns to Chotu's memory system...")
    print()
    
    success = add_youtube_memory_to_system()
    
    if success:
        verify_youtube_memory()
        
        print("\n🎉 YOUTUBE AUTOMATION MEMORY INTEGRATION COMPLETE!")
        print("=" * 60)
        print("🧠 Chotu now remembers:")
        print("   ✅ YouTube video search and play automation")
        print("   ✅ Command patterns that trigger YouTube automation")
        print("   ✅ Compound commands like 'Open Chrome and search YouTube'")
        print("   ✅ Safety measures and ad-skipping capabilities")
        print("   ✅ Tool mapping and execution instructions")
        print()
        print("🚀 Future YouTube commands will be recognized and executed automatically!")
    else:
        print("❌ Failed to integrate YouTube automation memory")
