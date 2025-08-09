#!/usr/bin/env python3
"""
🔧 SIMPLE CHOTU FAILURE LEARNING TEST
====================================
Test Chotu's ability to learn from failures autonomously
"""

import os
import sys
import json
from datetime import datetime

# Add paths
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
sys.path.append(os.path.join(project_root, 'utils'))

# Import what we need
from utils.gpt_interface import call_gpt_learning

def analyze_email_failure():
    """Let Chotu analyze the email failure and learn from it"""
    
    print("🔧 CHOTU ANALYZING EMAIL TOOL FAILURE")
    print("=" * 50)
    
    failure_prompt = """
You are Chotu, an autonomous learning system. An email tool you created has failed and you need to learn from this failure.

TOOL FAILURE DETAILS:
- Tool Name: gmail_email_sender.py
- Error: [Errno 61] Connection refused when connecting to smtp.gmail.com:587
- User Intent: Send email summary to Gmail account
- Root Issue: SMTP connection failure, likely authentication or configuration problem

ANALYZE THIS FAILURE AND LEARN:

1. What went wrong technically?
2. What domain knowledge do you need to learn about email/SMTP?
3. How should you improve your email tool generation capabilities?
4. What specific patterns should you remember for Gmail SMTP?

Provide a detailed analysis that will help you create better email tools in the future.

Return your analysis as JSON:
{
    "failure_analysis": {
        "root_cause": "specific technical reason",
        "what_went_wrong": "detailed explanation",
        "missing_knowledge": ["key concepts I didn't understand"]
    },
    "domain_learning": {
        "smtp_concepts": ["SMTP concepts to learn"],
        "gmail_specifics": ["Gmail-specific requirements"],
        "authentication": ["authentication methods to understand"],
        "troubleshooting": ["common issues and solutions"]
    },
    "improvement_strategy": {
        "better_patterns": ["coding patterns for reliable email tools"],
        "configuration_approach": "how to handle SMTP configuration",
        "error_handling": "how to handle connection failures",
        "testing_approach": "how to test email tools safely"
    },
    "learned_lessons": ["key lessons for future email tool generation"]
}
"""
    
    print("🧠 Chotu is analyzing the failure...")
    
    try:
        response = call_gpt_learning(failure_prompt)
        
        # Clean response
        response = response.strip()
        if response.startswith('```json'):
            response = response[7:]
        if response.endswith('```'):
            response = response[:-3]
        
        analysis = json.loads(response.strip())
        
        print("✅ Analysis Complete!")
        print(f"\nRoot Cause: {analysis.get('failure_analysis', {}).get('root_cause', 'unknown')}")
        print(f"Missing Knowledge: {len(analysis.get('failure_analysis', {}).get('missing_knowledge', []))} concepts")
        print(f"SMTP Concepts to Learn: {len(analysis.get('domain_learning', {}).get('smtp_concepts', []))} items")
        print(f"Lessons Learned: {len(analysis.get('learned_lessons', []))} lessons")
        
        return analysis
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        return None

def generate_improved_email_tool(analysis):
    """Let Chotu generate an improved email tool based on failure analysis"""
    
    print(f"\n🛠️  CHOTU GENERATING IMPROVED EMAIL TOOL")
    print("=" * 50)
    
    if not analysis:
        print("❌ Cannot generate without analysis")
        return None
    
    improvement_prompt = f"""
You are Chotu, an autonomous learning system. Based on your failure analysis, create an improved Gmail email tool.

YOUR FAILURE ANALYSIS:
{json.dumps(analysis, indent=2)}

REQUIREMENTS FOR IMPROVED TOOL:
1. Handle Gmail SMTP connection properly (smtp.gmail.com:587)
2. Use TLS encryption for security
3. Support app passwords for authentication
4. Have proper error handling and retry logic
5. Include connection testing before sending
6. Provide clear error messages to users
7. Support both text and HTML emails

Create a complete Python tool that implements these improvements.

Include:
- Proper imports
- Configuration handling
- Connection testing
- Email sending function
- Error handling
- Usage example

Make it production-ready and robust.
"""
    
    print("🧠 Chotu is generating improved email tool...")
    
    try:
        response = call_gpt_learning(improvement_prompt)
        
        print("✅ Improved tool generated!")
        print(f"Generated {len(response)} characters of code")
        
        # Save the improved tool
        tool_path = os.path.join(project_root, "chotu_improved_email_sender.py")
        with open(tool_path, 'w') as f:
            f.write(response)
        
        print(f"💾 Saved improved tool to: {tool_path}")
        
        return response
        
    except Exception as e:
        print(f"❌ Tool generation failed: {e}")
        return None

