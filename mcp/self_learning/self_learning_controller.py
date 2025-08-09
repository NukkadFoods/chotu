#!/usr/bin/env python3
"""
🧠 SELF-LEARNING CONTROLLER
===========================
Main controller that orchestrates the autonomous learning process
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

# Import self-learning components
from .code_analyzer import CodeAnalyzer
from .code_generator import CodeGenerator
from .code_validator import CodeValidator
from .code_updater import CodeUpdater
from .sandbox_executor import SandboxExecutor

# Import specialized GPT interface
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from utils.gpt_interface import call_gpt_learning, call_gpt_system

class SelfLearningController:
    """Main controller for autonomous self-learning capabilities"""
    
    def __init__(self):
        self.analyzer = CodeAnalyzer()
        self.generator = CodeGenerator()
        self.validator = CodeValidator()
        self.updater = CodeUpdater()
        self.sandbox = SandboxExecutor()
        
        self.learning_log = self._load_learning_log()
        self.safety_mode = os.getenv('MCP_SAFE_MODE', '1') == '1'
        self.max_tools = int(os.getenv('MCP_MAX_TOOLS', '100'))
        
        print(f"🧠 Self-Learning Controller initialized")
        print(f"🔒 Safety Mode: {'ON' if self.safety_mode else 'OFF'}")
        print(f"📊 Max Tools: {self.max_tools}")
    
    def _load_learning_log(self) -> Dict:
        """Load the learning history log"""
        log_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "learning_log.json")
        
        try:
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    return json.load(f)
            else:
                return {
                    "code_updates": [],
                    "generated_tools": [],
                    "validation_errors": [],
                    "learning_sessions": [],
                    "success_rate": 0.0,
                    "total_attempts": 0,
                    "successful_attempts": 0
                }
        except Exception as e:
            print(f"⚠️ Failed to load learning log: {e}")
            return {"code_updates": [], "generated_tools": [], "validation_errors": []}
    
    def _save_learning_log(self):
        """Save the learning history log"""
        log_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "learning_log.json")
        
        try:
            with open(log_file, 'w') as f:
                json.dump(self.learning_log, f, indent=2)
        except Exception as e:
            print(f"⚠️ Failed to save learning log: {e}")
    
    def handle_new_request(self, intent: str, context: Dict = None) -> Dict[str, Any]:
        """
        Handle a new capability request through autonomous learning
        
        Args:
            intent: User's intent/request
            context: Additional context about the request
        
        Returns:
            Dict: Learning result with status and details
        """
        
        print(f"🎯 Handling new learning request: {intent}")
        
        # Record learning attempt
        self.learning_log["total_attempts"] += 1
        
        learning_session = {
            "timestamp": datetime.now().isoformat(),
            "intent": intent,
            "context": context or {},
            "status": "started",
            "steps": []
        }
        
        try:
            # Step 1: Analyze the capability gap
            print("📊 Step 1: Analyzing capability gap...")
            existing_capabilities = self._get_existing_capabilities()
            analysis = self.analyzer.analyze_intent(intent, existing_capabilities)
            
            learning_session["steps"].append({
                "step": "analysis",
                "status": "completed",
                "result": analysis
            })
            
            # Check if we actually need a new capability
            if not self.analyzer.validate_capability_gap(intent, analysis):
                learning_session["status"] = "skipped"
                learning_session["reason"] = "capability_already_exists"
                self.learning_log["learning_sessions"].append(learning_session)
                self._save_learning_log()
                
                return {
                    "status": "exists",
                    "message": "Capability already exists",
                    "details": analysis
                }
            
            # Step 2: Generate implementation plan
            print("📋 Step 2: Generating implementation plan...")
            enhancement_plan = self.analyzer.generate_enhancement_plan(analysis)
            
            learning_session["steps"].append({
                "step": "planning",
                "status": "completed",
                "result": enhancement_plan
            })
            
            # Check if we should proceed based on plan assessment
            if enhancement_plan["priority_level"] == "low" and self.safety_mode:
                learning_session["status"] = "aborted"
                learning_session["reason"] = "low_priority_in_safe_mode"
                self.learning_log["learning_sessions"].append(learning_session)
                self._save_learning_log()
                
                return {
                    "status": "deferred",
                    "message": "Request deferred due to low priority in safe mode",
                    "plan": enhancement_plan
                }
            
            # Step 3: Generate or enhance code
            print("🛠️ Step 3: Generating code...")
            if analysis["implementation_strategy"]["approach"] == "extend_existing":
                result = self._enhance_existing_capability(analysis, enhancement_plan, learning_session)
            else:
                result = self._create_new_capability(analysis, enhancement_plan, learning_session)
            
            if not result["success"]:
                learning_session["status"] = "failed"
                learning_session["error"] = result["error"]
                self.learning_log["learning_sessions"].append(learning_session)
                self.learning_log["validation_errors"].append({
                    "timestamp": datetime.now().isoformat(),
                    "intent": intent,
                    "error": result["error"]
                })
                self._save_learning_log()
                
                return result
            
            # Step 4: Final validation and deployment
            print("✅ Step 4: Final validation...")
            validation_result = self._final_validation(result, learning_session)
            
            if validation_result["success"]:
                learning_session["status"] = "completed"
                learning_session["result"] = validation_result
                self.learning_log["successful_attempts"] += 1
                self.learning_log["generated_tools"].append({
                    "timestamp": datetime.now().isoformat(),
                    "intent": intent,
                    "tool_name": result.get("tool_name"),
                    "approach": analysis["implementation_strategy"]["approach"]
                })
            else:
                learning_session["status"] = "validation_failed"
                learning_session["error"] = validation_result["error"]
                self.learning_log["validation_errors"].append({
                    "timestamp": datetime.now().isoformat(),
                    "intent": intent,
                    "error": validation_result["error"]
                })
            
            self.learning_log["learning_sessions"].append(learning_session)
            self._update_success_rate()
            self._save_learning_log()
            
            return validation_result
            
        except Exception as e:
            learning_session["status"] = "error"
            learning_session["error"] = str(e)
            self.learning_log["learning_sessions"].append(learning_session)
            self._save_learning_log()
            
            print(f"❌ Learning session failed: {e}")
            return {
                "status": "error",
                "message": f"Learning failed: {str(e)}",
                "session": learning_session
            }
    
    def _get_existing_capabilities(self) -> Dict:
        """Get all existing capabilities"""
        # This would integrate with the dynamic loader
        tools_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tools")
        capabilities = {}
        
        if os.path.exists(tools_dir):
            for file in os.listdir(tools_dir):
                if file.endswith('.py') and not file.startswith('__'):
                    module_name = file[:-3]
                    capabilities[module_name] = {"functions": [], "description": ""}
        
        return capabilities
    
    def _enhance_existing_capability(self, analysis: Dict, plan: Dict, session: Dict) -> Dict:
        """Enhance an existing capability"""
        
        target_module = analysis["implementation_strategy"]["target_module"]
        tools_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tools")
        module_path = os.path.join(tools_dir, f"{target_module}.py")
        
        if not os.path.exists(module_path):
            return {
                "success": False,
                "error": f"Target module {target_module} not found"
            }
        
        # Generate enhancement requirements
        enhancement_requirements = {
            "target_module": target_module,
            "new_functionality": analysis["missing_capability"],
            "function_name": analysis["implementation_strategy"]["new_function_name"],
            "integration_points": analysis["implementation_strategy"]["integration_points"],
            "safety_considerations": analysis["safety_considerations"]
        }
        
        # Generate enhanced code
        enhanced_code = self.generator.update_existing_tool(module_path, enhancement_requirements)
        
        if not enhanced_code:
            return {
                "success": False,
                "error": "Failed to generate enhanced code"
            }
        
        # Validate enhanced code
        validation_result = self.validator.comprehensive_validation(enhanced_code)
        
        if not validation_result["overall_valid"]:
            return {
                "success": False,
                "error": f"Enhanced code validation failed: {validation_result}",
                "validation_details": validation_result
            }
        
        # Test in sandbox if enabled
        if self.safety_mode:
            sandbox_result = self.sandbox.execute_with_full_monitoring(enhanced_code)
            
            if not sandbox_result["overall_safe"]:
                return {
                    "success": False,
                    "error": f"Enhanced code failed sandbox testing: {sandbox_result}",
                    "sandbox_details": sandbox_result
                }
        
        # Update the file
        update_success = self.updater.atomic_update(
            module_path, 
            enhanced_code, 
            f"enhance_for_{analysis['missing_capability']}"
        )
        
        if not update_success:
            return {
                "success": False,
                "error": "Failed to update module file"
            }
        
        session["steps"].append({
            "step": "enhancement",
            "status": "completed",
            "module": target_module,
            "validation": validation_result
        })
        
        return {
            "success": True,
            "approach": "enhancement",
            "module_enhanced": target_module,
            "function_added": analysis["implementation_strategy"]["new_function_name"]
        }
    
    def _create_new_capability(self, analysis: Dict, plan: Dict, session: Dict) -> Dict:
        """Create a new capability"""
        
        # Check tool limit
        existing_tools = len(self._get_existing_capabilities())
        if existing_tools >= self.max_tools:
            return {
                "success": False,
                "error": f"Maximum tool limit reached ({self.max_tools})"
            }
        
        # Generate tool requirements
        tool_requirements = {
            "name": analysis["implementation_strategy"]["new_function_name"],
            "category": analysis["intent_category"],
            "description": analysis["missing_capability"],
            "user_goal": analysis["user_goal"],
            "technical_requirements": analysis["technical_requirements"],
            "safety_considerations": analysis["safety_considerations"],
            "test_scenarios": analysis["test_scenarios"]
        }
        
        # Generate new tool code
        tool_code = self.generator.generate_tool(tool_requirements)
        
        if not tool_code:
            return {
                "success": False,
                "error": "Failed to generate tool code"
            }
        
        # Validate generated code
        validation_result = self.validator.comprehensive_validation(tool_code)
        
        if not validation_result["overall_valid"]:
            return {
                "success": False,
                "error": f"Generated code validation failed: {validation_result}",
                "validation_details": validation_result
            }
        
        # Test in sandbox if enabled
        if self.safety_mode:
            sandbox_result = self.sandbox.execute_with_full_monitoring(tool_code)
            
            if not sandbox_result["overall_safe"]:
                return {
                    "success": False,
                    "error": f"Generated code failed sandbox testing: {sandbox_result}",
                    "sandbox_details": sandbox_result
                }
        
        # Generate complete tool package
        tool_name = tool_requirements["name"]
        tool_package = self.generator.create_tool_package(tool_name, tool_code, tool_requirements)
        
        # Save the tool package
        save_success = self.generator.save_tool_package(tool_name, tool_package)
        
        if not save_success:
            return {
                "success": False,
                "error": "Failed to save tool package"
            }
        
        session["steps"].append({
            "step": "generation",
            "status": "completed",
            "tool_name": tool_name,
            "validation": validation_result
        })
        
        return {
            "success": True,
            "approach": "new_tool",
            "tool_created": tool_name,
            "tool_name": tool_name
        }
    
    def _final_validation(self, result: Dict, session: Dict) -> Dict:
        """Perform final validation of the learning result"""
        
        if not result["success"]:
            return result
        
        try:
            # Reload capabilities to verify integration
            new_capabilities = self._get_existing_capabilities()
            
            # Check if the new capability is accessible
            if result["approach"] == "new_tool":
                tool_name = result["tool_created"]
                if tool_name not in new_capabilities:
                    return {
                        "success": False,
                        "error": f"New tool {tool_name} not found in capabilities after creation"
                    }
            
            # Run integration test
            integration_test = self._run_integration_test(result)
            
            if not integration_test["success"]:
                return {
                    "success": False,
                    "error": f"Integration test failed: {integration_test['error']}"
                }
            
            session["steps"].append({
                "step": "final_validation",
                "status": "completed",
                "integration_test": integration_test
            })
            
            return {
                "status": "success",
                "message": "New capability successfully learned and validated",
                "details": result,
                "integration_test": integration_test
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Final validation failed: {str(e)}"
            }
    
    def _run_integration_test(self, result: Dict) -> Dict:
        """Run integration test for the new capability"""
        
        # This is a basic integration test
        # In a full implementation, this would test the capability in the context of the MCP server
        
        try:
            if result["approach"] == "new_tool":
                tool_name = result["tool_created"]
                tools_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tools")
                tool_path = os.path.join(tools_dir, f"{tool_name}.py")
                
                if not os.path.exists(tool_path):
                    return {
                        "success": False,
                        "error": f"Tool file not found: {tool_path}"
                    }
                
                # Try to import the tool
                import importlib.util
                spec = importlib.util.spec_from_file_location(tool_name, tool_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Check if the main function exists
                if hasattr(module, tool_name):
                    return {
                        "success": True,
                        "message": f"Tool {tool_name} successfully integrated"
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Main function {tool_name} not found in module"
                    }
            
            elif result["approach"] == "enhancement":
                module_name = result["module_enhanced"]
                tools_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tools")
                module_path = os.path.join(tools_dir, f"{module_name}.py")
                
                # Try to reload the enhanced module
                import importlib.util
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                function_name = result["function_added"]
                if hasattr(module, function_name):
                    return {
                        "success": True,
                        "message": f"Enhanced function {function_name} successfully integrated"
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Enhanced function {function_name} not found in module"
                    }
            
            return {
                "success": True,
                "message": "Integration test passed"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Integration test failed: {str(e)}"
            }
    
    def _update_success_rate(self):
        """Update the success rate statistics"""
        if self.learning_log["total_attempts"] > 0:
            self.learning_log["success_rate"] = (
                self.learning_log["successful_attempts"] / 
                self.learning_log["total_attempts"]
            ) * 100
    
    def get_learning_statistics(self) -> Dict:
        """Get learning statistics and performance metrics"""
        
        return {
            "total_attempts": self.learning_log["total_attempts"],
            "successful_attempts": self.learning_log["successful_attempts"],
            "success_rate": self.learning_log.get("success_rate", 0.0),
            "tools_generated": len(self.learning_log.get("generated_tools", [])),
            "validation_errors": len(self.learning_log.get("validation_errors", [])),
            "learning_sessions": len(self.learning_log.get("learning_sessions", [])),
            "safety_mode": self.safety_mode,
            "max_tools": self.max_tools
        }
    
    def create_system_checkpoint(self, name: str) -> bool:
        """Create a system checkpoint for rollback purposes"""
        return self.updater.create_system_checkpoint(name)
    
    def rollback_to_checkpoint(self, checkpoint_path: str) -> bool:
        """Rollback system to a previous checkpoint"""
        return self.updater.restore_system_checkpoint(checkpoint_path)
    
    def learn_from_failure(self, tool_name: str, error_message: str, user_intent: str) -> Dict[str, Any]:
        """
        Learn from tool failure and autonomously create improved solution
        This is where Chotu learns from mistakes and improves itself
        """
        print(f"\n🔧 Chotu Learning from Failure: {tool_name}")
        print(f"   Error: {error_message[:100]}...")
        print(f"   Intent: {user_intent}")
        
        try:
            # Step 1: Analyze the failure
            print("\n📊 Analyzing why the tool failed...")
            failure_analysis = self.analyzer.analyze_tool_failure(tool_name, error_message, user_intent)
            
            if not failure_analysis.get('failure_analysis', {}).get('fixable', False):
                print("❌ Analysis indicates this failure is not easily fixable")
                return {
                    'success': False,
                    'reason': 'unfixable_failure',
                    'analysis': failure_analysis
                }
            
            # Step 2: Generate improvement requirements 
            improvement_req = f"""
