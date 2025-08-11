#!/usr/bin/env python3
"""
📊 CAPABILITY REGISTRY MANAGER
============================
Manages the capability registry with version tracking, dependency mapping, and statistics
"""

import json
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path

class CapabilityRegistry:
    """Manages Chotu's capability registry and tool metadata"""
    
    def __init__(self):
        self.registry_path = "/Users/mahendrabahubali/chotu/memory/capability_registry.json"
        self.tools_dir = "/Users/mahendrabahubali/chotu/mcp/tools"
        self.registry = self._load_registry()
        
    def _load_registry(self) -> Dict:
        """Load the capability registry"""
        try:
            if os.path.exists(self.registry_path):
                with open(self.registry_path, 'r') as f:
                    return json.load(f)
            else:
                return self._create_empty_registry()
        except Exception as e:
            print(f"⚠️ Failed to load registry: {e}")
            return self._create_empty_registry()
    
    def _create_empty_registry(self) -> Dict:
        """Create an empty registry structure"""
        return {
            "version": "1.0.0",
            "last_updated": datetime.now().isoformat(),
            "tools": {},
            "categories": {},
            "learning_stats": {
                "total_generated_tools": 0,
                "successful_generations": 0,
                "failed_generations": 0,
                "success_rate": 0,
                "last_learning_session": None,
                "average_generation_time": 0,
                "most_requested_category": None
            },
            "system_health": {
                "total_tools": 0,
                "active_tools": 0,
                "broken_tools": 0,
                "last_health_check": datetime.now().isoformat(),
                "memory_usage": "normal",
                "disk_usage": "normal"
            }
        }
    
    def save_registry(self):
        """Save the registry to disk"""
        try:
            self.registry["last_updated"] = datetime.now().isoformat()
            with open(self.registry_path, 'w') as f:
                json.dump(self.registry, f, indent=2)
        except Exception as e:
            print(f"⚠️ Failed to save registry: {e}")
    
    def register_tool(self, tool_name: str, tool_info: Dict) -> bool:
        """Register a new tool in the registry"""
        try:
            tool_entry = {
                "module": tool_info.get("module", f"tools/{tool_name}.py"),
                "version": tool_info.get("version", "1.0.0"),
                "category": tool_info.get("category", "utility"),
                "dependencies": tool_info.get("dependencies", []),
                "capabilities": tool_info.get("capabilities", []),
                "auto_generated": tool_info.get("auto_generated", True),
                "created_at": datetime.now().isoformat(),
                "last_tested": None,
                "success_rate": 0.0,
                "usage_count": 0,
                "description": tool_info.get("description", ""),
                "safety_level": tool_info.get("safety_level", "safe")
            }
            
            self.registry["tools"][tool_name] = tool_entry
            self._update_category_stats(tool_entry["category"])
            self._update_system_health()
            self.save_registry()
            
            print(f"✅ Tool '{tool_name}' registered successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to register tool '{tool_name}': {e}")
            return False
    
    def update_tool_stats(self, tool_name: str, success: bool, execution_time: float = 0):
        """Update tool usage statistics"""
        if tool_name not in self.registry["tools"]:
            print(f"⚠️ Tool '{tool_name}' not found in registry")
            return
        
        tool = self.registry["tools"][tool_name]
        tool["usage_count"] += 1
        tool["last_tested"] = datetime.now().isoformat()
        
        # Update success rate
        current_rate = tool.get("success_rate", 0.0)
        usage_count = tool["usage_count"]
        
        if success:
            new_rate = ((current_rate * (usage_count - 1)) + 100) / usage_count
        else:
            new_rate = (current_rate * (usage_count - 1)) / usage_count
        
        tool["success_rate"] = round(new_rate, 2)
        
        # Update category stats
        self._update_category_stats(tool["category"])
        self.save_registry()
    
    def get_tool_info(self, tool_name: str) -> Optional[Dict]:
        """Get information about a specific tool"""
        return self.registry["tools"].get(tool_name)
    
    def get_tools_by_category(self, category: str) -> List[str]:
        """Get all tools in a specific category"""
        return [
            name for name, info in self.registry["tools"].items()
            if info.get("category") == category
        ]
    
    def get_capabilities(self) -> Dict[str, List[str]]:
        """Get all capabilities mapped by tool"""
        capabilities = {}
        for tool_name, tool_info in self.registry["tools"].items():
            capabilities[tool_name] = tool_info.get("capabilities", [])
        return capabilities
    
    def find_tools_with_capability(self, capability: str) -> List[str]:
        """Find all tools that have a specific capability"""
        matches = []
        for tool_name, tool_info in self.registry["tools"].items():
            if capability.lower() in [cap.lower() for cap in tool_info.get("capabilities", [])]:
                matches.append(tool_name)
        return matches
    
    def get_dependency_map(self) -> Dict[str, List[str]]:
        """Get dependency mapping for all tools"""
        dependencies = {}
        for tool_name, tool_info in self.registry["tools"].items():
            deps = tool_info.get("dependencies", [])
            if deps:
                dependencies[tool_name] = deps
        return dependencies
    
    def check_broken_tools(self) -> List[str]:
        """Check for tools that might be broken"""
        broken = []
        current_time = datetime.now()
        
        for tool_name, tool_info in self.registry["tools"].items():
            # Check if tool file exists
            module_path = tool_info.get("module", "")
            full_path = os.path.join("/Users/mahendrabahubali/chotu/mcp", module_path)
            
            if not os.path.exists(full_path):
                broken.append(tool_name)
                continue
            
            # Check success rate
            success_rate = tool_info.get("success_rate", 0)
            usage_count = tool_info.get("usage_count", 0)
            
            if usage_count > 5 and success_rate < 50:
                broken.append(tool_name)
        
        return broken
    
    def get_learning_recommendations(self) -> Dict[str, Any]:
        """Get recommendations for what to learn next"""
        recommendations = {
            "missing_categories": [],
            "low_performing_tools": [],
            "high_demand_capabilities": [],
            "suggested_improvements": []
        }
        
        # Find categories with no tools
        common_categories = ["system_control", "file_operations", "communication", "media", "development"]
        existing_categories = set(tool["category"] for tool in self.registry["tools"].values())
        recommendations["missing_categories"] = [cat for cat in common_categories if cat not in existing_categories]
        
        # Find low-performing tools
        for tool_name, tool_info in self.registry["tools"].items():
            if tool_info.get("usage_count", 0) > 3 and tool_info.get("success_rate", 0) < 70:
                recommendations["low_performing_tools"].append({
                    "tool": tool_name,
                    "success_rate": tool_info.get("success_rate", 0),
                    "usage_count": tool_info.get("usage_count", 0)
                })
        
        return recommendations
    
    def _update_category_stats(self, category: str):
        """Update statistics for a category"""
        if "categories" not in self.registry:
            self.registry["categories"] = {}
        
        if category not in self.registry["categories"]:
            self.registry["categories"][category] = {
                "total_tools": 0,
                "success_rate": 0,
                "last_updated": None
            }
        
        # Count tools in category
        category_tools = self.get_tools_by_category(category)
        self.registry["categories"][category]["total_tools"] = len(category_tools)
        
        # Calculate average success rate
        if category_tools:
            total_success = sum(
                self.registry["tools"][tool].get("success_rate", 0)
                for tool in category_tools
            )
            avg_success = total_success / len(category_tools)
            self.registry["categories"][category]["success_rate"] = round(avg_success, 2)
        
        self.registry["categories"][category]["last_updated"] = datetime.now().isoformat()
    
    def _update_system_health(self):
        """Update overall system health metrics"""
        health = self.registry["system_health"]
        
        total_tools = len(self.registry["tools"])
        broken_tools = self.check_broken_tools()
        active_tools = total_tools - len(broken_tools)
        
        health.update({
            "total_tools": total_tools,
            "active_tools": active_tools,
            "broken_tools": len(broken_tools),
            "last_health_check": datetime.now().isoformat()
        })
        
        # Update memory and disk usage (simplified)
        # In a full implementation, this would check actual system resources
        if total_tools > 100:
            health["memory_usage"] = "high"
        elif total_tools > 50:
            health["memory_usage"] = "medium"
        else:
            health["memory_usage"] = "normal"
    
    def update_learning_stats(self, success: bool, generation_time: float, category: str):
        """Update learning statistics"""
        stats = self.registry["learning_stats"]
        
        if success:
            stats["successful_generations"] += 1
        else:
            stats["failed_generations"] += 1
        
        stats["total_generated_tools"] = stats["successful_generations"] + stats["failed_generations"]
        
        if stats["total_generated_tools"] > 0:
            stats["success_rate"] = round(
                (stats["successful_generations"] / stats["total_generated_tools"]) * 100, 2
            )
        
        # Update average generation time
        current_avg = stats.get("average_generation_time", 0)
        total_sessions = stats["total_generated_tools"]
        
        if total_sessions == 1:
            stats["average_generation_time"] = generation_time
        else:
            stats["average_generation_time"] = round(
                ((current_avg * (total_sessions - 1)) + generation_time) / total_sessions, 2
            )
        
        stats["last_learning_session"] = datetime.now().isoformat()
        
        # Track most requested category
        category_counts = {}
        for tool in self.registry["tools"].values():
            cat = tool.get("category", "unknown")
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        if category_counts:
            stats["most_requested_category"] = max(category_counts, key=category_counts.get)
        
        self.save_registry()
    
    def export_registry_summary(self) -> Dict:
        """Export a summary of the registry for display"""
        return {
            "total_tools": len(self.registry["tools"]),
            "categories": list(self.registry.get("categories", {}).keys()),
            "learning_stats": self.registry.get("learning_stats", {}),
            "system_health": self.registry.get("system_health", {}),
            "recent_tools": [
                {
                    "name": name,
                    "category": info.get("category"),
                    "created": info.get("created_at"),
                    "success_rate": info.get("success_rate", 0)
                }
                for name, info in sorted(
                    self.registry["tools"].items(),
                    key=lambda x: x[1].get("created_at", ""),
                    reverse=True
                )[:5]
            ],
            "recommendations": self.get_learning_recommendations()
        }

# Global instance
capability_registry = CapabilityRegistry()
