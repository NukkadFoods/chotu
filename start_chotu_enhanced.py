#!/usr/bin/env python3
"""
🚀 CHOTU ENHANCED LAUNCHER
=========================
Launch Chotu with all enhanced features working properly
"""

import sys
import os

# Fix import paths
base_path = "/Users/mahendrabahubali/chotu"
sys.path.insert(0, base_path)
sys.path.insert(0, f"{base_path}/mcp")
sys.path.insert(0, f"{base_path}/mcp/tools")
sys.path.insert(0, f"{base_path}/utils")
sys.path.insert(0, f"{base_path}/memory")

def main():
    print("🚀 Starting Enhanced Chotu with All Features")
    print("=" * 50)
    
    # Verify enhanced features
    try:
        from mcp.tools.enhanced_youtube_automation import enhanced_youtube_play
        print("✅ Enhanced YouTube automation ready")
    except Exception as e:
        print(f"⚠️ Enhanced YouTube issue: {e}")
    
    try:
        from mcp.tools.stealth_browser import create_stealth_driver
        print("✅ Stealth browser ready")
    except Exception as e:
        print(f"⚠️ Stealth browser issue: {e}")
    
    # Import and start the main Chotu
    print("\n🤖 Starting Chotu AI Agent...")
    
    try:
        # Import the main Chotu module
        import importlib.util
        spec = importlib.util.spec_from_file_location("chotu_main", f"{base_path}/chotu.py")
        chotu_main = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(chotu_main)
        
        # Start Chotu
        chotu_main.main()
        
    except KeyboardInterrupt:
        print("\n👋 Chotu shutdown by user")
    except Exception as e:
        print(f"❌ Chotu startup failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
