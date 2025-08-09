#!/usr/bin/env python3
"""
🔧 TEST CHOTU'S FAILURE LEARNING
===============================
Test Chotu's ability to learn from tool failures and improve autonomously
"""

import os
import sys
import subprocess

# Add project directories to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mcp'))

try:
    from mcp.self_learning.self_learning_controller import SelfLearningController
except ImportError:
    # Alternative import path
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mcp', 'self_learning'))
    from self_learning_controller import SelfLearningController

def simulate_email_tool_failure():
    """Simulate the email tool failure that occurred"""
    
    print("🔧 TESTING CHOTU'S FAILURE LEARNING CAPABILITY")
    print("=" * 60)
    
    # Initialize the learning controller
    controller = SelfLearningController()
    
    # Simulate the actual failure that occurred
    tool_name = "gmail_email_sender"
    error_message = """
[Errno 61] Connection refused when trying to connect to smtp.gmail.com:587.
This appears to be a localhost SMTP server configuration issue.
The tool attempted to send via Gmail but failed to establish SMTP connection.
Authentication or network connectivity problems with Gmail SMTP.
"""
    
    user_intent = "send email summary to gmail account"
    
    print(f"\n📧 Simulating Email Tool Failure:")
    print(f"   Tool: {tool_name}")
    print(f"   Error: Connection refused to smtp.gmail.com:587")
    print(f"   Intent: {user_intent}")
    
    # Let Chotu learn from this failure
    print(f"\n🧠 Letting Chotu analyze and learn from this failure...")
    
    result = controller.learn_from_failure(tool_name, error_message, user_intent)
    
    print(f"\n📊 FAILURE LEARNING RESULTS:")
    print(f"   Success: {result.get('success', False)}")
    
    if result.get('success', False):
        print(f"   Improved Tool: {result.get('improved_tool', 'unknown')}")
        print(f"   Root Cause Identified: {result.get('analysis', {}).get('failure_analysis', {}).get('root_cause', 'unknown')}")
        print(f"   Solution Approach: {result.get('analysis', {}).get('improvement_strategy', {}).get('approach', 'unknown')}")
        
        # Show what Chotu learned
        lessons = result.get('analysis', {}).get('domain_knowledge', {}).get('concepts_to_learn', [])
        if lessons:
            print(f"\n🎓 What Chotu Learned:")
            for lesson in lessons[:3]:  # Show first 3 lessons
                print(f"     • {lesson}")
    else:
        print(f"   Reason: {result.get('reason', 'unknown')}")
        print(f"   Analysis: {result.get('analysis', {})}")
    
    return result

def test_autonomous_email_improvement():
    """Test if Chotu can autonomously improve email capabilities"""
    
    print(f"\n🚀 TESTING AUTONOMOUS EMAIL IMPROVEMENT")
    print("=" * 50)
    
    controller = SelfLearningController()
    
    # Request email capability improvement
    improvement_request = """
Create a robust email sending tool that:
1. Can send emails via Gmail SMTP with proper authentication
2. Handles connection failures gracefully
3. Supports both text and HTML email formats
4. Has proper error handling and retry logic
5. Works with app passwords for Gmail accounts
"""
    
    print(f"📝 Improvement Request:")
    print(f"   Create robust Gmail email tool with proper SMTP handling")
    
    # Let Chotu learn and implement
    result = controller.handle_new_request(improvement_request)
    
    print(f"\n📊 AUTONOMOUS IMPROVEMENT RESULTS:")
    print(f"   Status: {result.get('status', 'unknown')}")
    print(f"   Message: {result.get('message', 'no message')}")
    
    if result.get('status') == 'success':
        details = result.get('details', {})
        print(f"   Approach: {details.get('approach', 'unknown')}")
        
        if details.get('approach') == 'new_tool':
            print(f"   Tool Created: {details.get('tool_created', 'unknown')}")
        elif details.get('approach') == 'enhancement':
            print(f"   Module Enhanced: {details.get('module_enhanced', 'unknown')}")
            print(f"   Function Added: {details.get('function_added', 'unknown')}")
    
    return result

def check_learning_statistics():
    """Check Chotu's learning statistics"""
    
    print(f"\n📈 CHOTU'S LEARNING STATISTICS")
    print("=" * 40)
    
    controller = SelfLearningController()
    stats = controller.get_learning_statistics()
    
    print(f"   Total Learning Attempts: {stats.get('total_attempts', 0)}")
    print(f"   Successful Attempts: {stats.get('successful_attempts', 0)}")
    print(f"   Success Rate: {stats.get('success_rate', 0):.1f}%")
    print(f"   Tools Generated: {stats.get('tools_generated', 0)}")
    print(f"   Validation Errors: {stats.get('validation_errors', 0)}")
    print(f"   Learning Sessions: {stats.get('learning_sessions', 0)}")
    print(f"   Safety Mode: {'ON' if stats.get('safety_mode', True) else 'OFF'}")
    
    return stats

def main():
    """Main test function"""
    
    print("🧠 CHOTU FAILURE LEARNING TEST")
    print("=" * 50)
    print("Testing Chotu's ability to learn from failures autonomously")
    print("This demonstrates genuine autonomous learning capabilities")
    
    try:
        # Test 1: Learn from email tool failure
        failure_result = simulate_email_tool_failure()
        
        # Test 2: Autonomous email improvement
        improvement_result = test_autonomous_email_improvement()
        
        # Test 3: Check learning statistics
        stats = check_learning_statistics()
        
        print(f"\n🏆 FINAL ASSESSMENT:")
        print("=" * 30)
        
        if failure_result.get('success', False):
            print("✅ Chotu successfully learned from email tool failure")
        else:
            print("❌ Chotu could not learn from email tool failure")
        
        if improvement_result.get('status') == 'success':
            print("✅ Chotu autonomously improved email capabilities")
        else:
            print("❌ Chotu could not autonomously improve email capabilities")
        
        overall_success = stats.get('success_rate', 0) > 50
        if overall_success:
            print("✅ Overall learning performance is good")
        else:
            print("⚠️  Overall learning performance needs improvement")
        
        print(f"\n🎯 CONCLUSION:")
        if failure_result.get('success', False) and improvement_result.get('status') == 'success':
            print("🌟 Chotu demonstrates excellent autonomous failure learning!")
            print("   The system can detect failures, analyze them, and create improved solutions")
        else:
            print("🔧 Chotu's failure learning needs refinement")
            print("   The system shows partial autonomous learning capabilities")
    
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
