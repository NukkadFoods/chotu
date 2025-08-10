#!/usr/bin/env python3
"""
📋 SCHEMA MANAGER
================
Manages the macOS schema file with automatic updates for:
- Dependency tracking
- Tool installation/removal
- System capability changes
"""

import json
import subprocess
import os
from typing import Dict, List, Any
from datetime import datetime

class SchemaManager:
    """Manages and updates the macOS schema dynamically"""
    
    def __init__(self, schema_path: str = "/Users/mahendrabahubali/chotu/macos_schema.json"):
        self.schema_path = schema_path
        self.schema = self._load_schema()
    
    def _load_schema(self) -> Dict:
        """Load the current schema"""
        try:
            with open(self.schema_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Could not load schema: {e}")
            return {}
    
    def _save_schema(self):
        """Save the updated schema"""
        try:
            # Update last modified timestamp
            self.schema["last_updated"] = datetime.now().strftime("%Y-%m-%d")
            
            with open(self.schema_path, 'w') as f:
                json.dump(self.schema, f, indent=2)
            print(f"📋 Schema updated: {self.schema_path}")
        except Exception as e:
            print(f"❌ Failed to save schema: {e}")
    
    def add_python_package(self, package_name: str, version: str = None):
        """Add a Python package to the schema"""
        if "installed_dependencies" not in self.schema:
            self.schema["installed_dependencies"] = {"python_packages": []}
        
        packages = self.schema["installed_dependencies"]["python_packages"]
        
        # Remove if already exists (to update)
        packages = [p for p in packages if not p.startswith(package_name)]
        
        # Add new entry
        if version:
            packages.append(f"{package_name}=={version}")
        else:
            packages.append(package_name)
        
        self.schema["installed_dependencies"]["python_packages"] = packages
        self._save_schema()
        print(f"📦 Added Python package: {package_name}")
    
    def remove_python_package(self, package_name: str):
        """Remove a Python package from the schema"""
        if "installed_dependencies" not in self.schema:
            return
        
        packages = self.schema["installed_dependencies"]["python_packages"]
        original_count = len(packages)
        
        # Remove package (handles versioned entries too)
        packages = [p for p in packages if not p.split('==')[0] == package_name]
        
        self.schema["installed_dependencies"]["python_packages"] = packages
        
        if len(packages) < original_count:
            self._save_schema()
            print(f"🗑️ Removed Python package: {package_name}")
        else:
            print(f"⚠️ Package not found: {package_name}")
    
    def add_system_tool(self, tool_name: str, install_command: str = None):
        """Add a system tool to the schema"""
        if "installed_dependencies" not in self.schema:
            self.schema["installed_dependencies"] = {"system_tools": []}
        
        tools = self.schema["installed_dependencies"]["system_tools"]
        
        if tool_name not in tools:
            tools.append(tool_name)
            self.schema["installed_dependencies"]["system_tools"] = tools
            
            # Also track how it was installed
            if install_command:
                if "installation_commands" not in self.schema:
                    self.schema["installation_commands"] = {}
                self.schema["installation_commands"][tool_name] = install_command
            
            self._save_schema()
            print(f"🔧 Added system tool: {tool_name}")
    
    def remove_system_tool(self, tool_name: str):
        """Remove a system tool from the schema"""
        if "installed_dependencies" not in self.schema:
            return
        
        tools = self.schema["installed_dependencies"]["system_tools"]
        
        if tool_name in tools:
            tools.remove(tool_name)
            self.schema["installed_dependencies"]["system_tools"] = tools
            
            # Remove installation command if exists
            if "installation_commands" in self.schema and tool_name in self.schema["installation_commands"]:
                del self.schema["installation_commands"][tool_name]
            
            self._save_schema()
            print(f"🗑️ Removed system tool: {tool_name}")
        else:
            print(f"⚠️ Tool not found: {tool_name}")
    
    def update_system_info(self):
        """Update system information in the schema"""
        print("🔄 Updating system information...")
        
        try:
            # Update Python version
            result = subprocess.run(["python3", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                python_version = result.stdout.strip().split()[-1]
                self.schema["system_info"]["python_version"] = python_version
            
            # Update macOS version
            result = subprocess.run(["sw_vers", "-productVersion"], capture_output=True, text=True)
            if result.returncode == 0:
                macos_version = result.stdout.strip()
                self.schema["system_info"]["version"] = macos_version
            
            # Update build version
            result = subprocess.run(["sw_vers", "-buildVersion"], capture_output=True, text=True)
            if result.returncode == 0:
                build_version = result.stdout.strip()
                self.schema["system_info"]["build_version"] = build_version
            
            self._save_schema()
            print("✅ System information updated")
            
        except Exception as e:
            print(f"❌ Failed to update system info: {e}")
    
    def verify_dependencies(self):
        """Verify that listed dependencies are actually installed"""
        print("🔍 Verifying dependencies...")
        
        # Check Python packages
        if "python_packages" in self.schema.get("installed_dependencies", {}):
            verified_packages = []
            for package in self.schema["installed_dependencies"]["python_packages"]:
                package_name = package.split('==')[0]
                try:
                    result = subprocess.run(
                        ["pip", "show", package_name], 
                        capture_output=True, 
                        text=True
                    )
                    if result.returncode == 0:
                        verified_packages.append(package)
                        print(f"  ✅ {package_name}")
                    else:
                        print(f"  ❌ {package_name} - not installed")
                except:
                    print(f"  ❌ {package_name} - verification failed")
            
            self.schema["installed_dependencies"]["python_packages"] = verified_packages
        
        # Check system tools
        if "system_tools" in self.schema.get("installed_dependencies", {}):
            verified_tools = []
            for tool in self.schema["installed_dependencies"]["system_tools"]:
                try:
                    result = subprocess.run(
                        ["which", tool], 
                        capture_output=True, 
                        text=True
                    )
                    if result.returncode == 0:
                        verified_tools.append(tool)
                        print(f"  ✅ {tool}")
                    else:
                        print(f"  ❌ {tool} - not found")
                except:
                    print(f"  ❌ {tool} - verification failed")
            
            self.schema["installed_dependencies"]["system_tools"] = verified_tools
        
        self._save_schema()
        print("✅ Dependency verification complete")
    
    def add_generated_tool(self, tool_name: str, tool_path: str, capabilities: List[str]):
        """Add a generated tool to the schema"""
        if "generated_tools" not in self.schema:
            self.schema["generated_tools"] = {}
        
        self.schema["generated_tools"][tool_name] = {
            "path": tool_path,
            "capabilities": capabilities,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "active"
        }
        
        self._save_schema()
        print(f"🤖 Added generated tool: {tool_name}")
    
    def remove_generated_tool(self, tool_name: str):
        """Remove a generated tool from the schema"""
        if "generated_tools" in self.schema and tool_name in self.schema["generated_tools"]:
            del self.schema["generated_tools"][tool_name]
            self._save_schema()
            print(f"🗑️ Removed generated tool: {tool_name}")
    
    def get_available_commands(self, category: str = None) -> Dict:
        """Get available commands from schema"""
        if category:
            return self.schema.get("macos_commands", {}).get(category, {})
        else:
            return self.schema.get("macos_commands", {})
    
    def add_command(self, category: str, command_name: str, command_path: str):
        """Add a new command to the schema"""
        if "macos_commands" not in self.schema:
            self.schema["macos_commands"] = {}
        
        if category not in self.schema["macos_commands"]:
            self.schema["macos_commands"][category] = {}
        
        self.schema["macos_commands"][category][command_name] = command_path
        self._save_schema()
        print(f"⚡ Added command: {category}.{command_name}")
    
    def get_schema_summary(self) -> Dict:
        """Get a summary of the current schema"""
        summary = {
            "version": self.schema.get("schema_version", "unknown"),
            "last_updated": self.schema.get("last_updated", "unknown"),
            "python_packages": len(self.schema.get("installed_dependencies", {}).get("python_packages", [])),
            "system_tools": len(self.schema.get("installed_dependencies", {}).get("system_tools", [])),
            "command_categories": len(self.schema.get("macos_commands", {})),
            "generated_tools": len(self.schema.get("generated_tools", {}))
        }
        return summary

# Usage example
if __name__ == "__main__":
    manager = SchemaManager()
    
    print("📋 Schema Summary:")
    summary = manager.get_schema_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    # Example operations
    print("\n🔧 Testing schema updates...")
    manager.verify_dependencies()
    manager.update_system_info()
