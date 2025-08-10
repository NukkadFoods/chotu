#!/usr/bin/env python3
"""
🧠 ENHANCED SELF-LEARNING CONTROLLER
===================================
Implements the complete autonomous learning pipeline with:
- Intent confidence assessment
- System-aware code generation  
- Automatic dependency installation
- Code validation and integration
"""

import json
import os
import subprocess
from typing import Dict, Any, List
from mcp.self_learning.self_learning_controller import SelfLearningController
from utils.gpt_interface import call_gpt_context, call_gpt_coding
from schema_manager import SchemaManager

class EnhancedSelfLearningController(SelfLearningController):
    """Enhanced learning with system awareness and auto-installation"""
    
    def __init__(self):
        super().__init__()
        self.schema_manager = SchemaManager()
        self.system_context = self.schema_manager.schema
        
    def handle_new_request_enhanced(self, user_request: str) -> Dict[str, Any]:
        """Enhanced learning pipeline with confidence assessment"""
        
        print(f"🎯 Enhanced Learning Pipeline: {user_request}")
        print("=" * 60)
        
        # Phase 1: Confidence Assessment
        confidence_score = self._assess_intent_confidence(user_request)
        print(f"📊 Intent Confidence: {confidence_score}%")
        
        if confidence_score < 80:
            print("🔄 Low confidence - Using GPT-3.5-turbo for clarification...")
            clarified_request = self._clarify_intent(user_request)
            print(f"✨ Clarified Intent: {clarified_request}")
        else:
            print("✅ High confidence - Proceeding directly to code generation")
            clarified_request = user_request
        
        # Phase 2: System-Aware Code Generation
        print("🛠️ Generating system-aware code...")
        generation_result = self._generate_with_system_context(clarified_request)
        
        if generation_result["status"] != "success":
            return generation_result
        
        # Phase 3: Dependency Installation
        print("📦 Installing dependencies...")
        install_result = self._install_dependencies(generation_result["dependencies"])
        
        if install_result["status"] != "success":
            return install_result
        
        # Phase 4: Code Validation & Integration
        print("✅ Validating and integrating tool...")
        return self._validate_and_integrate(generation_result)
    
    def _assess_intent_confidence(self, user_request: str) -> int:
        """Assess confidence in understanding user intent"""
        
        prompt = f"""
Assess how clearly this request specifies what the user wants:

REQUEST: "{user_request}"

Rate confidence (0-100) based on:
- Clarity of desired functionality
- Specificity of requirements  
- Technical feasibility
- Sufficient detail for implementation

Return only a number 0-100.
"""
        try:
            response = call_gpt_context(prompt)
            return int(response.strip())
        except:
            return 50  # Default to medium confidence
    
    def _clarify_intent(self, user_request: str) -> str:
        """Use GPT-3.5-turbo to clarify unclear user intent"""
        
        prompt = f"""
The user made this request but it needs clarification:

REQUEST: "{user_request}"

SYSTEM CAPABILITIES:
{json.dumps(self.system_context["chotu_capabilities"], indent=2)}

AVAILABLE TOOLS:
{json.dumps(self.system_context["available_tools"], indent=2)}

Rephrase this request as a clear, specific, technically detailed requirement that includes:
1. Exact functionality needed
2. Expected inputs and outputs
3. Integration with existing system
4. Success criteria

Return a clear, detailed requirement specification:
"""
        
        return call_gpt_context(prompt)
    
    def _generate_with_system_context(self, clarified_request: str) -> Dict[str, Any]:
        """Generate code with full system context"""
        
        prompt = f"""
TASK: Create a macOS Python tool for Chotu AI assistant

USER REQUIREMENT:
{clarified_request}

SYSTEM CONTEXT:
{json.dumps(self.system_context, indent=2)}

CRITICAL REQUIREMENTS:
1. Return ONLY raw Python code (no markdown blocks)
2. Use only macOS-compatible commands from system_context
3. Follow the exact return format specified in system_context
4. Include comprehensive error handling
5. Use subprocess.run() with shell=False for safety

At the end, provide dependencies as a comment:
# DEPENDENCIES: ["package1", "package2"]
# INSTALL_COMMANDS: ["pip install package1", "brew install tool1"]

Generate the complete Python tool:
"""
        
        try:
            code_response = call_gpt_coding(prompt)
            
            # Extract dependencies from the code
            dependencies = self._extract_dependencies(code_response)
            
            # Clean code (remove dependency comments)
            clean_code = self._clean_code_response(code_response)
            
            return {
                "status": "success",
                "code": clean_code,
                "dependencies": dependencies
            }
            
        except Exception as e:
            return {
                "status": "error", 
                "message": f"Code generation failed: {e}"
            }
    
    def _extract_dependencies(self, code_response: str) -> Dict[str, List[str]]:
        """Extract dependency information from code response"""
        dependencies = {"packages": [], "install_commands": []}
        
        for line in code_response.split('\n'):
            if line.startswith('# DEPENDENCIES:'):
                try:
                    deps = json.loads(line.split(':', 1)[1].strip())
                    dependencies["packages"] = deps
                except:
                    pass
            elif line.startswith('# INSTALL_COMMANDS:'):
                try:
                    cmds = json.loads(line.split(':', 1)[1].strip())
                    dependencies["install_commands"] = cmds
                except:
                    pass
        
        return dependencies
    
    def _clean_code_response(self, code_response: str) -> str:
        """Clean code response by removing dependency comments"""
        lines = []
        for line in code_response.split('\n'):
            if not line.startswith('# DEPENDENCIES:') and not line.startswith('# INSTALL_COMMANDS:'):
                lines.append(line)
        return '\n'.join(lines)
    
    def _install_dependencies(self, dependencies: Dict[str, List[str]]) -> Dict[str, Any]:
        """Automatically install required dependencies and update schema"""
        
        print(f"📦 Installing {len(dependencies.get('packages', []))} packages...")
        
        for package in dependencies.get("packages", []):
            if package == "subprocess":  # Skip built-in modules
                continue
                
            print(f"  📥 Installing {package}...")
            try:
                result = subprocess.run(
                    ["pip", "install", package], 
                    capture_output=True, 
                    text=True, 
                    timeout=60
                )
                if result.returncode == 0:
                    print(f"  ✅ {package} installed successfully")
                    # Update schema with new package
                    self.schema_manager.add_python_package(package)
                else:
                    print(f"  ⚠️ Package {package} install failed: {result.stderr}")
            except Exception as e:
                print(f"  ❌ Error installing {package}: {e}")
        
        for command in dependencies.get("install_commands", []):
            print(f"  🔧 Running: {command}")
            try:
                result = subprocess.run(
                    command.split(), 
                    capture_output=True, 
                    text=True, 
                    timeout=60
                )
                if result.returncode == 0:
                    print(f"  ✅ Command successful")
                    # Extract tool name and update schema
                    if "brew install" in command:
                        tool_name = command.split()[-1]
                        self.schema_manager.add_system_tool(tool_name, command)
                else:
                    print(f"  ⚠️ Command failed: {result.stderr}")
            except Exception as e:
                print(f"  ❌ Error running command: {e}")
        
        return {"status": "success"}
    
    def _validate_and_integrate(self, generation_result: Dict) -> Dict[str, Any]:
        """Validate generated code and integrate into tools"""
        
        code = generation_result["code"]
        
        # Syntax validation
        try:
            compile(code, '<generated>', 'exec')
            print("✅ Syntax validation passed")
        except SyntaxError as e:
            return {
                "status": "error",
                "message": f"Syntax error: {e}"
            }
        
        # Save and test the tool
        tool_name = f"auto_generated_tool_{len(os.listdir('/Users/mahendrabahubali/chotu/mcp/dynamic_tools'))}"
        tool_path = f"/Users/mahendrabahubali/chotu/mcp/dynamic_tools/{tool_name}.py"
        
        try:
            with open(tool_path, 'w') as f:
                f.write(code)
            
            print(f"💾 Tool saved to: {tool_path}")
            
            # Test import
            import importlib.util
            spec = importlib.util.spec_from_file_location(tool_name, tool_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            print("✅ Tool import test passed")
            
            # Extract tool capabilities for schema
            capabilities = self._extract_tool_capabilities(code)
            
            # Update schema with new tool
            self.schema_manager.add_generated_tool(tool_name, tool_path, capabilities)
            
            return {
                "status": "success",
                "message": "Tool created and validated successfully",
                "tool_path": tool_path,
                "tool_name": tool_name
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Tool integration failed: {e}"
            }
    
    def _extract_tool_capabilities(self, code: str) -> List[str]:
        """Extract function names from generated code as capabilities"""
        capabilities = []
        for line in code.split('\n'):
            if line.strip().startswith('def ') and not line.strip().startswith('def main'):
                func_name = line.split('def ')[1].split('(')[0].strip()
                capabilities.append(func_name)
        return capabilities

# Test the enhanced system
if __name__ == "__main__":
    controller = EnhancedSelfLearningController()
    result = controller.handle_new_request_enhanced(
        "create a tool to list WiFi networks and Bluetooth devices"
    )
    print(f"\n🏆 FINAL RESULT: {result}")
