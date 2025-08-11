#!/usr/bin/env python3
"""
🔍 CODE VALIDATOR
================
Validates syntax, execution, dependencies, and safety of generated code
"""

import ast
import subprocess
import tempfile
import os
import sys
import json
import time
import signal
from typing import Dict, List, Tuple, Optional
from contextlib import contextmanager

class CodeValidator:
    """Advanced code validation with safety checks and sandbox execution"""
    
    def __init__(self):
        self.max_execution_time = 10  # seconds
        self.allowed_imports = {
            'subprocess', 'os', 'sys', 'json', 'time', 'datetime', 
            'pathlib', 're', 'shutil', 'tempfile', 'typing',
            'collections', 'itertools', 'functools', 'math'
        }
        self.dangerous_functions = {
            'eval', 'exec', 'compile', '__import__', 'globals', 'locals',
            'getattr', 'setattr', 'delattr', 'hasattr'
        }
        self.dangerous_modules = {
            'socket', 'urllib', 'requests', 'http', 'ftplib', 'smtplib',
            'pickle', 'marshal', 'shelve', 'dbm'
        }
    
    def validate_syntax(self, code: str) -> Tuple[bool, Optional[str]]:
        """
        Validate Python syntax
        
        Args:
            code: Python code to validate
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            ast.parse(code)
            return True, None
        except SyntaxError as e:
            return False, f"Syntax error at line {e.lineno}: {e.msg}"
        except Exception as e:
            return False, f"Parse error: {str(e)}"
    
    def validate_security(self, code: str) -> Tuple[bool, List[str]]:
        """
        Validate code for security issues
        
        Args:
            code: Python code to validate
        
        Returns:
            Tuple of (is_safe, list_of_security_issues)
        """
        issues = []
        
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                # Check for dangerous function calls
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        if node.func.id in self.dangerous_functions:
                            issues.append(f"Dangerous function call: {node.func.id}")
                
                # Check for dangerous imports
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name in self.dangerous_modules:
                            issues.append(f"Dangerous import: {alias.name}")
                
                if isinstance(node, ast.ImportFrom):
                    if node.module in self.dangerous_modules:
                        issues.append(f"Dangerous import from: {node.module}")
                
                # Check for shell=True in subprocess calls
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                    if (node.func.attr in ['run', 'call', 'check_call', 'check_output'] and
                        any(keyword.arg == 'shell' and 
                            isinstance(keyword.value, ast.Constant) and 
                            keyword.value.value is True 
                            for keyword in node.keywords)):
                        issues.append("subprocess call with shell=True detected")
                
                # Check for file operations outside allowed paths
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    if node.func.id in ['open', 'file']:
                        # Check if path argument contains dangerous patterns
                        if node.args and isinstance(node.args[0], ast.Constant):
                            path = node.args[0].value
                            if isinstance(path, str):
                                if path.startswith('/etc/') or path.startswith('/System/'):
                                    issues.append(f"Dangerous file access: {path}")
        
        except Exception as e:
            issues.append(f"Security analysis failed: {str(e)}")
        
        return len(issues) == 0, issues
    
    def validate_dependencies(self, code: str) -> Tuple[bool, List[str]]:
        """
        Validate that all required dependencies are available
        
        Args:
            code: Python code to validate
        
        Returns:
            Tuple of (all_available, list_of_missing_dependencies)
        """
        missing_deps = []
        
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                # Check imports
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if not self._check_module_available(alias.name):
                            missing_deps.append(alias.name)
                
                if isinstance(node, ast.ImportFrom):
                    if node.module and not self._check_module_available(node.module):
                        missing_deps.append(node.module)
        
        except Exception as e:
            missing_deps.append(f"dependency_check_failed: {str(e)}")
        
        return len(missing_deps) == 0, missing_deps
    
    def _check_module_available(self, module_name: str) -> bool:
        """Check if a module is available for import"""
        try:
            __import__(module_name)
            return True
        except ImportError:
            return False
    
    @contextmanager
    def timeout_context(self, seconds: int):
        """Context manager for timeout execution"""
        def timeout_handler(signum, frame):
            raise TimeoutError(f"Execution timed out after {seconds} seconds")
        
        # Set up the timeout
        old_handler = signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(seconds)
        
        try:
            yield
        finally:
            # Clean up
            signal.alarm(0)
            signal.signal(signal.SIGALRM, old_handler)
    
    def validate_execution(self, code: str, test_cases: List[Dict] = None) -> Tuple[bool, str]:
        """
        Validate code execution in a sandboxed environment
        
        Args:
            code: Python code to execute
            test_cases: Optional test cases to run
        
        Returns:
            Tuple of (execution_successful, result_or_error_message)
        """
        
        # First validate syntax and security
        syntax_valid, syntax_error = self.validate_syntax(code)
        if not syntax_valid:
            return False, f"Syntax validation failed: {syntax_error}"
        
        security_valid, security_issues = self.validate_security(code)
        if not security_valid:
            return False, f"Security validation failed: {'; '.join(security_issues)}"
        
        # Create temporary file for execution
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp_file:
                tmp_file.write(code)
                tmp_file.flush()
                
                # Test basic execution
                try:
                    with self.timeout_context(self.max_execution_time):
                        result = subprocess.run(
                            [sys.executable, '-c', f'import sys; sys.path.insert(0, "{os.path.dirname(tmp_file.name)}"); exec(open("{tmp_file.name}").read())'],
                            capture_output=True,
                            text=True,
                            timeout=self.max_execution_time
                        )
                    
                    if result.returncode != 0:
                        return False, f"Execution failed: {result.stderr}"
                    
                    # If test cases provided, run them
                    if test_cases:
                        test_results = self._run_test_cases(tmp_file.name, test_cases)
                        if not test_results['all_passed']:
                            return False, f"Test cases failed: {test_results['failures']}"
                    
                    return True, result.stdout or "Execution successful"
                
                except TimeoutError as e:
                    return False, str(e)
                except subprocess.TimeoutExpired:
                    return False, f"Execution timed out after {self.max_execution_time} seconds"
                except Exception as e:
                    return False, f"Execution error: {str(e)}"
                
        except Exception as e:
            return False, f"Validation setup failed: {str(e)}"
        
        finally:
            # Clean up temporary file
            try:
                os.unlink(tmp_file.name)
            except:
                pass
    
    def _run_test_cases(self, code_file: str, test_cases: List[Dict]) -> Dict:
        """Run test cases against the code"""
        results = {
            'all_passed': True,
            'total_tests': len(test_cases),
            'passed': 0,
            'failed': 0,
            'failures': []
        }
        
        for i, test_case in enumerate(test_cases):
            try:
                # Create test script
                test_script = f"""
