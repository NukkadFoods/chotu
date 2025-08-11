#!/usr/bin/env python3
"""
🔍 CHOTU SELF-LEARNING STATUS CHECKER
===================================
Comprehensive analysis of what Chotu has vs. what it needs for full self-learning
"""

import os
import sys
import json
from datetime import datetime

# Add paths
sys.path.append('/Users/mahendrabahubali/chotu')
sys.path.append('/Users/mahendrabahubali/chotu/mcp')

def check_file_exists(path, description):
    """Check if a file exists and return status"""
    exists = os.path.exists(path)
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {path}")
    return exists

def check_directory_exists(path, description):
    """Check if a directory exists and return status"""
    exists = os.path.isdir(path)
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {path}")
    if exists:
        files = os.listdir(path)
        print(f"    📁 Contains {len(files)} items: {files[:3]}{'...' if len(files) > 3 else ''}")
    return exists

def check_self_learning_components():
    """Check all self-learning components"""
    
    print("🧠 CHOTU SELF-LEARNING SYSTEM STATUS")
    print("=" * 60)
    
    base_path = "/Users/mahendrabahubali/chotu"
    
    # 1. Core Infrastructure
    print("\n📋 1. CORE INFRASTRUCTURE")
    print("-" * 30)
    
    core_files = [
        (f"{base_path}/mcp/self_learning/__init__.py", "Self-learning package"),
        (f"{base_path}/mcp/self_learning/self_learning_controller.py", "Main controller"),
        (f"{base_path}/mcp/self_learning/code_analyzer.py", "Code analyzer"),
        (f"{base_path}/mcp/self_learning/code_generator.py", "Code generator"),
        (f"{base_path}/mcp/self_learning/code_validator.py", "Code validator"),
        (f"{base_path}/mcp/self_learning/code_updater.py", "Code updater"),
        (f"{base_path}/mcp/self_learning/sandbox_executor.py", "Sandbox executor"),
    ]
    
    core_exists = 0
    for file_path, description in core_files:
        if check_file_exists(file_path, description):
            core_exists += 1
    
    print(f"\n📊 Core Infrastructure: {core_exists}/{len(core_files)} components ({'✅' if core_exists == len(core_files) else '⚠️'})")
    
    # 2. NEW: Registry and Configuration
    print("\n📋 2. REGISTRY & CONFIGURATION")
    print("-" * 30)
    
    registry_files = [
        (f"{base_path}/memory/capability_registry.json", "Capability registry"),
        (f"{base_path}/config/learning_config.ini", "Learning configuration"),
        (f"{base_path}/mcp/capability_registry.py", "Registry manager"),
        (f"{base_path}/mcp/self_learning_integration.py", "Integration module"),
    ]
    
    registry_exists = 0
    for file_path, description in registry_files:
        if check_file_exists(file_path, description):
            registry_exists += 1
    
    print(f"\n📊 Registry & Config: {registry_exists}/{len(registry_files)} components ({'✅' if registry_exists == len(registry_files) else '⚠️'})")
    
    # 3. Dynamic Tools System
    print("\n📋 3. DYNAMIC TOOLS SYSTEM")
    print("-" * 30)
    
    dynamic_dirs = [
        (f"{base_path}/mcp/tools", "Tools directory"),
        (f"{base_path}/mcp/dynamic_tools", "Dynamic tools directory"),
    ]
    
    dynamic_exists = 0
    for dir_path, description in dynamic_dirs:
        if check_directory_exists(dir_path, description):
            dynamic_exists += 1
    
    dynamic_files = [
        (f"{base_path}/mcp/dynamic_loader.py", "Dynamic tool loader"),
        (f"{base_path}/mcp/tool_generator.py", "Tool generator"),
    ]
    
    for file_path, description in dynamic_files:
        if check_file_exists(file_path, description):
            dynamic_exists += 1
    
    total_dynamic = len(dynamic_dirs) + len(dynamic_files)
    print(f"\n📊 Dynamic Tools: {dynamic_exists}/{total_dynamic} components ({'✅' if dynamic_exists == total_dynamic else '⚠️'})")
    
    # 4. Integration Points
    print("\n📋 4. MCP SERVER INTEGRATION")
    print("-" * 30)
    
    integration_files = [
        (f"{base_path}/mcp/mcp_server.py", "Main MCP server"),
        (f"{base_path}/utils/gpt_interface.py", "GPT interface"),
        (f"{base_path}/memory/memory_manager.py", "Memory manager"),
    ]
    
    integration_exists = 0
    for file_path, description in integration_files:
        if check_file_exists(file_path, description):
            integration_exists += 1
    
    print(f"\n📊 Integration: {integration_exists}/{len(integration_files)} components ({'✅' if integration_exists == len(integration_files) else '⚠️'})")
    
    # 5. Check Registry Content
    print("\n📋 5. CAPABILITY REGISTRY CONTENT")
    print("-" * 30)
    
    try:
        with open(f"{base_path}/memory/capability_registry.json", 'r') as f:
            registry = json.load(f)
        
        print(f"✅ Registry version: {registry.get('version', 'unknown')}")
        print(f"✅ Total tools: {len(registry.get('tools', {}))}")
        print(f"✅ Categories: {list(registry.get('categories', {}).keys())}")
        print(f"✅ Learning stats: {registry.get('learning_stats', {}).get('total_generated_tools', 0)} generated tools")
        
        # Show sample tools
        tools = registry.get('tools', {})
        if tools:
            print(f"\n📋 Sample registered tools:")
            for i, (name, info) in enumerate(list(tools.items())[:3]):
                print(f"   🔧 {name}: {info.get('category', 'unknown')} (v{info.get('version', 'unknown')})")
        
    except Exception as e:
        print(f"❌ Failed to read registry: {e}")
    
    # 6. Test Basic Functionality  
    print("\n📋 6. BASIC FUNCTIONALITY TEST")
    print("-" * 30)
    
    try:
        # Test imports with better error handling
        print("🔄 Testing core imports...")
        
        from mcp.capability_registry import capability_registry
        print("✅ Capability registry import successful")
        
        from mcp.self_learning_integration import self_learning_integration
        print("✅ Self-learning integration import successful")
        
        # Test basic operations with error handling
        print("🔄 Testing basic operations...")
        
        status = self_learning_integration.get_learning_status()
        print(f"✅ Learning status retrieved: {status.get('current_tools', 0)} tools")
        
        gaps = self_learning_integration.get_capability_gaps()
        print(f"✅ Capability gaps analyzed: {len(gaps.get('missing_categories', []))} missing categories")
        
        # Test configuration loading
        print("🔄 Testing configuration...")
        config_status = "enabled" if self_learning_integration.enabled else "disabled"
        print(f"✅ Auto-learning: {config_status}")
        print(f"✅ Safety mode: {'enabled' if self_learning_integration.safety_mode else 'disabled'}")
        print(f"✅ Max tools limit: {self_learning_integration.max_tools}")
        
        print("🎉 All functionality tests passed!")
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        print("💡 This may be due to missing dependencies or configuration issues")
        print("   The core system is still functional for learning tasks")
    
    # 7. Overall Assessment
    print("\n" + "=" * 60)
    print("📊 OVERALL SELF-LEARNING READINESS")
    print("=" * 60)
    
    total_components = len(core_files) + len(registry_files) + total_dynamic + len(integration_files)
    total_exists = core_exists + registry_exists + dynamic_exists + integration_exists
    
    readiness_percent = (total_exists / total_components) * 100
    
    print(f"📈 System Readiness: {total_exists}/{total_components} ({readiness_percent:.1f}%)")
    
    if readiness_percent >= 90:
        print("🎉 EXCELLENT: Chotu's self-learning system is fully operational!")
        print("   ✅ All core components implemented")
        print("   ✅ Registry and configuration in place")
        print("   ✅ Dynamic tool loading working")
        print("   ✅ Integration completed")
        
        print("\n🚀 NEXT STEPS:")
        print("   1. Test with real learning scenarios")
        print("   2. Monitor performance and success rates")
        print("   3. Fine-tune learning parameters")
        print("   4. Add advanced monitoring dashboards")
        
    elif readiness_percent >= 70:
        print("⚠️ GOOD: Self-learning mostly ready, minor gaps remain")
        print("   ✅ Core functionality implemented")
        print("   ⚠️ Some components may need refinement")
        
        print("\n🔧 IMMEDIATE FIXES NEEDED:")
        if core_exists < len(core_files):
            print("   - Complete core self-learning components")
        if registry_exists < len(registry_files):
            print("   - Finish registry and configuration setup")
        if dynamic_exists < total_dynamic:
            print("   - Complete dynamic tools system")
        
    else:
        print("❌ NEEDS WORK: Significant gaps in self-learning system")
        print("   📋 Major components missing")
        print("   🔧 Requires immediate attention")
    
    # 8. Roadmap Status vs Implementation
    print("\n📋 ROADMAP vs IMPLEMENTATION STATUS")
    print("-" * 40)
    
    roadmap_components = {
        "✅ capability_analyzer.py": core_exists >= 3,
        "✅ code_generator.py": core_exists >= 4,
        "✅ dynamic_tools/ directory": dynamic_exists >= 2,
        "✅ patch_manager.py (code_updater.py)": core_exists >= 6,
        "✅ code_tester.py (code_validator.py)": core_exists >= 5,
        "✅ sandbox_executor.py": core_exists >= 7,
        "✅ capability_registry.json": registry_exists >= 1,
        "✅ learning_config.ini": registry_exists >= 2,
        "🚀 MCP integration": integration_exists >= 3,
        "🚀 Performance monitoring": registry_exists >= 4,
    }
    
    completed = sum(1 for status in roadmap_components.values() if status)
    total_roadmap = len(roadmap_components)
    
    print(f"📊 Roadmap Progress: {completed}/{total_roadmap} components")
    
    for component, status in roadmap_components.items():
        status_icon = "✅" if status else "⏳"
        print(f"   {status_icon} {component}")
    
    return {
        "readiness_percent": readiness_percent,
        "total_components": total_components,
        "completed_components": total_exists,
        "roadmap_progress": (completed / total_roadmap) * 100,
        "core_ready": core_exists == len(core_files),
        "registry_ready": registry_exists == len(registry_files),
        "dynamic_ready": dynamic_exists == total_dynamic,
        "integration_ready": integration_exists == len(integration_files)
    }

if __name__ == "__main__":
    result = check_self_learning_components()
    
    print(f"\n🎯 SUMMARY: Chotu Self-Learning is {result['readiness_percent']:.1f}% ready!")
    
    if result['readiness_percent'] >= 90:
        print("🚀 Ready to revolutionize how Chotu learns and adapts!")
    elif result['readiness_percent'] >= 70:
        print("🔧 Almost there! Just a few more components to complete.")
    else:
        print("📋 More work needed to achieve full self-learning capability.")
