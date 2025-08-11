#!/usr/bin/env python3
"""
🛠️ CODE GENERATOR
================
Creates new tools, updates existing code, and generates test cases
"""

import os
import sys
import json
import ast
import tempfile
from typing import Dict, List, Any, Optional

# Import specialized GPT interface
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from utils.gpt_interface import call_gpt_coding, call_gpt_learning

class CodeGenerator:
    """Advanced code generation for autonomous capability development"""
    
    def __init__(self):
        self.templates_dir = os.path.join(os.path.dirname(__file__), "..", "dynamic_tools")
        self.tools_dir = os.path.join(os.path.dirname(__file__), "..", "tools")
        self._ensure_directories()
        self._load_tool_template()
    
    def _ensure_directories(self):
        """Ensure required directories exist"""
        os.makedirs(self.templates_dir, exist_ok=True)
        os.makedirs(self.tools_dir, exist_ok=True)
    
    def _load_tool_template(self):
        """Load the tool template for consistent code generation"""
        template_path = os.path.join(self.templates_dir, "tool_template.py")
        
        if not os.path.exists(template_path):
            # Create the template if it doesn't exist
            template_content = '''#!/usr/bin/env python3
"""
AUTO-GENERATED TOOL TEMPLATE
===========================
This template provides the structure for all auto-generated tools
"""

import subprocess
import os
from datetime import datetime
from typing import Optional, Dict, Any

def execute_template(params: dict = None) -> dict:
    """
    Template function for auto-generated tools
    
    Args:
        params: Dictionary of parameters for the tool
    
    Returns:
        dict: Result with success status and output/error
    """
    try:
        # Implementation will be auto-generated here
        result = {"success": True, "output": "Template executed successfully"}
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}

# Tool metadata (auto-populated)
TOOL_METADATA = {
    "name": "template_tool",
    "category": "utility",
    "description": "Auto-generated tool template",
    "version": "1.0.0",
    "auto_generated": True,
    "created_at": datetime.now().isoformat()
}
'''
            with open(template_path, 'w') as f:
                f.write(template_content)
        
        with open(template_path, 'r') as f:
            self.tool_template = f.read()
    
    def generate_tool(self, requirements: Dict[str, Any]) -> Optional[str]:
        """
        Generate a complete Python tool based on requirements
        
        Args:
            requirements: Dictionary containing tool specifications
        
        Returns:
            str: Generated Python code or None if generation failed
        """
        
        # Load macOS-specific patterns and commands
        macos_patterns = self._load_macos_patterns()
        
        prompt = f"""
TASK: Create a macOS Python tool for the Chotu AI Assistant

SYSTEM CONTEXT:
- OS: macOS (latest version)
- Python: Python 3.9+
- Architecture: MCP (Model Context Protocol) tool system
- Location: Will be saved as /Users/mahendrabahubali/chotu/mcp/dynamic_tools/{{tool_name}}.py

SPECIFIC REQUIREMENTS:
Tool Name: {requirements.get('name', 'unknown_tool')}
Category: {requirements.get('category', 'unknown')}
Purpose: {requirements.get('description', 'No description provided')}
User Goal: {requirements.get('user_goal', 'No goal specified')}

TECHNICAL SPECIFICATIONS:
{json.dumps(requirements.get('technical_requirements', {}), indent=2)}

SAFETY REQUIREMENTS:
{requirements.get('safety_considerations', ['Standard safety practices'])}

SUCCESS CRITERIA (Must implement these test scenarios):
{requirements.get('test_scenarios', ['Basic functionality test'])}

MACOS COMMAND PATTERNS (Use these specific commands):
{json.dumps(macos_patterns, indent=2)}

EXACT TEMPLATE TO FOLLOW:
{self.tool_template}

OUTPUT REQUIREMENTS:
1. Return ONLY executable Python code (no markdown, no explanations)
2. Start with #!/usr/bin/env python3
3. Include complete imports at the top
4. Follow the template structure exactly
5. Implement ALL test scenarios as functions
6. Use only the macOS patterns provided above
7. Include proper error handling with try/except
8. Return consistent dict format: {{"status": "success/error", "message": "...", "data": {{}}}}

IMPLEMENTATION RULES:
- Function names must be descriptive and snake_case
- All functions must have type hints
- Include docstrings for all functions
- Use subprocess.run() for system commands
- Validate all inputs
- Handle timeouts and errors gracefully
- Log important actions
- Never use os.system() or shell=True

Generate the complete tool code now:"""
        
        try:
            code = call_gpt_coding(prompt)
            
            # Clean the generated code
            code = self._clean_generated_code(code)
            
            # Validate the generated code
            if self._validate_generated_code(code):
                return code
            else:
                print("❌ Generated code failed validation")
                return None
                
        except Exception as e:
            print(f"❌ Tool generation failed: {e}")
            return None
    
    def _load_macos_patterns(self) -> Dict[str, Any]:
        """Load macOS-specific command patterns and best practices"""
        return {
            "volume_control": {
                "command": "osascript -e 'set volume output volume {level}'",
                "level_range": "0-100",
                "example": "osascript -e 'set volume output volume 50'"
            },
            "brightness_control": {
                "command": "osascript -e 'tell application \"System Events\" to tell every desktop to set brightness to {level}'",
                "level_range": "0.0-1.0",
                "example": "osascript -e 'tell application \"System Events\" to tell every desktop to set brightness to 0.5'"
            },
            "application_control": {
                "open": "open -a '{app_name}'",
                "close": "osascript -e 'tell app \"{app_name}\" to quit'",
                "example": "open -a 'Safari'"
            },
            "file_operations": {
                "create_folder": "mkdir -p '{path}'",
                "open_folder": "open '{path}'",
                "delete": "rm -rf '{path}'",
                "copy": "cp -r '{source}' '{destination}'"
            },
            "system_info": {
                "battery": "pmset -g batt",
                "cpu_usage": "top -l 1 -n 0 | grep 'CPU usage'",
                "memory": "vm_stat",
                "disk_space": "df -h"
            },
            "bluetooth": {
                "status": "blueutil -p",
                "enable": "blueutil -p 1",
                "disable": "blueutil -p 0",
                "list_devices": "blueutil --paired"
            },
            "network": {
                "wifi_status": "networksetup -getairportpower en0",
                "wifi_networks_scan": "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s",
                "wifi_networks_preferred": "networksetup -listpreferredwirelessnetworks 'Wi-Fi'",
                "wifi_interface_info": "networksetup -listallhardwareports | grep -A 1 Wi-Fi",
                "network_interfaces": "networksetup -listallhardwareports",
                "ip_address": "ifconfig | grep 'inet '",
                "current_network": "networksetup -getairportnetwork en0",
                "examples": {
                    "scan_wifi": "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s",
                    "check_wifi_power": "networksetup -getairportpower en0",
                    "get_current_network": "networksetup -getairportnetwork en0"
                }
            },
            "screenshot": {
                "full_screen": "screencapture '{filename}'",
                "selection": "screencapture -s '{filename}'",
                "window": "screencapture -w '{filename}'"
            },
            "notification": {
                "display": "osascript -e 'display notification \"{message}\" with title \"{title}\"'"
            },
            "email_systems": {
                "gmail_smtp": {
                    "server": "smtp.gmail.com",
                    "port": 587,
                    "security": "TLS",
                    "auth_method": "app_password",
                    "requirements": [
                        "2FA enabled on Gmail account",
                        "App-specific password generated",
                        "SMTP access enabled"
                    ],
                    "python_modules": ["smtplib", "email.mime.text", "email.mime.multipart", "ssl"],
                    "connection_steps": [
                        "Create SMTP connection to smtp.gmail.com:587",
                        "Start TLS encryption",
                        "Login with email and app password",
                        "Send message",
                        "Close connection"
                    ]
                },
                "system_email": {
                    "macos_mail": "open 'mailto:recipient@domain.com?subject=Subject&body=Body'",
                    "command_line": "echo 'message' | mail -s 'subject' recipient@domain.com",
                    "requirements": ["Mail.app configured", "SMTP server configured in system"]
                },
                "troubleshooting": {
                    "localhost_smtp_fails": "Connection refused error indicates no local SMTP server",
                    "gmail_auth_fails": "Check app password and 2FA settings",
                    "connection_timeout": "Check network connectivity and firewall",
                    "ssl_errors": "Verify TLS/SSL support and certificates"
                }
            }
        }
    
    def _clean_generated_code(self, code: str) -> str:
        """Clean and format generated code"""
        # Remove markdown code blocks (handle various formats)
        if code.startswith('````python'):
            code = code[10:]
        elif code.startswith('```python'):
            code = code[9:]
        elif code.startswith('````'):
            code = code[4:]
        elif code.startswith('```'):
            code = code[3:]
        
        if code.endswith('````'):
            code = code[:-4]
        elif code.endswith('```'):
            code = code[:-3]
        
        # Remove extra whitespace
        code = code.strip()
        
        # Ensure proper imports
        if not code.startswith('#!/usr/bin/env python3'):
            code = '#!/usr/bin/env python3\n' + code
        
        return code
    
    def _validate_generated_code(self, code: str) -> bool:
        """Validate generated code for syntax and basic structure"""
        try:
            # Check syntax
            ast.parse(code)
            
            # Check for required elements
            required_elements = [
                'import subprocess',
                'def ',
                'return ',
                'except Exception'
            ]
            
            for element in required_elements:
                if element not in code:
                    print(f"❌ Missing required element: {element}")
                    return False
            
            # Check for dangerous patterns
            dangerous_patterns = [
                'os.system(',
                'eval(',
                'exec(',
                'shell=True'
            ]
            
            for pattern in dangerous_patterns:
                if pattern in code:
                    print(f"❌ Dangerous pattern detected: {pattern}")
                    return False
            
            return True
            
        except SyntaxError as e:
            print(f"❌ Syntax error in generated code: {e}")
            
            # Save the problematic code for debugging
            debug_file = "/Users/mahendrabahubali/chotu/debug_generated_code.py"
            try:
                with open(debug_file, 'w') as f:
                    f.write(code)
                print(f"🐛 Debug: Generated code saved to {debug_file}")
                print(f"🐛 Error details: Line {e.lineno}, {e.msg}")
            except Exception as save_error:
                print(f"🐛 Could not save debug code: {save_error}")
            
            return False
    
    def update_existing_tool(self, tool_path: str, enhancement_requirements: Dict) -> Optional[str]:
        """
        Update an existing tool with new functionality
        
        Args:
            tool_path: Path to the existing tool file
            enhancement_requirements: Requirements for the enhancement
        
        Returns:
            str: Updated code or None if update failed
        """
        
        if not os.path.exists(tool_path):
            print(f"❌ Tool file not found: {tool_path}")
            return None
        
        # Read existing code
        with open(tool_path, 'r') as f:
            existing_code = f.read()
        
        prompt = f"""
You are enhancing an existing Python tool. Add new functionality while maintaining backward compatibility.

EXISTING CODE:
{existing_code}

ENHANCEMENT REQUIREMENTS:
{json.dumps(enhancement_requirements, indent=2)}

ENHANCEMENT RULES:
1. Preserve all existing functionality
2. Add new functions without breaking existing ones
3. Follow the same coding style and patterns
4. Update docstrings and metadata
5. Add comprehensive error handling for new features
6. Maintain the same return format consistency
7. Add version information for the enhancement

Return the complete enhanced code:
"""
        
        try:
            enhanced_code = call_gpt_coding(prompt)
            enhanced_code = self._clean_generated_code(enhanced_code)
            
            if self._validate_enhanced_code(existing_code, enhanced_code):
                return enhanced_code
            else:
                print("❌ Enhanced code failed validation")
                return None
                
        except Exception as e:
            print(f"❌ Tool enhancement failed: {e}")
            return None
    
    def _validate_enhanced_code(self, original_code: str, enhanced_code: str) -> bool:
        """Validate that enhanced code maintains backward compatibility"""
        try:
            # Check syntax
            ast.parse(enhanced_code)
            
            # Extract function names from original code
            original_tree = ast.parse(original_code)
            original_functions = {node.name for node in ast.walk(original_tree) if isinstance(node, ast.FunctionDef)}
            
            # Extract function names from enhanced code
            enhanced_tree = ast.parse(enhanced_code)
            enhanced_functions = {node.name for node in ast.walk(enhanced_tree) if isinstance(node, ast.FunctionDef)}
            
            # Check that all original functions are preserved
            missing_functions = original_functions - enhanced_functions
            if missing_functions:
                print(f"❌ Enhanced code missing original functions: {missing_functions}")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Enhanced code validation failed: {e}")
            return False
    
    def generate_test_cases(self, tool_code: str, requirements: Dict) -> List[Dict]:
        """
        Generate comprehensive test cases for a tool
        
        Args:
            tool_code: The tool code to generate tests for
            requirements: Original requirements for context
        
        Returns:
            List of test case dictionaries
        """
        
        prompt = f"""
Generate comprehensive test cases for this Python tool.

TOOL CODE:
{tool_code}

ORIGINAL REQUIREMENTS:
{json.dumps(requirements, indent=2)}

Generate test cases that cover:
1. Normal operation scenarios
2. Edge cases and boundary conditions
3. Error conditions and exception handling
4. Parameter validation
5. System integration tests
6. Performance considerations

Return as JSON array:
[
    {{
        "test_name": "descriptive_test_name",
        "description": "what this test validates",
        "test_type": "unit|integration|error|performance",
        "input_params": {{"param": "value"}},
        "expected_outcome": "success|error|specific_result",
        "validation_criteria": "how to determine if test passed",
        "setup_required": "any setup steps needed",
        "cleanup_required": "any cleanup steps needed"
    }}
]
"""
        
        try:
            response = call_gpt_learning(prompt)
            
            # Clean and parse JSON
            response = response.strip()
            if response.startswith('```json'):
                response = response[7:]
            if response.endswith('```'):
                response = response[:-3]
            
            test_cases = json.loads(response.strip())
            return test_cases
            
        except Exception as e:
            print(f"❌ Test case generation failed: {e}")
            return []
    
    def generate_documentation(self, tool_code: str, requirements: Dict) -> str:
        """
        Generate comprehensive documentation for a tool
        
        Args:
            tool_code: The tool code to document
            requirements: Original requirements for context
        
        Returns:
            str: Generated documentation in markdown format
        """
        
        prompt = f"""
Generate comprehensive documentation for this auto-generated tool.

TOOL CODE:
{tool_code}

REQUIREMENTS CONTEXT:
{json.dumps(requirements, indent=2)}

Generate documentation that includes:
1. Tool overview and purpose
2. Function signatures and parameters
3. Usage examples
4. Error handling and troubleshooting
5. Dependencies and requirements
6. Security considerations
7. Version history
8. Known limitations

Format as markdown:
"""
        
        try:
            documentation = call_gpt_learning(prompt)
            return documentation
            
        except Exception as e:
            print(f"❌ Documentation generation failed: {e}")
            return f"# Documentation Generation Failed\n\nError: {e}"
    
    def create_tool_package(self, tool_name: str, tool_code: str, requirements: Dict) -> Dict[str, str]:
        """
        Create a complete tool package with code, tests, and documentation
        
        Args:
            tool_name: Name of the tool
            tool_code: Generated tool code
            requirements: Original requirements
        
        Returns:
            Dict containing all generated files
        """
        
        package = {
            'tool_code': tool_code,
            'test_cases': json.dumps(self.generate_test_cases(tool_code, requirements), indent=2),
            'documentation': self.generate_documentation(tool_code, requirements),
            'metadata': json.dumps({
                'name': tool_name,
                'version': '1.0.0',
                'auto_generated': True,
                'created_at': __import__('datetime').datetime.now().isoformat(),
                'requirements': requirements,
                'generator_version': '2.0'
            }, indent=2)
        }
        
        return package
    
    def save_tool_package(self, tool_name: str, package: Dict[str, str]) -> bool:
        """
        Save a complete tool package to the filesystem
        
        Args:
            tool_name: Name of the tool
            package: Package dictionary from create_tool_package
        
        Returns:
            bool: True if saved successfully
        """
        
        try:
            # Save tool code
            tool_path = os.path.join(self.tools_dir, f"{tool_name}.py")
            with open(tool_path, 'w') as f:
                f.write(package['tool_code'])
            
            # Save metadata
            metadata_path = os.path.join(self.tools_dir, f"{tool_name}_metadata.json")
            with open(metadata_path, 'w') as f:
                f.write(package['metadata'])
            
            # Save test cases
            tests_path = os.path.join(self.tools_dir, f"{tool_name}_tests.json")
            with open(tests_path, 'w') as f:
                f.write(package['test_cases'])
            
            # Save documentation
            docs_path = os.path.join(self.tools_dir, f"{tool_name}_docs.md")
            with open(docs_path, 'w') as f:
                f.write(package['documentation'])
            
            print(f"✅ Tool package saved:")
            print(f"   Code: {tool_path}")
            print(f"   Metadata: {metadata_path}")
            print(f"   Tests: {tests_path}")
            print(f"   Docs: {docs_path}")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to save tool package: {e}")
            return False
