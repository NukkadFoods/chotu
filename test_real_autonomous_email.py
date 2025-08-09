#!/usr/bin/env python3
"""
Real test: Let the autonomous learning system detect email capability gaps
and create its own solution
"""

import sys
import os

# Add the correct path
sys.path.insert(0, '/Users/mahendrabahubali/chotu')
sys.path.insert(0, '/Users/mahendrabahubali/chotu/mcp/self_learning')

def test_autonomous_email_learning():
    print("🤖 REAL TEST: Autonomous Email Learning")
    print("=" * 50)
    print("🎯 Objective: Ask system to email summary and let IT figure out the problems")
    
    # Import the autonomous learning system
    try:
        from code_analyzer import CodeAnalyzer
        
        analyzer = CodeAnalyzer()
        
        # The real test: Ask it to email the achievement summary
        user_request = "Email the self-improvement achievement summary to ajay261999tiwari@gmail.com with a professional subject line"
        
        print(f"\n📝 User Request: {user_request}")
        print("\n🔍 Let the system analyze this request...")
        
        # Step 1: Analyze the intent
        analysis = analyzer.analyze_intent(user_request, analyzer.known_tools)
        
        print(f"\n📊 System Analysis:")
        print(f"   Intent Category: {analysis.get('intent_category', 'unknown')}")
        print(f"   User Goal: {analysis.get('user_goal', 'unknown')}")
        print(f"   Missing Capability: {analysis.get('missing_capability', 'unknown')}")
        print(f"   Confidence Score: {analysis.get('confidence_score', 0)}%")
        
        # Step 2: Check if it detects the email capability gap
        has_gap = analyzer.validate_capability_gap(user_request, analysis)
        
        print(f"\n🎯 Capability Gap Analysis:")
        if has_gap:
            print(f"   ✅ GAP DETECTED - System will create new email tool")
            print(f"   🧠 Reasoning: System detected existing email tool limitations")
        else:
            print(f"   ❌ NO GAP - System thinks existing email tool is sufficient")
            print(f"   🤔 Let's test the existing tool to prove it's broken...")
            test_existing_email_tool()
            
        # Step 3: If gap detected, see what the system would do
        if has_gap:
            enhancement_plan = analyzer.generate_enhancement_plan(analysis)
            print(f"\n🛠️ System Enhancement Plan:")
            print(f"   Implementation Type: {enhancement_plan.get('implementation_type', 'unknown')}")
            print(f"   Priority Level: {enhancement_plan.get('priority_level', 'unknown')}")
            print(f"   Estimated Effort: {enhancement_plan.get('estimated_effort', 'unknown')}")
            print(f"   Dependencies: {enhancement_plan.get('dependencies', [])}")
            
            # Step 4: Let's trigger actual tool generation
            print(f"\n🚀 Triggering Autonomous Tool Generation...")
            trigger_autonomous_learning(user_request)
        
    except Exception as e:
        print(f"❌ Autonomous learning test failed: {e}")

def test_existing_email_tool():
    """Test the existing email tool to show it's broken"""
    print(f"\n🧪 Testing Existing Email Tool:")
    
    try:
        sys.path.insert(0, '/Users/mahendrabahubali/chotu/mcp/tools')
        from send_email import send_email
        
        # Test the broken email tool
        result = send_email(
            "ajay261999tiwari@gmail.com",
            "Test Email from Chotu AI",
            "This is a test email to verify email functionality."
        )
        
        print(f"   📧 Email Tool Result: {result}")
        
        if "Error" in result or "Connection refused" in result:
            print(f"   ❌ CONFIRMED: Existing email tool is BROKEN (localhost SMTP)")
            print(f"   🎯 This proves the autonomous system should detect this gap!")
        else:
            print(f"   ✅ Email tool working (unexpected)")
            
    except Exception as e:
        print(f"   ❌ Email tool test failed: {e}")
        print(f"   🎯 This confirms the email capability needs improvement")

def trigger_autonomous_learning(user_request):
    """Trigger the autonomous learning system to create email solution"""
    
    try:
        from self_learning_controller import SelfLearningController
        
        controller = SelfLearningController()
        
        print(f"🧠 Autonomous Learning Controller Processing Request...")
        
        # Let the system process the email request autonomously
        result = controller.process_learning_request(
            user_intent=user_request,
            context="email_capability_enhancement",
            priority="high"
        )
        
        print(f"\n🎯 Autonomous Learning Result:")
        print(f"   Status: {result.get('status', 'unknown')}")
        print(f"   Generated Tool: {result.get('generated_tool_name', 'none')}")
        print(f"   Approach: {result.get('approach', 'unknown')}")
        print(f"   Validation: {result.get('validation_passed', False)}")
        
        if result.get('status') == 'success':
            print(f"   ✅ System autonomously created email solution!")
            
            # Test the new tool
            tool_path = result.get('tool_file_path')
            if tool_path:
                print(f"\n🧪 Testing Generated Email Tool...")
                test_generated_email_tool(tool_path)
        else:
            print(f"   ❌ Autonomous generation failed: {result.get('error', 'unknown')}")
            
    except Exception as e:
        print(f"❌ Autonomous learning controller failed: {e}")
        print(f"🔧 Fallback: Let me check what the system would analyze...")
        
        # Fallback: Show what a real autonomous system would detect
        show_autonomous_analysis(user_request)

def test_generated_email_tool(tool_path):
    """Test the autonomously generated email tool"""
    try:
        import subprocess
        
        result = subprocess.run(
            ['python3', tool_path], 
            capture_output=True, 
            text=True, 
            cwd='/Users/mahendrabahubali/chotu'
        )
        
        if result.returncode == 0:
            print(f"   ✅ Generated email tool executed successfully")
            print(f"   📊 Output: {result.stdout[:200]}...")
        else:
            print(f"   ❌ Generated email tool failed: {result.stderr}")
            
    except Exception as e:
        print(f"   ❌ Generated email tool test error: {e}")

def show_autonomous_analysis(user_request):
    """Show what the autonomous system would detect about email capabilities"""
    
    print(f"\n🔍 Autonomous System Analysis Would Detect:")
    print(f"   🎯 User wants to: Email achievement summary to Gmail")
    print(f"   🔧 Existing tool: send_email.py (uses localhost SMTP)")
    print(f"   ❌ Problem: Localhost SMTP cannot reach Gmail servers")
    print(f"   📧 Gmail needs: SMTP authentication, TLS, app passwords")
    print(f"   🛠️ Solution: Create Gmail-compatible email tool")
    print(f"   🚀 Autonomous action: Generate enhanced_gmail_sender.py")
    
    print(f"\n💡 What Real Autonomous Learning Would Do:")
    print(f"   1. 🔍 Analyze existing send_email.py code")
    print(f"   2. ❌ Detect localhost limitation")
    print(f"   3. 🧠 Research Gmail SMTP requirements")
    print(f"   4. 🛠️ Generate Gmail-compatible tool")
    print(f"   5. 🧪 Test with simulation/preview mode")
    print(f"   6. ✅ Report success to user")

if __name__ == "__main__":
    test_autonomous_email_learning()
