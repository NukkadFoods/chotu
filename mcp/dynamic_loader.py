#!/usr/bin/env python3
"""
🔄 DYNAMIC TOOL LOADER
=====================
Automatically discovers and loads all tools from the tools/ directory
"""

import os
import importlib
import importlib.util
from typing import Dict, Any

class DynamicToolLoader:
    """Dynamically loads and manages tools"""
    
    def __init__(self, tools_directory=None):
        if tools_directory is None:
            # Auto-detect tools directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.tools_dir = os.path.join(current_dir, "tools")
        else:
            self.tools_dir = tools_directory
        self.loaded_tools = {}
        self.tool_functions = {}
        
    def discover_tools(self):
        """Discover all Python files in tools directory"""
        tools = []
        if not os.path.exists(self.tools_dir):
            print(f"⚠️ Tools directory not found: {self.tools_dir}")
            return tools
            
        for file in os.listdir(self.tools_dir):
            if file.endswith('.py') and not file.startswith('__'):
                tool_name = file[:-3]  # Remove .py extension
                tools.append(tool_name)
        
        return tools
    
    def load_tool_module(self, tool_name):
        """Load a specific tool module"""
        try:
            file_path = f"{self.tools_dir}/{tool_name}.py"
            
            if not os.path.exists(file_path):
                print(f"❌ Tool file not found: {file_path}")
                return None
            
            spec = importlib.util.spec_from_file_location(tool_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            self.loaded_tools[tool_name] = module
            
            # Extract functions from the module
            functions = {}
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if callable(attr) and not attr_name.startswith('_'):
                    functions[attr_name] = attr
            
            self.tool_functions[tool_name] = functions
            print(f"✅ Loaded tool: {tool_name} with {len(functions)} functions")
            return module
            
        except Exception as e:
            print(f"❌ Failed to load tool {tool_name}: {e}")
            return None
    
    def load_all_tools(self):
        """Load all available tools"""
        print("🔄 Loading all tools...")
        
        # Clear existing tools
        self.loaded_tools.clear()
        self.tool_functions.clear()
        
        # Clear import cache
        importlib.invalidate_caches()
        
        tools = self.discover_tools()
        loaded_count = 0
        
        for tool_name in tools:
            if self.load_tool_module(tool_name):
                loaded_count += 1
        
        print(f"🎯 Loaded {loaded_count} tools successfully")
        return loaded_count
    
    def get_tool_function(self, tool_name, function_name):
        """Get a specific function from a tool"""
        if tool_name in self.tool_functions:
            return self.tool_functions[tool_name].get(function_name)
        return None
    
    def get_all_capabilities(self):
        """Get a list of all available capabilities"""
        capabilities = {}
        
        for tool_name, functions in self.tool_functions.items():
            capabilities[tool_name] = list(functions.keys())
        
        return capabilities
    
    def find_function_by_pattern(self, pattern):
        """Find functions that match a pattern"""
        matches = []
        pattern_lower = pattern.lower()
        
        for tool_name, functions in self.tool_functions.items():
            for func_name in functions:
                if pattern_lower in func_name.lower():
                    matches.append((tool_name, func_name))
        
        return matches
    
    def reload_specific_tool(self, tool_name):
        """Reload a specific tool (useful after updates)"""
        print(f"🔄 Reloading tool: {tool_name}")
        
        # Remove from cache if exists
        if tool_name in self.loaded_tools:
            del self.loaded_tools[tool_name]
        if tool_name in self.tool_functions:
            del self.tool_functions[tool_name]
        
        # Clear import cache
        importlib.invalidate_caches()
        
        # Reload
        return self.load_tool_module(tool_name)

# Global instance
tool_loader = DynamicToolLoader()
