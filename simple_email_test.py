#!/usr/bin/env python3
"""
Simple test: Let the system analyze email capability directly
"""

import sys
import os

# Add the correct path
sys.path.insert(0, '/Users/mahendrabahubali/chotu')
sys.path.insert(0, '/Users/mahendrabahubali/chotu/mcp/self_learning')

def simple_email_test():
    print("📧 Simple Autonomous Email Test")
    print("=" * 40)
    
    try:
        from code_analyzer import CodeAnalyzer
        
        analyzer = CodeAnalyzer()
        
        # Simple request
        request = "send email to ajay261999tiwari@gmail.com"
        
        print(f"📝 Request: {request}")
        
        # Check if existing email tool works
        print(f"\n🧪 Testing existing email tool first...")
        test_existing_email()
        
        # Let system validate capability gap
        print(f"\n🔍 System capability gap analysis...")
        
        # Simple analysis object to test gap detection
        analysis = {
            "intent_category": "communication",
            "user_goal": "send email to gmail address",
            "missing_capability": "gmail smtp email sending functionality"
        }
        
        has_gap = analyzer.validate_capability_gap(request, analysis)
        
        if has_gap:
            print(f"✅ System detected email capability gap!")
            print(f"🎯 Would generate improved email tool")
        else:
            print(f"❌ System thinks existing email tool is sufficient")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

def test_existing_email():
    """Test the existing broken email tool"""
    try:
        sys.path.insert(0, '/Users/mahendrabahubali/chotu/mcp/tools')
        from send_email import send_email
        
        result = send_email(
            "ajay261999tiwari@gmail.com",
            "Test from Chotu AI",
            "Testing email functionality"
        )
        
        print(f"   📧 Result: {result}")
        
        if "Error" in result or "Connection refused" in result:
            print(f"   ❌ CONFIRMED: Email tool is broken!")
            return False
        else:
            print(f"   ✅ Email tool working")
            return True
            
    except Exception as e:
        print(f"   ❌ Email test failed: {e}")
        return False

if __name__ == "__main__":
    simple_email_test()
