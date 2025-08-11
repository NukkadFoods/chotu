#!/usr/bin/env python3
"""
🧪 SIMULATE CHOTU TOOL LOADING
==============================
Simulate exactly what happens during Chotu startup
"""

import sys
import os

# Add paths
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

print("🧪 Simulating Chotu tool loading process...")
print("=" * 50)

# Import and use the dynamic loader
try:
    from mcp.dynamic_loader import DynamicToolLoader
    
    print("✅ Dynamic loader imported")
    
    # Create loader instance
    loader = DynamicToolLoader()
    print("✅ Loader instance created")
    
    # This is what happens during startup - load all tools
    print("\n🔄 Loading all tools...")
    count = loader.load_all_tools()
    print(f"🎯 Loaded {count} tools successfully")
    
except Exception as e:
    print(f"❌ Tool loading simulation failed: {e}")
    import traceback
    traceback.print_exc()

print("\n🎯 Tool loading simulation completed!")
print("If you see '⚠️ Stealth browser not available' above, that's where it's coming from!")
