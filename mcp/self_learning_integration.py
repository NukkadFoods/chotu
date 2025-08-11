#!/usr/bin/env python3
"""
🔗 SELF-LEARNING INTEGRATION
==========================
Integrates the self-learning system with the main MCP server
"""

import os
import sys
import json
import configparser
from datetime import datetime
from typing import Dict, Any, Optional

# Add paths
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import self-learning components
from mcp.self_learning.self_learning_controller import SelfLearningController
from mcp.capability_registry import capability_registry
from mcp.dynamic_loader import tool_loader

class SelfLearningIntegration:
    """Integrates self-learning capabilities with the MCP server"""
    
    def __init__(self):
        self.config = self._load_config()
        self.controller = SelfLearningController()
        self.enabled = self.config.getboolean('learning', 'auto_learning_enabled', fallback=True)
        self.safety_mode = self.config.getboolean('learning', 'safety_mode', fallback=True)
        self.max_tools = self.config.getint('learning', 'max_auto_tools', fallback=50)
        
        print(f"🔗 Self-Learning Integration initialized")
        print(f"   Auto-learning: {'ON' if self.enabled else 'OFF'}")
        print(f"   Safety mode: {'ON' if self.safety_mode else 'OFF'}")
        print(f"   Max tools: {self.max_tools}")
    
    def _load_config(self) -> configparser.ConfigParser:
        """Load the learning configuration"""
        config = configparser.ConfigParser()
        config_path = "/Users/mahendrabahubali/chotu/config/learning_config.ini"
        
        if os.path.exists(config_path):
            config.read(config_path)
        else:
            print("⚠️ Learning config not found, using defaults")
        
        return config
    
    def handle_unknown_command(self, user_request: str, context: Dict = None) -> Dict[str, Any]:
        """
        Handle unknown commands by attempting to learn the capability
        This is called when the MCP server encounters an unknown command
        """
        
        if not self.enabled:
            return {
                "success": False,
                "reason": "auto_learning_disabled",
                "message": "Auto-learning is disabled"
            }
        
        # Check if we've hit the tool limit
        current_tools = len(capability_registry.registry["tools"])
        if current_tools >= self.max_tools:
            return {
                "success": False,
                "reason": "tool_limit_reached",
                "message": f"Maximum tool limit ({self.max_tools}) reached"
            }
        
        print(f"🧠 Auto-learning triggered for: {user_request}")
        
        try:
            start_time = datetime.now()
            
            # Use the self-learning controller to handle the request
            result = self.controller.handle_new_request(user_request, context)
            
            end_time = datetime.now()
            generation_time = (end_time - start_time).total_seconds()
            
            # Update learning statistics
            success = result.get("status") == "success"
            category = "unknown"
            
            if success and "details" in result:
                if "tool_created" in result["details"]:
                    # Register the new tool in the capability registry
                    tool_name = result["details"]["tool_created"]
                    tool_info = {
                        "auto_generated": True,
                        "category": category,
                        "description": f"Auto-generated for: {user_request}",
                        "capabilities": [user_request.lower().replace(" ", "_")],
                        "safety_level": "safe" if self.safety_mode else "medium"
                    }
                    capability_registry.register_tool(tool_name, tool_info)
                    
                    # Reload tools in the dynamic loader
                    tool_loader.load_all_tools()
            
            # Update learning statistics
            capability_registry.update_learning_stats(success, generation_time, category)
            
            return result
            
        except Exception as e:
            print(f"❌ Auto-learning failed: {e}")
            
            # Update failure statistics
            capability_registry.update_learning_stats(False, 0, "unknown")
            
            return {
                "success": False,
                "reason": "learning_error",
                "message": f"Auto-learning failed: {str(e)}"
            }
    
    def handle_tool_failure(self, tool_name: str, error_message: str, user_intent: str) -> Dict[str, Any]:
        """
        Handle tool failures by attempting to learn an improved version
        This enables Chotu to learn from its mistakes
        """
        
        if not self.enabled:
            return {
                "success": False,
                "reason": "auto_learning_disabled"
            }
        
        print(f"🔧 Learning from tool failure: {tool_name}")
        
        try:
            # Use the failure learning capability
            result = self.controller.learn_from_failure(tool_name, error_message, user_intent)
            
            if result.get("success"):
                improved_tool = result.get("improved_tool")
                
                if improved_tool:
                    # Register the improved tool
                    tool_info = {
                        "auto_generated": True,
                        "category": "improved",
                        "description": f"Improved version of {tool_name}",
                        "capabilities": [user_intent.lower().replace(" ", "_")],
                        "safety_level": "safe" if self.safety_mode else "medium",
                        "replaces": tool_name
                    }
                    capability_registry.register_tool(improved_tool, tool_info)
                    
                    # Mark original tool as deprecated in registry
                    original_info = capability_registry.get_tool_info(tool_name)
                    if original_info:
                        original_info["deprecated"] = True
                        original_info["replaced_by"] = improved_tool
                        capability_registry.save_registry()
                    
                    # Reload tools
                    tool_loader.load_all_tools()
                    
                    print(f"✅ Learned improved tool: {improved_tool}")
            
            return result
            
        except Exception as e:
            print(f"❌ Failure learning failed: {e}")
            return {
                "success": False,
                "reason": "failure_learning_error",
                "message": str(e)
            }
    
    def get_learning_status(self) -> Dict[str, Any]:
        """Get the current status of the learning system"""
        
        registry_summary = capability_registry.export_registry_summary()
        controller_stats = self.controller.get_learning_statistics()
        
        return {
            "enabled": self.enabled,
            "safety_mode": self.safety_mode,
            "max_tools": self.max_tools,
            "current_tools": registry_summary["total_tools"],
            "learning_stats": registry_summary["learning_stats"],
            "system_health": registry_summary["system_health"],
            "controller_stats": controller_stats,
            "recent_tools": registry_summary["recent_tools"],
            "recommendations": registry_summary["recommendations"]
        }
    
    def toggle_auto_learning(self, enabled: bool) -> bool:
        """Enable or disable auto-learning"""
        self.enabled = enabled
        
        # Update config file
        config_path = "/Users/mahendrabahubali/chotu/config/learning_config.ini"
        if os.path.exists(config_path):
            self.config.set('learning', 'auto_learning_enabled', '1' if enabled else '0')
            with open(config_path, 'w') as f:
                self.config.write(f)
        
        print(f"🔄 Auto-learning {'enabled' if enabled else 'disabled'}")
        return True
    
    def create_system_backup(self) -> str:
        """Create a backup of the current system state"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        checkpoint_name = f"system_backup_{timestamp}"
        
        success = self.controller.create_system_checkpoint(checkpoint_name)
        
        if success:
            print(f"💾 System backup created: {checkpoint_name}")
            return checkpoint_name
        else:
            print("❌ Failed to create system backup")
            return ""
    
    def manual_learn_capability(self, user_request: str, force: bool = False) -> Dict[str, Any]:
        """
        Manually trigger learning for a specific capability
        Used by the /learn endpoint
        """
        
        if not force and not self.enabled:
            return {
                "success": False,
                "reason": "auto_learning_disabled",
                "message": "Auto-learning is disabled. Use force=true to override."
            }
        
        print(f"👤 Manual learning request: {user_request}")
        
        # Use the same learning pipeline as auto-learning
        return self.handle_unknown_command(user_request, {"manual": True, "force": force})
    
    def get_capability_gaps(self) -> Dict[str, Any]:
        """Analyze capability gaps and suggest improvements"""
        
        recommendations = capability_registry.get_learning_recommendations()
        
        # Add analysis from the learning controller
        existing_capabilities = {
            tool_name: tool_info.get("capabilities", [])
            for tool_name, tool_info in capability_registry.registry["tools"].items()
        }
        
        return {
            "missing_categories": recommendations["missing_categories"],
            "low_performing_tools": recommendations["low_performing_tools"],
            "suggested_capabilities": [
                "file_compression",
                "email_automation", 
                "calendar_management",
                "system_monitoring",
                "network_diagnostics",
                "media_conversion",
                "text_processing",
                "api_integration"
            ],
            "existing_capabilities": existing_capabilities,
            "total_tools": len(existing_capabilities),
            "health_score": self._calculate_health_score()
        }
    
    def _calculate_health_score(self) -> float:
        """Calculate overall system health score (0-100)"""
        
        tools = capability_registry.registry["tools"]
        if not tools:
            return 0.0
        
        # Factors: success rates, tool coverage, recent activity
        total_success_rate = sum(tool.get("success_rate", 0) for tool in tools.values())
        avg_success_rate = total_success_rate / len(tools)
        
        # Coverage factor (more categories = better)
        categories = set(tool.get("category") for tool in tools.values())
        coverage_score = min(len(categories) * 10, 50)  # Max 50 points for coverage
        
        # Activity factor (recent usage = better)
        recent_tools = 0
        current_time = datetime.now()
        
        for tool in tools.values():
            last_tested = tool.get("last_tested")
            if last_tested:
                try:
                    # Handle both timezone-aware and naive datetime strings
                    if last_tested.endswith('Z'):
                        last_tested = last_tested[:-1] + '+00:00'
                    elif '+' not in last_tested and 'T' in last_tested:
                        # Assume naive datetime is local time
                        test_time = datetime.fromisoformat(last_tested)
                    else:
                        test_time = datetime.fromisoformat(last_tested)
                    
                    # For timezone-aware comparison, make current_time naive too
                    if hasattr(test_time, 'tzinfo') and test_time.tzinfo is not None:
                        test_time = test_time.replace(tzinfo=None)
                    
                    if (current_time - test_time).days < 7:
                        recent_tools += 1
                except (ValueError, TypeError):
                    # Skip invalid datetime strings
                    continue
        activity_score = min((recent_tools / len(tools)) * 30, 30)  # Max 30 points for activity
        
        health_score = (avg_success_rate * 0.2) + coverage_score + activity_score
        return round(min(health_score, 100), 2)

# Global instance
self_learning_integration = SelfLearningIntegration()