Improve failed tool: {tool_name}

FAILURE CONTEXT:
- Original Error: {error_message}
- User Intent: {user_intent}
- Root Cause: {failure_analysis.get('failure_analysis', {}).get('root_cause', 'unknown')}

IMPROVEMENT REQUIREMENTS:
{json.dumps(failure_analysis.get('technical_requirements', {}), indent=2)}

Create an improved version that addresses the root cause and fulfills the user's intent.
"""
            
            # Step 3: Let Chotu learn and generate improved tool
            result = self.handle_new_request(improvement_req)
            
            if result.get('status') == 'success':
                # Log this learning experience
                self._log_failure_learning(tool_name, error_message, user_intent, failure_analysis, result)
                print(f"✅ Chotu successfully learned from failure and created improved solution")
                
                return {
                    'success': True,
                    'improved_tool': result.get('details', {}).get('tool_created', 'improved_tool'),
                    'analysis': failure_analysis,
                    'result': result
                }
            else:
                return {
                    'success': False,
                    'reason': f"improvement_failed: {result.get('message', 'unknown')}",
                    'analysis': failure_analysis
                }
            
        except Exception as e:
            print(f"❌ Learning from failure failed: {e}")
            return {
                'success': False,
                'reason': f'learning_error: {e}',
                'analysis': {}
            }
    
    def _log_failure_learning(self, original_tool: str, error: str, intent: str, analysis: Dict, result: Dict):
        """Log failure learning for future reference"""
        learning_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': 'failure_learning',
            'original_tool': original_tool,
            'error_summary': error[:200],
            'user_intent': intent,
            'root_cause': analysis.get('failure_analysis', {}).get('root_cause', 'unknown'),
            'solution_approach': analysis.get('improvement_strategy', {}).get('approach', 'unknown'),
            'new_tool': result.get('details', {}).get('tool_created', 'unknown'),
            'success': result.get('status') == 'success',
            'lessons_learned': analysis.get('domain_knowledge', {}).get('concepts_to_learn', [])
        }
        
        # Add to learning logs
        if 'failure_learning' not in self.learning_log:
            self.learning_log['failure_learning'] = []
        
        self.learning_log['failure_learning'].append(learning_entry)
        self._save_learning_log()