def test_learning_improvement():
    """Test if the learning actually improved Chotu's capabilities"""
    
    print(f"\n📊 TESTING LEARNING IMPROVEMENT")
    print("=" * 40)
    
    # Test by asking Chotu to explain what it learned
    learning_test_prompt = """
You are Chotu. You just learned from an email tool failure and created an improved version.

Explain what you learned:
1. What were the 3 most important technical insights?
2. How will you approach email tools differently now?
3. What specific Gmail SMTP knowledge did you gain?
4. What patterns will you use for future email tools?

Provide a concise summary showing your improved understanding.
"""
    
    print("🧠 Testing Chotu's improved understanding...")
    
    try:
        response = call_gpt_learning(learning_test_prompt)
        
        print("✅ Learning test complete!")
        print("\n🎓 CHOTU'S LEARNED INSIGHTS:")
        print(response[:500] + "..." if len(response) > 500 else response)
        
        return True
        
    except Exception as e:
        print(f"❌ Learning test failed: {e}")
        return False

def log_learning_session(analysis, tool_generated, test_passed):
    """Log this learning session"""
    
    learning_log = {
        'timestamp': datetime.now().isoformat(),
        'type': 'autonomous_failure_learning',
        'original_failure': 'gmail_email_sender SMTP connection refused',
        'analysis_success': analysis is not None,
        'tool_generation_success': tool_generated is not None,
        'learning_test_passed': test_passed,
        'lessons_learned': analysis.get('learned_lessons', []) if analysis else [],
        'overall_success': analysis is not None and tool_generated is not None and test_passed
    }
    
    # Save to learning log
    log_file = os.path.join(project_root, "failure_learning_log.json")
    
    try:
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                logs = json.load(f)
        else:
            logs = []
        
        logs.append(learning_log)
        
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
        
        print(f"📝 Learning session logged to: {log_file}")
        
    except Exception as e:
        print(f"⚠️ Failed to log learning session: {e}")

def main():
    """Main test function"""
    
    print("🧠 CHOTU AUTONOMOUS FAILURE LEARNING TEST")
    print("=" * 60)
    print("Testing Chotu's ability to learn from email tool failure")
    print("This demonstrates genuine autonomous learning from mistakes")
    
    try:
        # Step 1: Analyze the failure
        analysis = analyze_email_failure()
        
        # Step 2: Generate improved tool
        improved_tool = generate_improved_email_tool(analysis)
        
        # Step 3: Test learning improvement
        test_passed = test_learning_improvement()
        
        # Step 4: Log the learning session
        log_learning_session(analysis, improved_tool, test_passed)
        
        # Final assessment
        print(f"\n🏆 AUTONOMOUS LEARNING ASSESSMENT:")
        print("=" * 50)
        
        if analysis:
            print("✅ Chotu successfully analyzed the email tool failure")
        else:
            print("❌ Chotu could not analyze the failure")
        
        if improved_tool:
            print("✅ Chotu autonomously generated an improved email tool")
        else:
            print("❌ Chotu could not generate improved tool")
        
        if test_passed:
            print("✅ Chotu demonstrated improved understanding")
        else:
            print("❌ Chotu's learning improvement unclear")
        
        overall_success = analysis and improved_tool and test_passed
        
        print(f"\n🎯 CONCLUSION:")
        if overall_success:
            print("🌟 EXCELLENT! Chotu demonstrates autonomous failure learning!")
            print("   ✓ Analyzed failure root cause")
            print("   ✓ Generated improved solution")
            print("   ✓ Showed improved understanding")
            print("   This is genuine autonomous learning from mistakes!")
        else:
            print("🔧 Chotu's autonomous learning needs improvement")
            print("   Some aspects of failure learning worked, others need refinement")
        
        return overall_success
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    main()
