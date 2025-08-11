#!/usr/bin/env python3
"""
🛡️ SAFETY CHECKER
=================
Multi-layer security validation system for autonomous code generation
"""

import ast
import re
import subprocess
import os
import json
import hashlib
from typing import Dict, List, Tuple, Any, Optional
from datetime import datetime

class SafetyChecker:
    """Multi-layer code validation system with security focus"""
    
    def __init__(self):
        self.rules = {
            'max_code_length': 2000,
            'max_functions': 10,
            'max_imports': 15,
            'allowed_subprocess_commands': [
                'osascript', 'open', 'pmset', 'networksetup', 
                'screencapture', 'blueutil', 'ls', 'cat', 'grep',
                'sw_vers', 'uname', 'whoami', 'pwd', 'date',
                'find', 'awk', 'sed', 'sort', 'uniq', 'head', 'tail'
            ],
            'banned_patterns': [
                r'os\.system\s*\(',
                r'eval\s*\(',
                r'exec\s*\(',
                r'__import__\s*\(',
                r'shell\s*=\s*True',
                r'rm\s+-rf',
                r'sudo\s+',
                r'curl.*\|\s*bash',
                r'wget.*\|\s*sh'
            ],
            'dangerous_paths': [
                '/etc/passwd', '/etc/shadow', '/etc/sudoers',
                '/System/Library/', '/usr/bin/sudo', '/bin/rm',
                '/Library/LaunchDaemons/', '/Library/StartupItems/'
            ]
        }
        
        self.allowed_imports = {
            'subprocess', 'os.path', 'os', 'json', 'datetime', 'time',
            'pathlib', 're', 'shutil', 'tempfile', 'typing',
            'collections', 'itertools', 'functools', 'math',
            'sys', 'platform', 'glob', 'uuid', 'hashlib'
        }
        
        self.security_log = []
    
    def validate(self, code: str, metadata: Dict = None) -> Dict[str, Any]:
        """
        Comprehensive multi-layer validation
        
        Args:
            code: Python code to validate
            metadata: Additional context about the code
        
        Returns:
            Dict: Validation results with safety assessment
        """
        
        validation_result = {
            'safe': True,
            'risk_level': 'low',
            'violations': [],
            'warnings': [],
            'recommendations': [],
            'security_score': 100,
            'passed_checks': [],
            'failed_checks': []
        }
        
        # Layer 1: Syntax and structure validation
        syntax_result = self._check_syntax(code)
        if not syntax_result['valid']:
            validation_result['safe'] = False
            validation_result['failed_checks'].append('syntax')
            validation_result['violations'].append(f"Syntax error: {syntax_result['error']}")
        else:
            validation_result['passed_checks'].append('syntax')
        
        # Layer 2: Security pattern analysis
        security_result = self._check_security_patterns(code)
        validation_result['violations'].extend(security_result['violations'])
        validation_result['warnings'].extend(security_result['warnings'])
        validation_result['security_score'] -= security_result['penalty']
        
        if security_result['violations']:
            validation_result['safe'] = False
            validation_result['failed_checks'].append('security_patterns')
        else:
            validation_result['passed_checks'].append('security_patterns')
        
        # Layer 3: Import validation
        import_result = self._check_imports(code)
        if not import_result['valid']:
            validation_result['safe'] = False
            validation_result['failed_checks'].append('imports')
            validation_result['violations'].extend(import_result['violations'])
        else:
            validation_result['passed_checks'].append('imports')
        
        # Layer 4: Code complexity analysis
        complexity_result = self._check_complexity(code)
        if complexity_result['violations']:
            validation_result['warnings'].extend(complexity_result['violations'])
            validation_result['security_score'] -= 10
            validation_result['failed_checks'].append('complexity')
        else:
            validation_result['passed_checks'].append('complexity')
        
        # Layer 5: System call validation
        syscall_result = self._check_system_calls(code)
        if syscall_result['violations']:
            validation_result['safe'] = False
            validation_result['failed_checks'].append('system_calls')
            validation_result['violations'].extend(syscall_result['violations'])
        else:
            validation_result['passed_checks'].append('system_calls')
        
        # Layer 6: File operation validation
        fileop_result = self._check_file_operations(code)
        if fileop_result['violations']:
            validation_result['safe'] = False
            validation_result['failed_checks'].append('file_operations')
            validation_result['violations'].extend(fileop_result['violations'])
        else:
            validation_result['passed_checks'].append('file_operations')
        
        # Determine final risk level
        validation_result['risk_level'] = self._calculate_risk_level(validation_result)
        
        # Log this validation
        self._log_validation(code, validation_result, metadata)
        
        return validation_result
    
    def _check_syntax(self, code: str) -> Dict[str, Any]:
        """Basic syntax validation"""
        try:
            ast.parse(code)
            return {'valid': True, 'error': None}
        except SyntaxError as e:
            return {'valid': False, 'error': f"Line {e.lineno}: {e.msg}"}
        except Exception as e:
            return {'valid': False, 'error': str(e)}
    
    def _check_security_patterns(self, code: str) -> Dict[str, Any]:
        """Check for dangerous security patterns"""
        result = {
            'violations': [],
            'warnings': [],
            'penalty': 0
        }
        
        for pattern in self.rules['banned_patterns']:
            matches = re.findall(pattern, code, re.IGNORECASE)
            if matches:
                result['violations'].append(f"Dangerous pattern detected: {pattern}")
                result['penalty'] += 50  # Major penalty
        
        # Check for potential code injection
        if re.search(r'f["\'].*\{.*\}.*["\']', code):
            result['warnings'].append("F-string with variable interpolation detected")
            result['penalty'] += 5
        
        # Check for network operations
        network_patterns = [
            r'requests\.',
            r'urllib\.',
            r'socket\.',
            r'http\.',
            r'ftp\.'
        ]
        
        for pattern in network_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                result['warnings'].append(f"Network operation detected: {pattern}")
                result['penalty'] += 10
        
        return result
    
    def _check_imports(self, code: str) -> Dict[str, Any]:
        """Validate imports against whitelist"""
        result = {
            'valid': True,
            'violations': []
        }
        
        try:
            tree = ast.parse(code)
            imported_modules = set()
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imported_modules.add(alias.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imported_modules.add(node.module.split('.')[0])
            
            # Check against allowed imports
            unauthorized_imports = imported_modules - self.allowed_imports
            if unauthorized_imports:
                result['valid'] = False
                result['violations'] = [f"Unauthorized import: {imp}" for imp in unauthorized_imports]
        
        except Exception as e:
            result['valid'] = False
            result['violations'] = [f"Import analysis failed: {e}"]
        
        return result
    
    def _check_complexity(self, code: str) -> Dict[str, Any]:
        """Check code complexity limits"""
        result = {'violations': []}
        
        # Check code length
        if len(code) > self.rules['max_code_length']:
            result['violations'].append(f"Code too long: {len(code)} > {self.rules['max_code_length']}")
        
        try:
            tree = ast.parse(code)
            
            # Count functions
            functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            if len(functions) > self.rules['max_functions']:
                result['violations'].append(f"Too many functions: {len(functions)} > {self.rules['max_functions']}")
            
            # Check for deeply nested code
            max_depth = self._calculate_nesting_depth(tree)
            if max_depth > 5:
                result['violations'].append(f"Code too deeply nested: depth {max_depth}")
        
        except Exception as e:
            result['violations'].append(f"Complexity analysis failed: {e}")
        
        return result
    
    def _check_system_calls(self, code: str) -> Dict[str, Any]:
        """Validate system calls and subprocess usage"""
        result = {'violations': []}
        
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    # Check subprocess calls
                    if (isinstance(node.func, ast.Attribute) and 
                        isinstance(node.func.value, ast.Name) and
                        node.func.value.id == 'subprocess'):
                        
                        # Analyze the command being executed
                        if node.args and isinstance(node.args[0], ast.List):
                            # subprocess.run(['command', 'arg1', 'arg2'])
                            cmd_elements = []
                            for elt in node.args[0].elts:
                                if isinstance(elt, ast.Constant):
                                    cmd_elements.append(elt.value)
                            
                            if cmd_elements:
                                command = cmd_elements[0]
                                if command not in self.rules['allowed_subprocess_commands']:
                                    result['violations'].append(f"Unauthorized command: {command}")
                        
                        # Check for shell=True
                        for keyword in node.keywords:
                            if (keyword.arg == 'shell' and 
                                isinstance(keyword.value, ast.Constant) and 
                                keyword.value.value is True):
                                result['violations'].append("subprocess with shell=True is forbidden")
        
        except Exception as e:
            result['violations'].append(f"System call analysis failed: {e}")
        
        return result
    
    def _check_file_operations(self, code: str) -> Dict[str, Any]:
        """Check file operations for dangerous paths"""
        result = {'violations': []}
        
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    if node.func.id in ['open', 'file']:
                        # Check file path
                        if node.args and isinstance(node.args[0], ast.Constant):
                            path = node.args[0].value
                            if isinstance(path, str):
                                for dangerous_path in self.rules['dangerous_paths']:
                                    if path.startswith(dangerous_path):
                                        result['violations'].append(f"Dangerous file access: {path}")
                                
                                # Allow /tmp, /Users, and relative paths but flag system files
                                if (path.startswith('/etc/passwd') or
                                    path.startswith('/etc/shadow') or
                                    path.startswith('/etc/sudoers')):
                                    result['violations'].append(f"Critical system file access: {path}")
                                elif not (path.startswith('/tmp/') or 
                                         path.startswith('/Users/') or 
                                         not path.startswith('/') or
                                         path.startswith('./') or
                                         path.startswith('../')):
                                    result['violations'].append(f"Potentially unsafe file path: {path}")
        
        except Exception as e:
            result['violations'].append(f"File operation analysis failed: {e}")
        
        return result
    
    def _calculate_nesting_depth(self, node, current_depth=0):
        """Calculate maximum nesting depth of AST"""
        max_depth = current_depth
        
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.For, ast.While, ast.If, ast.With, ast.Try, ast.FunctionDef, ast.ClassDef)):
                child_depth = self._calculate_nesting_depth(child, current_depth + 1)
                max_depth = max(max_depth, child_depth)
            else:
                child_depth = self._calculate_nesting_depth(child, current_depth)
                max_depth = max(max_depth, child_depth)
        
        return max_depth
    
    def _calculate_risk_level(self, validation_result: Dict) -> str:
        """Calculate overall risk level"""
        if validation_result['violations']:
            return 'high'
        elif validation_result['security_score'] < 70:
            return 'medium'
        elif validation_result['warnings']:
            return 'low-medium'
        else:
            return 'low'
    
    def _log_validation(self, code: str, result: Dict, metadata: Dict = None):
        """Log validation results for audit trail"""
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'code_hash': hashlib.sha256(code.encode()).hexdigest()[:16],
            'safe': result['safe'],
            'risk_level': result['risk_level'],
            'security_score': result['security_score'],
            'violations_count': len(result['violations']),
            'warnings_count': len(result['warnings']),
            'metadata': metadata or {}
        }
        
        self.security_log.append(log_entry)
        
        # Keep only last 1000 entries
        if len(self.security_log) > 1000:
            self.security_log = self.security_log[-1000:]
    
    def get_security_report(self) -> Dict[str, Any]:
        """Generate security audit report"""
        
        if not self.security_log:
            return {
                'total_validations': 0,
                'safe_percentage': 0,
                'average_security_score': 0,
                'recent_violations': []
            }
        
        total = len(self.security_log)
        safe_count = sum(1 for entry in self.security_log if entry['safe'])
        
        avg_score = sum(entry['security_score'] for entry in self.security_log) / total
        
        recent_violations = [
            entry for entry in self.security_log[-50:]  # Last 50
            if not entry['safe']
        ]
        
        return {
            'total_validations': total,
            'safe_percentage': round((safe_count / total) * 100, 2),
            'average_security_score': round(avg_score, 2),
            'recent_violations': recent_violations[-10:],  # Last 10 violations
            'risk_distribution': self._get_risk_distribution()
        }
    
    def _get_risk_distribution(self) -> Dict[str, int]:
        """Get distribution of risk levels"""
        distribution = {'low': 0, 'low-medium': 0, 'medium': 0, 'high': 0}
        
        for entry in self.security_log:
            risk = entry.get('risk_level', 'unknown')
            if risk in distribution:
                distribution[risk] += 1
        
        return distribution

# Global instance
safety_checker = SafetyChecker()
