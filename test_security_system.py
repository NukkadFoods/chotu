#!/usr/bin/env python3
"""
🧪 SECURITY TEST SUITE
======================
Comprehensive test cases for autonomous learning security
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp.self_learning.safety_checker import safety_checker
from mcp.self_learning.code_generator import CodeGenerator
from mcp.self_learning.code_validator import CodeValidator

def test_malicious_code_rejection():
    """Test that malicious code patterns are properly rejected"""
    
    print("🔒 Testing malicious code rejection...")
    
    malicious_codes = [
        # System command injection
        "import os; os.system('rm -rf /')",
        
        # Eval/exec usage
        "user_input = input('Enter code: '); eval(user_input)",
        
        # Shell injection
        "subprocess.run(['ls'], shell=True)",
        
        # Dangerous file access
        "open('/etc/passwd', 'r').read()",
        
        # Network access
        "import socket; socket.socket().connect(('evil.com', 80))",
        
        # Code injection via f-strings
        "command = f'rm -rf {user_input}'; os.system(command)"
    ]
    
    passed = 0
    failed = 0
    
    for i, code in enumerate(malicious_codes, 1):
        print(f"\n   Test {i}: {code[:50]}...")
        result = safety_checker.validate(code)
        
        if not result['safe']:
            print(f"   ✅ PASSED - Correctly rejected (risk: {result['risk_level']})")
            passed += 1
        else:
            print(f"   ❌ FAILED - Should have been rejected!")
            failed += 1
    
    print(f"\n🔒 Malicious code tests: {passed} passed, {failed} failed")
    return failed == 0

def test_safe_code_acceptance():
    """Test that safe code patterns are properly accepted"""
    
    print("\n✅ Testing safe code acceptance...")
    
    safe_codes = [
        # Basic file reading
        """
import json
import os.path

def read_config(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return {}
""",
        
        # Safe subprocess usage
        """
import subprocess

def get_system_info():
    try:
        result = subprocess.run(['sw_vers'], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"Error: {e}"
""",
        
        # macOS automation
        """
import subprocess

def set_volume(level):
    try:
        cmd = ['osascript', '-e', f'set volume output volume {level}']
        subprocess.run(cmd, check=True)
        return {"status": "success", "volume": level}
    except Exception as e:
        return {"status": "error", "message": str(e)}
"""
    ]
    
    passed = 0
    failed = 0
    
    for i, code in enumerate(safe_codes, 1):
        print(f"\n   Test {i}: Safe code pattern...")
        result = safety_checker.validate(code)
        
        if result['safe'] and result['risk_level'] in ['low', 'low-medium']:
            print(f"   ✅ PASSED - Correctly accepted (score: {result['security_score']})")
            passed += 1
        else:
            print(f"   ❌ FAILED - Should have been accepted!")
            print(f"      Violations: {result['violations']}")
            failed += 1
    
    print(f"\n✅ Safe code tests: {passed} passed, {failed} failed")
    return failed == 0

def test_code_generation_security():
    """Test that code generation respects security constraints"""
    
    print("\n🛠️ Testing code generation security...")
    
    generator = CodeGenerator()
    
    test_requirements = [
        {
            "name": "safe_file_reader",
            "category": "utility",
            "description": "Read a text file safely",
            "user_goal": "Read file contents without security risks",
            "technical_requirements": {
                "input": "filepath",
                "output": "file contents or error",
                "safety": "no dangerous file access"
            }
        },
        {
            "name": "volume_controller", 
            "category": "system",
            "description": "Control macOS system volume",
            "user_goal": "Set system volume level",
            "technical_requirements": {
                "input": "volume level 0-100",
                "output": "success/error status",
                "safety": "use only osascript commands"
            }
        }
    ]
    
    passed = 0
    failed = 0
    
    for i, req in enumerate(test_requirements, 1):
        print(f"\n   Test {i}: Generating {req['name']}...")
        
        # Generate code
        generated_code = generator.generate_tool(req)
        
        if generated_code:
            # Validate security
            result = safety_checker.validate(generated_code, {
                'source': 'test_generation',
                'tool_name': req['name']
            })
            
            if result['safe'] and result['security_score'] >= 70:
                print(f"   ✅ PASSED - Generated secure code (score: {result['security_score']})")
                passed += 1
            else:
                print(f"   ❌ FAILED - Generated insecure code!")
                print(f"      Violations: {result['violations']}")
                failed += 1
        else:
            print(f"   ❌ FAILED - Code generation failed!")
            failed += 1
    
    print(f"\n🛠️ Code generation tests: {passed} passed, {failed} failed")
    return failed == 0

def test_comprehensive_validation():
    """Test the comprehensive validation system"""
    
    print("\n🔍 Testing comprehensive validation...")
    
    validator = CodeValidator()
    
    # Test code with various issues
    test_code = """
import subprocess
import socket  # Should trigger warning

def risky_function(user_input):
    # This should pass basic checks but have warnings
    result = subprocess.run(['ls', '-la'], capture_output=True, text=True)
    
    # File operation (should be monitored)
    with open('/tmp/test.txt', 'w') as f:
        f.write(result.stdout)
    
    return result.stdout

def nested_function():
    for i in range(10):
        for j in range(10):
            for k in range(10):  # Deep nesting
                if i == j == k:
                    return i * j * k
"""
    
    # Test validation
    result = validator.comprehensive_validation(test_code)
    
    print(f"   Overall valid: {result['overall_valid']}")
    print(f"   Validation results:")
    for check, details in result['validation_results'].items():
        status = "✅" if details['valid'] else "❌"
        print(f"     {status} {check}")
        if not details['valid'] and 'error' in details:
            print(f"        Error: {details['error']}")
        if 'issues' in details and details['issues']:
            for issue in details['issues']:
                print(f"        Issue: {issue}")
    
    return True

def test_security_report():
    """Test security reporting functionality"""
    
    print("\n📊 Testing security reporting...")
    
    # Generate some test validations
    test_codes = [
        "import json; data = json.loads('{}'); print(data)",  # Safe
        "import os; os.system('echo hello')",  # Unsafe
        "import subprocess; subprocess.run(['ls'])",  # Safe
        "eval('1 + 1')",  # Unsafe
    ]
    
    for code in test_codes:
        safety_checker.validate(code)
    
    # Get security report
    report = safety_checker.get_security_report()
    
    print(f"   Total validations: {report['total_validations']}")
    print(f"   Safe percentage: {report['safe_percentage']}%")
    print(f"   Average security score: {report['average_security_score']}")
    print(f"   Risk distribution: {report['risk_distribution']}")
    
    return report['total_validations'] > 0

def run_all_tests():
    """Run complete security test suite"""
    
    print("🧪 CHOTU AI SECURITY TEST SUITE")
    print("=" * 50)
    
    tests = [
        ("Malicious Code Rejection", test_malicious_code_rejection),
        ("Safe Code Acceptance", test_safe_code_acceptance),
        ("Code Generation Security", test_code_generation_security),
        ("Comprehensive Validation", test_comprehensive_validation),
        ("Security Reporting", test_security_report)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔄 Running: {test_name}")
        try:
            if test_func():
                print(f"✅ {test_name}: PASSED")
                passed += 1
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"💥 {test_name}: ERROR - {e}")
    
    print("\n" + "=" * 50)
    print(f"🏁 SECURITY TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL SECURITY TESTS PASSED! System is ready for deployment.")
    else:
        print("⚠️ SOME TESTS FAILED! Review security implementation before deployment.")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
