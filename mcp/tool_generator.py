#!/usr/bin/env python3
"""
🧠 DYNAMIC TOOL GENERATOR
========================
Automatically generates new tools when MCP encounters unknown commands
"""

import os
import json
import importlib
import importlib.util
from datetime import datetime

# Import specialized GPT interface functions
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.gpt_interface import call_gpt_learning, call_gpt_coding, call_gpt_context

class ToolGenerator:
    """Generates new tools dynamically based on user requests"""
    
    def __init__(self):
        # Auto-detect tools directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.tools_dir = os.path.join(current_dir, "tools")
        self.pending_tasks = []
        self.learned_tools = []
        
    def analyze_unknown_command(self, user_request, current_capabilities):
        """Analyze what new tool is needed using learning model"""
        prompt = f"""
You are an expert Python developer for an AI assistant MCP server.

USER REQUEST: {user_request}
CURRENT CAPABILITIES: {current_capabilities}

This request failed because we don't have the right tool. Analyze what's needed:

1. What specific functionality is missing?
2. What would be the best tool name (snake_case)?
3. What parameters would this tool need?
4. What imports/libraries might be required?

Respond in JSON format:
{{
    "missing_capability": "description of what's missing",
    "tool_name": "suggested_tool_name",
    "tool_category": "system|app|file|web|communication",
    "parameters": ["param1", "param2"],
    "required_imports": ["import1", "import2"],
    "complexity": "simple|medium|complex"
}}
"""
        
        try:
            response = call_gpt_learning(prompt)  # Use learning model for analysis
            # Clean JSON response
            response = response.strip()
            if response.startswith('```json'):
                response = response[7:]
            if response.endswith('```'):
                response = response[:-3]
            return json.loads(response.strip())
        except Exception as e:
            print(f"❌ Failed to analyze command: {e}")
            return None
    
    def generate_tool_code(self, tool_analysis, user_request):
        """Generate Python code for the new tool"""
        
        # Load tool schema for system context
        schema_path = os.path.join(os.path.dirname(self.tools_dir), "tool_schema.json")
        tool_schema = {}
        try:
            with open(schema_path, 'r') as f:
                tool_schema = json.load(f)
        except Exception as e:
            print(f"⚠️ Could not load tool schema: {e}")
        
        prompt = f"""
You are an expert Python developer creating tools for macOS. Generate a complete Python tool for an MCP server.

SYSTEM CONTEXT: {json.dumps(tool_schema, indent=2)}

TOOL ANALYSIS: {json.dumps(tool_analysis, indent=2)}
ORIGINAL USER REQUEST: {user_request}

CRITICAL INSTRUCTIONS:
1. Use ONLY commands/tools listed in "guaranteed_available" or "built_in_apps"
2. For "may_not_be_installed" tools, ALWAYS check existence first with 'which tool_name'
3. Follow the macOS-specific patterns exactly as shown in the schema
4. Use the working examples as templates
5. Implement proper error handling and fallbacks
6. NEVER invent commands that don't exist

Generate a complete Python file following these patterns:

FOR CAMERA/PHOTO:
- Check if imagesnap exists: subprocess.run(['which', 'imagesnap'], capture_output=True, check=True)
- If yes: use imagesnap with timestamp filename
- If no: use Photo Booth via AppleScript

FOR VOLUME:
- Use: osascript -e 'set volume output volume LEVEL_VALUE'
- Level range: 0-100
- Replace LEVEL_VALUE with actual parameter

FOR BRIGHTNESS:
- Use: osascript -e 'tell application "System Events" to tell every desktop to set brightness to BRIGHTNESS_VALUE'
- Level range: 0.0-1.0
- Replace BRIGHTNESS_VALUE with actual parameter

FOR APPS:
- Open: open -a 'APPLICATION_NAME'
- Close: osascript -e 'tell app "APPLICATION_NAME" to quit'
- Replace APPLICATION_NAME with actual app name

FOR FILES/FOLDERS:
- Create folder: os.makedirs(path, exist_ok=True) or mkdir -p
- Open folder: open 'FOLDER_PATH'
- Replace FOLDER_PATH with actual path

Example structure:
```python
# mcp/tools/{tool_analysis['tool_name']}.py
import subprocess
import os
from datetime import datetime

def {tool_analysis['tool_name']}(param1=None, param2=None):
    \"\"\"
    {tool_analysis.get('missing_capability', 'Tool description')}
    
    Args:
        param1: Description (optional with default)
        param2: Description (optional with default)
    
    Returns:
        str: Success/error message with ✅/❌ prefix
    \"\"\"
    try:
        # Check if external tool needed and exists
        # Use appropriate macOS command from schema
        # Implement with proper error handling
        return f"✅ Success: Operation completed"
    except Exception as e:
        return f"❌ Error: " + str(e)
```

RESPOND WITH ONLY THE PYTHON CODE, NO EXPLANATIONS.

Generate ONLY the Python code, no explanations:
"""
        
        try:
            return call_gpt_coding(prompt)  # Use coding model for code generation
        except Exception as e:
            print(f"❌ Failed to generate tool code: {e}")
            return None
    
    def save_new_tool(self, tool_name, tool_code):
        """Save the generated tool to the tools directory"""
        try:
            # Clean the code
            if tool_code.startswith('```python'):
                tool_code = tool_code[9:]
            if tool_code.endswith('```'):
                tool_code = tool_code[:-3]
            tool_code = tool_code.strip()
            
            # Save to file
            file_path = f"{self.tools_dir}/{tool_name}.py"
            with open(file_path, 'w') as f:
                f.write(tool_code)
            
            print(f"💾 New tool saved: {file_path}")
            return file_path
        except Exception as e:
            print(f"❌ Failed to save tool: {e}")
            return None
    
    def reload_tools(self):
        """Dynamically reload all tools"""
        try:
            # Clear import cache
            importlib.invalidate_caches()
            
            # Reimport the main module to pick up new tools
            print("🔄 Reloading tools...")
            return True
        except Exception as e:
            print(f"❌ Failed to reload tools: {e}")
            return False
    
    def test_new_tool(self, tool_name, original_request):
        """Test if the new tool works for the original request"""
        try:
            # Import the new tool
            spec = importlib.util.spec_from_file_location(
                tool_name, f"{self.tools_dir}/{tool_name}.py"
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Get the main function (assumes same name as file)
            if hasattr(module, tool_name):
                func = getattr(module, tool_name)
                # Test with minimal parameters
                result = func()
                print(f"✅ Tool test successful: {result}")
                return True
            else:
                print(f"❌ Function {tool_name} not found in module")
                return False
                
        except Exception as e:
            print(f"❌ Tool test failed: {e}")
            return False
    
    def intelligent_learn(self, learning_context):
        """
        INTELLIGENT LEARNING: Analyzes conversation history, user feedback, 
        and existing capabilities to understand what went wrong and fix it
        """
        print(f"🧠 INTELLIGENT LEARNING: Analyzing context...")
        
        prompt = f"""
You are an AI system that learns from context like a human baby. Analyze this failure and implement the correct solution.

CONTEXT ANALYSIS:
=================
Failed Command: {learning_context['failed_command']}
User Feedback: {learning_context['user_feedback']}
Error Context: {learning_context['error_context']}
Confidence Data: {learning_context['confidence_data']}
NLP Analysis: {learning_context['nlp_analysis']}

EXISTING CAPABILITIES:
=====================
{json.dumps(learning_context['existing_capabilities'], indent=2)}

LEARNING TASK:
==============
The user said: "{learning_context['user_feedback']}"
The system tried: "{learning_context['failed_command']}"

From this interaction, I need to:
1. Understand what the user ACTUALLY wanted vs what the system did
2. Identify if this requires a NEW function or FIXING an existing one
3. Determine the exact functionality needed

ANALYSIS QUESTIONS:
- Did the system misinterpret the command? (e.g., "bluetooth devices" → "enable bluetooth")
- Is this a missing feature in an existing module? (e.g., bluetooth module missing list_devices)
- Does this need a completely new tool/module?
- Can I infer the correct behavior from similar existing functions?

Respond in JSON format:
{{
    "analysis_type": "misinterpretation|missing_feature|new_capability",
    "root_cause": "detailed explanation of what went wrong",
    "user_actual_intent": "what the user really wanted",
    "solution_approach": "enhance_existing|create_new|fix_routing",
    "target_module": "which existing module to enhance (if applicable)",
    "function_needed": "specific function name needed",
    "implementation_strategy": "detailed plan for implementation",
    "test_criteria": "how to verify the fix works"
}}
"""
        
        try:
            response = call_gpt_learning(prompt)  # Use learning model for intelligent analysis
            response = response.strip()
            if response.startswith('```json'):
                response = response[7:]
            if response.endswith('```'):
                response = response[:-3]
            analysis = json.loads(response.strip())
            
            print(f"🎯 Intelligent Analysis: {analysis['analysis_type']}")
            print(f"🔍 Root Cause: {analysis['root_cause']}")
            print(f"🎪 Solution: {analysis['solution_approach']}")
            
            # Execute the solution based on analysis
            if analysis['solution_approach'] == 'enhance_existing':
                return self.enhance_existing_module(analysis, learning_context)
            elif analysis['solution_approach'] == 'create_new':
                return self.create_intelligent_tool(analysis, learning_context)
            elif analysis['solution_approach'] == 'fix_routing':
                return self.fix_command_routing(analysis, learning_context)
            else:
                print(f"❌ Unknown solution approach: {analysis['solution_approach']}")
                return False
                
        except Exception as e:
            print(f"❌ Intelligent learning failed: {e}")
            return False
    
    def enhance_existing_module(self, analysis, learning_context):
        """Enhance an existing module with missing functionality"""
        print(f"🔧 Enhancing existing module: {analysis['target_module']}")
        
        # Read the existing module
        module_path = os.path.join(self.tools_dir, f"{analysis['target_module']}.py")
        if not os.path.exists(module_path):
            print(f"❌ Module {analysis['target_module']} not found")
            return False
        
        with open(module_path, 'r') as f:
            existing_code = f.read()
        
        # Generate the enhancement
        prompt = f"""
You are enhancing an existing Python module. Add the missing functionality intelligently.

EXISTING MODULE CODE:
{existing_code}

ENHANCEMENT NEEDED:
Function Name: {analysis['function_needed']}
User Intent: {analysis['user_actual_intent']}
Implementation Strategy: {analysis['implementation_strategy']}

Add the new function to the existing module. Follow these rules:
1. Maintain the existing code structure and style
2. Add proper imports if needed
3. Follow the same error handling patterns
4. Use similar return message formats (✅/❌ prefix)
5. Place the new function logically within the module

Return the COMPLETE enhanced module code:
"""
        
        try:
            enhanced_code = call_gpt_coding(prompt)  # Use coding model for code enhancement
            if enhanced_code.startswith('```python'):
                enhanced_code = enhanced_code[9:]
            if enhanced_code.endswith('```'):
                enhanced_code = enhanced_code[:-3]
            enhanced_code = enhanced_code.strip()
            
            # Backup original and save enhanced version
            backup_path = f"{module_path}.backup"
            with open(backup_path, 'w') as f:
                f.write(existing_code)
            
            with open(module_path, 'w') as f:
                f.write(enhanced_code)
            
            print(f"✅ Enhanced module saved: {module_path}")
            print(f"📁 Backup created: {backup_path}")
            return True
            
        except Exception as e:
            print(f"❌ Module enhancement failed: {e}")
            return False
    
    def create_intelligent_tool(self, analysis, learning_context):
        """Create a new tool based on intelligent analysis"""
        print(f"🛠️ Creating intelligent tool: {analysis['function_needed']}")
        
        # Use the enhanced understanding to create a better tool
        tool_analysis = {
            "missing_capability": analysis['user_actual_intent'],
            "tool_name": analysis['function_needed'],
            "implementation_strategy": analysis['implementation_strategy'],
            "test_criteria": analysis['test_criteria']
        }
        
        return self.generate_contextual_tool(tool_analysis, learning_context)
    
    def fix_command_routing(self, analysis, learning_context):
        """Fix command routing/interpretation issues"""
        print(f"🔀 Fixing command routing based on: {analysis['root_cause']}")
        
        # This would typically involve updating the command processing logic
        # For now, we'll enhance the existing module to handle the routing better
        if analysis.get('target_module'):
            return self.enhance_existing_module(analysis, learning_context)
        else:
            print("❌ No target module specified for routing fix")
            return False
    
    def adaptive_learn_from_failure(self, learning_context, failure_result):
        """
        ADAPTIVE LEARNING: Learn from failures and adapt the solution
        """
        print(f"🎯 ADAPTIVE LEARNING: Learning from failure...")
        
        prompt = f"""
The first learning attempt failed. Analyze the failure and create an adaptive solution.

ORIGINAL CONTEXT: {learning_context}
FAILURE RESULT: {failure_result}

What went wrong and how can I fix it? Consider:
1. Was the generated code syntactically correct?
2. Did it use the right APIs/commands for macOS?
3. Was the function placed in the right module?
4. Did it handle errors properly?

Create an improved solution that addresses these specific failures.

Respond with a corrective action plan in JSON:
{{
    "failure_analysis": "what specifically went wrong",
    "corrective_action": "create_new|fix_existing|different_approach",
    "new_strategy": "detailed plan for the corrective action",
    "target_module": "which module to target",
    "code_corrections": "specific code fixes needed"
}}
"""
        
        try:
            response = call_gpt(prompt)
            response = response.strip()
            if response.startswith('```json'):
                response = response[7:]
            if response.endswith('```'):
                response = response[:-3]
            adaptive_plan = json.loads(response.strip())
            
            print(f"🔄 Adaptive Plan: {adaptive_plan['corrective_action']}")
            print(f"🎯 Strategy: {adaptive_plan['new_strategy']}")
            
            # Execute the adaptive plan
            if adaptive_plan['corrective_action'] == 'fix_existing':
                return self.apply_code_corrections(adaptive_plan, learning_context)
            elif adaptive_plan['corrective_action'] == 'create_new':
                return self.create_adaptive_tool(adaptive_plan, learning_context)
            else:
                print(f"❌ Unknown corrective action: {adaptive_plan['corrective_action']}")
                return False
                
        except Exception as e:
            print(f"❌ Adaptive learning failed: {e}")
            return False
    
    def apply_code_corrections(self, adaptive_plan, learning_context):
        """Apply specific code corrections based on adaptive learning"""
        print(f"🔧 Applying code corrections...")
        
        target_module = adaptive_plan['target_module']
        module_path = os.path.join(self.tools_dir, f"{target_module}.py")
        
        if not os.path.exists(module_path):
            print(f"❌ Target module {target_module} not found")
            return False
        
        with open(module_path, 'r') as f:
            current_code = f.read()
        
        prompt = f"""
Apply specific corrections to this code:

CURRENT CODE:
{current_code}

CORRECTIONS NEEDED:
{adaptive_plan['code_corrections']}

ADAPTIVE STRATEGY:
{adaptive_plan['new_strategy']}

Return the corrected code:
"""
        
        try:
            corrected_code = call_gpt_coding(prompt)  # Use coding model for code correction
            if corrected_code.startswith('```python'):
                corrected_code = corrected_code[9:]
            if corrected_code.endswith('```'):
                corrected_code = corrected_code[:-3]
            corrected_code = corrected_code.strip()
            
            with open(module_path, 'w') as f:
                f.write(corrected_code)
            
            print(f"✅ Code corrections applied to: {module_path}")
            return True
            
        except Exception as e:
            print(f"❌ Code correction failed: {e}")
            return False
    
    def create_adaptive_tool(self, adaptive_plan, learning_context):
        """Create a new tool using adaptive learning insights"""
        print(f"🛠️ Creating adaptive tool...")
        
        prompt = f"""
Create a new tool based on adaptive learning insights:

ADAPTIVE STRATEGY: {adaptive_plan['new_strategy']}
ORIGINAL CONTEXT: {learning_context}
LEARNED FROM FAILURE: {adaptive_plan['failure_analysis']}

Generate a robust Python tool that addresses the original failure and implements the adaptive strategy.

Return only the Python code:
"""
        
        try:
            tool_code = call_gpt_coding(prompt)  # Use coding model for adaptive tool generation
            if tool_code.startswith('```python'):
                tool_code = tool_code[9:]
            if tool_code.endswith('```'):
                tool_code = tool_code[:-3]
            tool_code = tool_code.strip()
            
            # Determine tool name from adaptive plan
            tool_name = adaptive_plan.get('target_module', 'adaptive_tool')
            tool_file = self.save_new_tool(tool_name, tool_code)
            
            if tool_file:
                print(f"✅ Adaptive tool created: {tool_file}")
                return True
            else:
                return False
                
        except Exception as e:
            print(f"❌ Adaptive tool creation failed: {e}")
            return False
    
    def learn_new_capability(self, user_request, current_capabilities):
        """
        BASIC LEARNING: Learn a new capability (fallback for simple cases)
        This is the original learning method for when intelligent learning isn't needed
        """
        print(f"🎓 Basic Learning: {user_request}")
        
        # Analyze what the user is asking for
        analysis = self.analyze_unknown_command(user_request, current_capabilities)
        
        if analysis['requires_new_tool']:
            print(f"📝 Generating new tool: {analysis['suggested_tool_name']}")
            
            # Generate the tool code
            tool_code = self.generate_tool_code(analysis)
            
            if tool_code:
                # Save the new tool
                tool_file = self.save_new_tool(analysis['suggested_tool_name'], tool_code)
                
                if tool_file:
                    print(f"✅ New capability learned and saved: {tool_file}")
                    
                    # Record this learning
                    self.record_learning(user_request, analysis, tool_file)
                    
                    return {
                        'success': True,
                        'tool_created': tool_file,
                        'capability': analysis['suggested_tool_name']
                    }
        
        print(f"❌ Failed to learn new capability")
        return {'success': False}
    
    def generate_contextual_tool(self, tool_analysis, learning_context):
        """Generate a tool with full context awareness"""
        print(f"🧠 Generating contextual tool with full awareness...")
        
        prompt = f"""
Generate a contextual tool that understands the full learning context:

TOOL ANALYSIS: {tool_analysis}
LEARNING CONTEXT: {learning_context}
USER'S ACTUAL INTENT: {tool_analysis['missing_capability']}

Create a Python tool that:
1. Addresses the user's exact intent
2. Handles the specific use case that failed
3. Integrates well with existing capabilities
4. Follows established patterns and conventions

Return the complete Python code:
"""
        
        try:
            tool_code = call_gpt(prompt)
            if tool_code.startswith('```python'):
                tool_code = tool_code[9:]
            if tool_code.endswith('```'):
                tool_code = tool_code[:-3]
            tool_code = tool_code.strip()
            
            tool_file = self.save_new_tool(tool_analysis['tool_name'], tool_code)
            return tool_file is not None
            
        except Exception as e:
            print(f"❌ Contextual tool generation failed: {e}")
            return False
    
    def generate_contextual_tool(self, tool_analysis, learning_context):
        """Generate a tool with full context awareness"""
        print(f"🧠 Generating contextual tool with full awareness...")
        
        prompt = f"""
Generate a contextual tool that understands the full learning context:

TOOL ANALYSIS: {tool_analysis}
LEARNING CONTEXT: {learning_context}
USER'S ACTUAL INTENT: {tool_analysis['missing_capability']}

Create a Python tool that:
1. Addresses the user's exact intent
2. Handles the specific use case that failed
3. Integrates well with existing capabilities
4. Follows established patterns and conventions

Return the complete Python code:
"""
        
        try:
            tool_code = call_gpt(prompt)
            if tool_code.startswith('```python'):
                tool_code = tool_code[9:]
            if tool_code.endswith('```'):
                tool_code = tool_code[:-3]
            tool_code = tool_code.strip()
            
            tool_file = self.save_new_tool(tool_analysis['tool_name'], tool_code)
            return tool_file is not None
            
        except Exception as e:
            print(f"❌ Contextual tool generation failed: {e}")
            return False
        """Complete learning process for new capability"""
        print(f"🧠 Learning new capability for: {user_request}")
        
        # Step 1: Analyze what's needed
        analysis = self.analyze_unknown_command(user_request, current_capabilities)
        if not analysis:
            return False
        
        print(f"📊 Analysis: {analysis['missing_capability']}")
        print(f"🔧 Generating tool: {analysis['tool_name']}")
        
        # Step 2: Generate tool code
        tool_code = self.generate_tool_code(analysis, user_request)
        if not tool_code:
            return False
        
        # Step 3: Save the tool
        tool_file = self.save_new_tool(analysis['tool_name'], tool_code)
        if not tool_file:
            return False
        
        # Step 4: Reload tools
        if not self.reload_tools():
            return False
        
        # Step 5: Record the learning
        self.record_learning(user_request, analysis, tool_file)
        
        print(f"🎉 Successfully learned new capability: {analysis['tool_name']}")
        return True
    
    def record_learning(self, original_request, analysis, tool_file):
        """Record what was learned for future reference"""
        learning_record = {
            "timestamp": datetime.now().isoformat(),
            "original_request": original_request,
            "tool_generated": analysis['tool_name'],
            "tool_file": tool_file,
            "capability_added": analysis['missing_capability'],
            "category": analysis['tool_category']
        }
        
        # Save to learning log
        log_file = "learning_log.json"
        try:
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    log_data = json.load(f)
            else:
                log_data = {"learned_tools": []}
            
            log_data["learned_tools"].append(learning_record)
            
            with open(log_file, 'w') as f:
                json.dump(log_data, f, indent=2)
                
            print(f"📚 Learning recorded in {log_file}")
        except Exception as e:
            print(f"⚠️ Failed to record learning: {e}")

# Global instance
tool_generator = ToolGenerator()