import sys
import os
sys.path.insert(0, '{os.path.dirname(code_file)}')

# Import the generated module
import importlib.util
spec = importlib.util.spec_from_file_location("test_module", "{code_file}")
test_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(test_module)

# Run the test
try:
    # Find the main function to test
    test_params = {test_case.get('input_params', {})}
    
    # Try to find and execute the main function
    for attr_name in dir(test_module):
        attr = getattr(test_module, attr_name)
        if callable(attr) and not attr_name.startswith('_'):
            if test_params:
                result = attr(**test_params)
            else:
                result = attr()
            print(f"TEST_RESULT: {{result}}")
            break
    else:
        print("TEST_ERROR: No callable function found")
        
except Exception as e:
    print(f"TEST_ERROR: {{str(e)}}")
"""
                
                test_result = subprocess.run(
                    [sys.executable, '-c', test_script],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                if test_result.returncode == 0 and 'TEST_RESULT:' in test_result.stdout:
                    results['passed'] += 1
                else:
                    results['failed'] += 1
                    results['all_passed'] = False
                    results['failures'].append({
                        'test_name': test_case.get('test_name', f'test_{i}'),
                        'error': test_result.stderr or 'Unknown error'
                    })
                    
            except Exception as e:
                results['failed'] += 1
                results['all_passed'] = False
                results['failures'].append({
                    'test_name': test_case.get('test_name', f'test_{i}'),
                    'error': str(e)
                })
        
        return results
    
    def validate_macos_compatibility(self, code: str) -> Tuple[bool, List[str]]:
        """
        Validate macOS compatibility of the code
        
        Args:
            code: Python code to validate
        
        Returns:
            Tuple of (is_compatible, list_of_compatibility_issues)
        """
        issues = []
        
        # Check for macOS-specific commands
        macos_commands = {
            'osascript', 'blueutil', 'open', 'say', 'networksetup',
            'pmset', 'screencapture', 'diskutil', 'system_profiler'
        }
        
        # Check for Windows-specific patterns
        windows_patterns = [
            'cmd.exe', 'powershell', 'wmic', 'reg.exe', 'tasklist',
            'C:\\', '\\windows\\', 'HKEY_'
        ]
        
        # Check for Linux-specific patterns
        linux_patterns = [
            'apt-get', 'yum', 'systemctl', 'ps aux', '/proc/',
            '/etc/passwd', '/var/log/', 'sudo '
        ]
        
        code_lower = code.lower()
        
        for pattern in windows_patterns:
            if pattern.lower() in code_lower:
                issues.append(f"Windows-specific pattern detected: {pattern}")
        
        for pattern in linux_patterns:
            if pattern.lower() in code_lower:
                issues.append(f"Linux-specific pattern detected: {pattern}")
        
        # Check for proper macOS command usage
        has_macos_commands = any(cmd in code_lower for cmd in macos_commands)
        
        # Only flag as issue if subprocess is used with Windows/Linux specific patterns
        # Generic subprocess usage is acceptable
        if 'subprocess' in code and not has_macos_commands:
            # Check if it's actually problematic (using non-macOS commands)
            has_problematic_commands = any(pattern.lower() in code_lower for pattern in windows_patterns + linux_patterns)
            if has_problematic_commands:
                issues.append("Uses subprocess with non-macOS commands")
            # Generic subprocess usage is fine, don't flag it
        
        return len(issues) == 0, issues
    
    def validate_resource_usage(self, code: str) -> Tuple[bool, List[str]]:
        """
        Validate that code doesn't use excessive resources
        
        Args:
            code: Python code to validate
        
        Returns:
            Tuple of (resource_usage_ok, list_of_resource_issues)
        """
        issues = []
        
        try:
            tree = ast.parse(code)
            
            # Check for potential memory issues
            for node in ast.walk(tree):
                # Large list comprehensions
                if isinstance(node, ast.ListComp):
                    issues.append("Large list comprehension detected - consider using generators")
                
                # Infinite loops
                if isinstance(node, ast.While):
                    if isinstance(node.test, ast.Constant) and node.test.value is True:
                        issues.append("Infinite loop detected: while True")
                
                # Large file operations
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                    if node.func.attr == 'read' and not any(
                        keyword.arg in ['size', 'n'] for keyword in node.keywords
                    ):
                        issues.append("Unbounded file read operation")
        
        except Exception as e:
            issues.append(f"Resource analysis failed: {str(e)}")
        
        return len(issues) == 0, issues
    
    def comprehensive_validation(self, code: str, test_cases: List[Dict] = None) -> Dict:
        """
        Run comprehensive validation including all checks
        
        Args:
            code: Python code to validate
            test_cases: Optional test cases to run
        
        Returns:
            Dict with comprehensive validation results
        """
        
        results = {
            'overall_valid': True,
            'validation_results': {}
        }
        
        # Syntax validation
        syntax_valid, syntax_error = self.validate_syntax(code)
        results['validation_results']['syntax'] = {
            'valid': syntax_valid,
            'error': syntax_error
        }
        if not syntax_valid:
            results['overall_valid'] = False
        
        # Security validation
        security_valid, security_issues = self.validate_security(code)
        results['validation_results']['security'] = {
            'valid': security_valid,
            'issues': security_issues
        }
        if not security_valid:
            results['overall_valid'] = False
        
        # Dependency validation
        deps_valid, missing_deps = self.validate_dependencies(code)
        results['validation_results']['dependencies'] = {
            'valid': deps_valid,
            'missing': missing_deps
        }
        if not deps_valid:
            results['overall_valid'] = False
        
        # macOS compatibility validation (warnings only, not blocking)
        macos_valid, macos_issues = self.validate_macos_compatibility(code)
        results['validation_results']['macos_compatibility'] = {
            'valid': macos_valid,
            'issues': macos_issues
        }
        # Don't fail overall validation for macOS compatibility issues
        # if not macos_valid:
        #     results['overall_valid'] = False
        
        # Resource usage validation (warnings only, not blocking)
        resource_valid, resource_issues = self.validate_resource_usage(code)
        results['validation_results']['resource_usage'] = {
            'valid': resource_valid,
            'issues': resource_issues
        }
        # Don't fail overall validation for resource usage warnings
        # Resource issues are just optimization suggestions
        
        # Execution validation (only if other validations pass)
        if results['overall_valid']:
            exec_valid, exec_result = self.validate_execution(code, test_cases)
            results['validation_results']['execution'] = {
                'valid': exec_valid,
                'result': exec_result
            }
            if not exec_valid:
                results['overall_valid'] = False
        
        return results
