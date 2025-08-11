#!/usr/bin/env python3
"""
🔧 CHOTU IMPORT FIXER
====================
Fix import issues and enable enhanced automation
"""

import sys
import os

def fix_chotu_imports():
    """Fix import paths for Chotu enhanced features"""
    
    print("🔧 Fixing Chotu import paths...")
    
    # Add all necessary paths
    base_path = "/Users/mahendrabahubali/chotu"
    
    paths_to_add = [
        base_path,
        f"{base_path}/mcp",
        f"{base_path}/mcp/tools", 
        f"{base_path}/utils",
        f"{base_path}/memory"
    ]
    
    for path in paths_to_add:
        if path not in sys.path:
            sys.path.insert(0, path)
            print(f"✅ Added to path: {path}")
    
    # Test imports with comprehensive checking
    success = True
    
    try:
        print("🧪 Testing enhanced YouTube automation...")
        from mcp.tools.enhanced_youtube_automation import enhanced_youtube_play
        print("✅ Enhanced YouTube automation import successful")
    except Exception as e:
        print(f"❌ Enhanced YouTube import failed: {e}")
        success = False
    
    try:
        print("🧪 Testing stealth browser integration...")
        from mcp.tools.enhanced_youtube_automation import STEALTH_AVAILABLE
        if STEALTH_AVAILABLE:
            print("✅ Stealth browser integration working")
        else:
            print("ℹ️ Stealth browser not available (optional)")
    except Exception as e:
        print(f"❌ Stealth browser check failed: {e}")
        success = False
    
    try:
        print("🧪 Testing session-aware YouTube...")
        from mcp.tools.session_aware_youtube import session_aware_youtube_play
        print("✅ Session-aware YouTube system available")
    except Exception as e:
        print(f"❌ Session-aware import failed: {e}")
        success = False
    
    return success

def test_stealth_browser():
    """Test stealth browser availability"""
    try:
        # Try multiple import paths
        try:
            from mcp.tools.stealth_browser import create_stealth_driver
            print("✅ Stealth browser available via mcp.tools")
            return True
        except ImportError:
            from stealth_browser import create_stealth_driver
            print("✅ Stealth browser available via direct import")
            return True
    except Exception as e:
        print(f"❌ Stealth browser not available: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Chotu Import Diagnostics")
    print("=" * 50)
    
    success1 = fix_chotu_imports()
    success2 = test_stealth_browser()
    
    if success1 and success2:
        print("\n🎉 All imports fixed! Enhanced automation ready!")
    else:
        print("\n⚠️ Some issues remain. Check error messages above.")
