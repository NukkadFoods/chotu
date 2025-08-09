#!/usr/bin/env python3
"""
🔒 SANDBOX EXECUTOR
==================
Isolated test environment with resource limits, network restrictions, and timeout protection
"""

import os
import sys
import subprocess
import tempfile
import resource
import signal
import threading
import time
import json
import shutil
from typing import Dict, List, Optional, Any, Tuple
from contextlib import contextmanager

class SandboxExecutor:
    """Advanced sandbox execution environment for safe code testing"""
    
    def __init__(self):
        self.max_execution_time = 30  # seconds
        self.max_memory_mb = 100  # MB
        self.max_cpu_time = 10  # seconds
        self.temp_dir = None
        
        # Restricted environment variables
        self.safe_env_vars = {
            'PATH': '/usr/bin:/bin',
            'PYTHONPATH': '',
            'HOME': '/tmp',
            'USER': 'sandbox',
            'SHELL': '/bin/sh'
        }
        
        # Allowed system calls (basic subset)
        self.allowed_syscalls = {
            'read', 'write', 'open', 'close', 'stat', 'fstat', 'lstat',
            'mmap', 'munmap', 'brk', 'rt_sigaction', 'rt_sigprocmask',
            'ioctl', 'access', 'pipe', 'select', 'mremap', 'msync',
            'mincore', 'madvise', 'shmget', 'shmat', 'shmctl'
        }
    
    def create_sandbox_environment(self) -> str:
        """
        Create isolated sandbox environment
        
        Returns:
            str: Path to sandbox directory
        """
        
        try:
            # Create temporary directory for sandbox
            self.temp_dir = tempfile.mkdtemp(prefix='chotu_sandbox_')
            
            # Create subdirectories
            os.makedirs(os.path.join(self.temp_dir, 'workspace'), exist_ok=True)
            os.makedirs(os.path.join(self.temp_dir, 'output'), exist_ok=True)
            os.makedirs(os.path.join(self.temp_dir, 'logs'), exist_ok=True)
            
            # Set restrictive permissions
            os.chmod(self.temp_dir, 0o755)
            
            print(f"🔒 Sandbox environment created: {self.temp_dir}")
            return self.temp_dir
            
        except Exception as e:
            print(f"❌ Failed to create sandbox: {e}")
            raise
    
    def cleanup_sandbox(self):
        """Clean up sandbox environment"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
                print(f"🗑️ Sandbox cleaned up: {self.temp_dir}")
            except Exception as e:
                print(f"⚠️ Failed to cleanup sandbox: {e}")
    
    @contextmanager
    def resource_limits(self):
        """Context manager for setting resource limits"""
        try:
            # Set memory limit
            memory_limit = self.max_memory_mb * 1024 * 1024  # Convert to bytes
            resource.setrlimit(resource.RLIMIT_AS, (memory_limit, memory_limit))
            
            # Set CPU time limit
            resource.setrlimit(resource.RLIMIT_CPU, (self.max_cpu_time, self.max_cpu_time))
            
            # Set file size limit
            resource.setrlimit(resource.RLIMIT_FSIZE, (1024*1024, 1024*1024))  # 1MB
            
            # Set number of open files limit
            resource.setrlimit(resource.RLIMIT_NOFILE, (64, 64))
            
            yield
            
        except Exception as e:
            print(f"⚠️ Failed to set resource limits: {e}")
            yield
        finally:
            # Reset limits (best effort)
            try:
                resource.setrlimit(resource.RLIMIT_AS, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))
                resource.setrlimit(resource.RLIMIT_CPU, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))
            except:
                pass
    
    def execute_code_in_sandbox(self, code: str, test_params: Dict = None) -> Dict[str, Any]:
        """
        Execute code in sandboxed environment
        
        Args:
            code: Python code to execute
            test_params: Parameters to pass to the code
        
        Returns:
            Dict: Execution results
        """
        
        sandbox_dir = None
        result = {
            'success': False,
            'output': '',
            'error': '',
            'execution_time': 0,
            'memory_used': 0,
            'exit_code': -1,
            'timeout': False,
            'resource_exceeded': False
        }
        
        try:
            # Create sandbox environment
            sandbox_dir = self.create_sandbox_environment()
            
            # Create code file in sandbox
            code_file = os.path.join(sandbox_dir, 'workspace', 'test_code.py')
            with open(code_file, 'w') as f:
                f.write(code)
            
            # Create test parameters file if provided
            if test_params:
                params_file = os.path.join(sandbox_dir, 'workspace', 'test_params.json')
                with open(params_file, 'w') as f:
                    json.dump(test_params, f)
            
            # Execute in sandbox
            start_time = time.time()
            execution_result = self._execute_with_monitoring(sandbox_dir, code_file, test_params)
            execution_time = time.time() - start_time
            
            result.update(execution_result)
            result['execution_time'] = execution_time
            
            return result
            
        except Exception as e:
            result['error'] = f"Sandbox execution failed: {str(e)}"
            return result
            
        finally:
            # Cleanup
            if sandbox_dir:
                self.cleanup_sandbox()
    
    def _execute_with_monitoring(self, sandbox_dir: str, code_file: str, test_params: Dict = None) -> Dict:
        """Execute code with comprehensive monitoring"""
        
        result = {
            'success': False,
            'output': '',
            'error': '',
            'exit_code': -1,
            'timeout': False,
            'resource_exceeded': False,
            'memory_used': 0
        }
        
        # Prepare execution command
        python_cmd = [
            sys.executable, 
            '-c',
            f'''
import sys
import os
import json
import resource
import traceback

# Change to sandbox workspace
os.chdir("{os.path.join(sandbox_dir, 'workspace')}")

# Load test parameters if available
test_params = None
if os.path.exists("test_params.json"):
    with open("test_params.json", "r") as f:
        test_params = json.load(f)

try:
    # Import and execute the code
    with open("test_code.py", "r") as f:
        code_content = f.read()
    
    # Create execution namespace
    exec_namespace = {{"__name__": "__main__", "test_params": test_params}}
    
    # Execute the code
    exec(code_content, exec_namespace)
    
    # Try to find and call main functions
    for name, obj in exec_namespace.items():
        if callable(obj) and not name.startswith("_"):
            try:
                if test_params:
                    result = obj(**test_params)
                else:
                    result = obj()
                print(f"FUNCTION_RESULT: {{result}}")
                break
            except TypeError:
                # Function might not accept parameters
                try:
                    result = obj()
                    print(f"FUNCTION_RESULT: {{result}}")
                    break
                except:
                    continue
            except Exception as e:
                print(f"FUNCTION_ERROR: {{str(e)}}")
                break
    
    print("EXECUTION_SUCCESS")
    
except Exception as e:
    print(f"EXECUTION_ERROR: {{str(e)}}")
    traceback.print_exc()
    sys.exit(1)
'''
        ]
        
        try:
            # Execute with timeout and monitoring
            process = subprocess.Popen(
                python_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=self.safe_env_vars,
                cwd=sandbox_dir,
                preexec_fn=self._setup_child_process
            )
            
            # Monitor execution with timeout
            try:
                stdout, stderr = process.communicate(timeout=self.max_execution_time)
                result['exit_code'] = process.returncode
                result['output'] = stdout
                result['error'] = stderr
                
                if process.returncode == 0 and 'EXECUTION_SUCCESS' in stdout:
                    result['success'] = True
                
            except subprocess.TimeoutExpired:
                process.kill()
                result['timeout'] = True
                result['error'] = f"Execution timed out after {self.max_execution_time} seconds"
                
                # Try to get partial output
                try:
                    stdout, stderr = process.communicate(timeout=1)
                    result['output'] = stdout
                    if stderr:
                        result['error'] += f"\nPartial stderr: {stderr}"
                except:
                    pass
            
            return result
            
        except Exception as e:
            result['error'] = f"Process execution failed: {str(e)}"
            return result
    
    def _setup_child_process(self):
        """Setup child process with security restrictions"""
        try:
            # Set resource limits
            memory_limit = self.max_memory_mb * 1024 * 1024
            resource.setrlimit(resource.RLIMIT_AS, (memory_limit, memory_limit))
            resource.setrlimit(resource.RLIMIT_CPU, (self.max_cpu_time, self.max_cpu_time))
            resource.setrlimit(resource.RLIMIT_FSIZE, (1024*1024, 1024*1024))
            resource.setrlimit(resource.RLIMIT_NOFILE, (32, 32))
            
            # Set process group (for easier cleanup)
            os.setpgrp()
            
        except Exception as e:
            print(f"⚠️ Failed to setup child process restrictions: {e}")
    
    def validate_code_safety(self, code: str) -> Tuple[bool, List[str]]:
        """
        Validate code for sandbox safety
        
        Args:
            code: Python code to validate
        
        Returns:
            Tuple of (is_safe, list_of_safety_issues)
        """
        
        issues = []
        
        # Check for dangerous imports
        dangerous_imports = [
            'socket', 'urllib', 'requests', 'http', 'ftplib', 'smtplib',
            'subprocess', 'os.system', 'eval', 'exec', 'compile',
            'pickle', 'marshal', 'shelve', 'ctypes', '__import__'
        ]
        
        for dangerous in dangerous_imports:
            if dangerous in code:
                issues.append(f"Dangerous import/function: {dangerous}")
        
        # Check for file system access outside allowed paths
        file_operations = ['open(', 'file(', 'os.path', 'pathlib', 'shutil']
        for op in file_operations:
            if op in code:
                # This is a warning, not necessarily dangerous in sandbox
                issues.append(f"File operation detected: {op} (will be sandboxed)")
        
        # Check for network operations
        network_operations = ['socket', 'urllib', 'requests', 'http', 'ftp']
        for net_op in network_operations:
            if net_op in code:
                issues.append(f"Network operation: {net_op} (blocked in sandbox)")
        
        # Check for infinite loops
        if 'while True:' in code and 'break' not in code:
            issues.append("Potential infinite loop detected")
        
        # Check for large data structures
        if any(pattern in code for pattern in ['range(1000000', '[0] * 1000000', 'list(range(']):
            issues.append("Large data structure creation detected")
        
        return len(issues) == 0, issues
    
    def run_security_scan(self, code: str) -> Dict[str, Any]:
        """
        Run comprehensive security scan on code
        
        Args:
            code: Python code to scan
        
        Returns:
            Dict: Security scan results
        """
        
        scan_result = {
            'safe': True,
            'risk_level': 'low',
            'issues': [],
            'recommendations': []
        }
        
        # Basic safety validation
        is_safe, issues = self.validate_code_safety(code)
        scan_result['issues'].extend(issues)
        
        if not is_safe:
            scan_result['safe'] = False
        
        # Determine risk level
        high_risk_patterns = ['subprocess', 'os.system', 'eval', 'exec', 'socket']
        medium_risk_patterns = ['open(', 'file(', 'import os', 'import sys']
        
        high_risk_count = sum(1 for pattern in high_risk_patterns if pattern in code)
        medium_risk_count = sum(1 for pattern in medium_risk_patterns if pattern in code)
        
        if high_risk_count > 0:
            scan_result['risk_level'] = 'high'
            scan_result['safe'] = False
        elif medium_risk_count > 2:
            scan_result['risk_level'] = 'medium'
        
        # Generate recommendations
        if high_risk_count > 0:
            scan_result['recommendations'].append("Remove or replace dangerous function calls")
        
        if 'while True:' in code:
            scan_result['recommendations'].append("Add break conditions to prevent infinite loops")
        
        if medium_risk_count > 0:
            scan_result['recommendations'].append("Review file operations and ensure they're necessary")
        
        return scan_result
    
    def execute_with_full_monitoring(self, code: str, test_params: Dict = None) -> Dict[str, Any]:
        """
        Execute code with full monitoring and security scanning
        
        Args:
            code: Python code to execute
            test_params: Parameters for the code
        
        Returns:
            Dict: Complete execution and security report
        """
        
        report = {
            'security_scan': self.run_security_scan(code),
            'execution_result': None,
            'overall_safe': False,
            'recommendations': []
        }
        
        # Check security first
        if not report['security_scan']['safe']:
            report['recommendations'].append("Code failed security scan - execution blocked")
            return report
        
        # Execute if security check passes
        report['execution_result'] = self.execute_code_in_sandbox(code, test_params)
        
        # Determine overall safety
        if (report['security_scan']['safe'] and 
            report['execution_result']['success'] and 
            not report['execution_result']['timeout'] and 
            not report['execution_result']['resource_exceeded']):
            report['overall_safe'] = True
        
        # Generate final recommendations
        if report['execution_result']['timeout']:
            report['recommendations'].append("Code execution timed out - optimize for better performance")
        
        if report['execution_result']['resource_exceeded']:
            report['recommendations'].append("Code exceeded resource limits - reduce memory/CPU usage")
        
        if not report['execution_result']['success']:
            report['recommendations'].append("Code execution failed - check for runtime errors")
        
        return report
    
    def batch_execute(self, code_list: List[str], test_params_list: List[Dict] = None) -> List[Dict]:
        """
        Execute multiple code snippets in separate sandboxes
        
        Args:
            code_list: List of Python code strings
            test_params_list: List of parameters for each code snippet
        
        Returns:
            List of execution results
        """
        
        results = []
        
        if test_params_list is None:
            test_params_list = [None] * len(code_list)
        
        for i, code in enumerate(code_list):
            test_params = test_params_list[i] if i < len(test_params_list) else None
            
            print(f"🔒 Executing code snippet {i+1}/{len(code_list)} in sandbox...")
            
            result = self.execute_with_full_monitoring(code, test_params)
            result['snippet_index'] = i
            results.append(result)
            
            # Brief pause between executions
            time.sleep(0.1)
        
        return results
