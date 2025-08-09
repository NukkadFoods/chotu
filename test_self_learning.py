#!/usr/bin/env python3
"""
Test autonomous learning system's ability to create tools for itself
"""

import sys
import os
import json
import requests
from datetime import datetime

# Add the correct path
sys.path.insert(0, '/Users/mahendrabahubali/chotu')

def test_self_learning_capability():
    print("🤖 Testing Self-Learning Capability")
    print("=" * 50)
    
    # Test cases for self-improvement tools
    self_improvement_requests = [
        "Create a tool to monitor my own learning performance and success rates",
        "Generate a function to analyze my own code generation quality",
        "Make a tool that can update my own capabilities based on user feedback",
        "Create a self-diagnostic tool to check my own system health",
        "Build a tool to backup and version my own learning progress"
    ]
    
    # MCP server should be running on port 3001
    server_url = "http://localhost:3001"
    
    print(f"🔗 Testing against MCP server at {server_url}")
    
    for i, request in enumerate(self_improvement_requests, 1):
        print(f"\n🧪 Test {i}: {request}")
        print("-" * 60)
        
        try:
            # Send learning request to autonomous learning endpoint
            response = requests.post(
                f"{server_url}/autonomous_learning/analyze_capability",
                json={
                    "user_intent": request,
                    "context": "self_improvement_test",
                    "priority": "high"
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"   📊 Analysis Result:")
                print(f"      Category: {result.get('intent_category', 'unknown')}")
                print(f"      Gap Detected: {result.get('capability_gap_detected', 'unknown')}")
                print(f"      Confidence: {result.get('confidence_score', 0)}%")
                
                if result.get('capability_gap_detected'):
                    print(f"   ✅ Would generate: {result.get('suggested_tool_name', 'unknown')}")
                    print(f"   🎯 Approach: {result.get('implementation_approach', 'unknown')}")
                else:
                    print(f"   ❌ No gap detected - existing capability found")
                    
            else:
                print(f"   ❌ Server error: {response.status_code}")
                print(f"   Error: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print(f"   ⚠️ Server not running - testing analyzer directly")
            test_analyzer_directly(request)
        except Exception as e:
            print(f"   ❌ Request failed: {e}")
    
    # Test actual tool generation
    print(f"\n🛠️ Testing Actual Tool Generation")
    print("=" * 50)
    
    test_direct_tool_generation()

def test_analyzer_directly(request):
    """Test the analyzer directly if server is not running"""
    try:
        sys.path.insert(0, '/Users/mahendrabahubali/chotu/mcp/self_learning')
        from code_analyzer import CodeAnalyzer
        
        analyzer = CodeAnalyzer()
        analysis = analyzer.analyze_intent(request, analyzer.known_tools)
        has_gap = analyzer.validate_capability_gap(request, analysis)
        
        print(f"   📊 Direct Analysis:")
        print(f"      Category: {analysis.get('intent_category', 'unknown')}")
        print(f"      Gap Detected: {has_gap}")
        print(f"      Confidence: {analysis.get('confidence_score', 0)}%")
        
    except Exception as e:
        print(f"   ❌ Direct analysis failed: {e}")

def test_direct_tool_generation():
    """Test generating a self-monitoring tool directly"""
    
    print(f"\n🔧 Generating Self-Learning Performance Monitor...")
    
    # Import the learning system
    try:
        sys.path.insert(0, '/Users/mahendrabahubali/chotu/mcp/self_learning')
        from self_learning_controller import SelfLearningController
        
        controller = SelfLearningController()
        
        # Request: Create a tool to monitor learning performance
        user_intent = "Create a tool to analyze and report on my autonomous learning system's performance metrics, success rates, and improvement suggestions"
        
        print(f"📝 Request: {user_intent}")
        
        # Trigger autonomous learning
        result = controller.process_learning_request(
            user_intent=user_intent,
            context="self_improvement_test",
            priority="high"
        )
        
        print(f"\n📊 Learning Result:")
        print(f"   Status: {result.get('status', 'unknown')}")
        print(f"   Generated Tool: {result.get('generated_tool_name', 'none')}")
        print(f"   File Location: {result.get('tool_file_path', 'none')}")
        print(f"   Validation: {result.get('validation_passed', False)}")
        
        if result.get('status') == 'success':
            print(f"   ✅ Self-learning tool successfully created!")
            
            # Test the generated tool
            tool_path = result.get('tool_file_path')
            if tool_path and os.path.exists(tool_path):
                print(f"\n🧪 Testing Generated Tool...")
                test_generated_tool(tool_path)
        else:
            print(f"   ❌ Tool generation failed: {result.get('error', 'unknown')}")
            
    except Exception as e:
        print(f"❌ Direct generation failed: {e}")
        print(f"Creating manual self-monitoring tool as fallback...")
        create_manual_self_monitor()

def test_generated_tool(tool_path):
    """Test the generated self-monitoring tool"""
    try:
        # Import and test the generated tool
        spec = importlib.util.spec_from_file_location("generated_tool", tool_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Look for main functions
        functions = [name for name, obj in inspect.getmembers(module) 
                    if inspect.isfunction(obj) and not name.startswith('_')]
        
        print(f"   🔍 Available functions: {functions}")
        
        # Try to run the main function if it exists
        if hasattr(module, 'analyze_learning_performance'):
            result = module.analyze_learning_performance()
            print(f"   📊 Tool output: {result}")
        elif hasattr(module, 'main'):
            result = module.main()
            print(f"   📊 Tool output: {result}")
        else:
            print(f"   ⚠️ No main function found to test")
            
    except Exception as e:
        print(f"   ❌ Tool test failed: {e}")

def create_manual_self_monitor():
    """Create a manual self-monitoring tool as fallback"""
    
    tool_content = '''#!/usr/bin/env python3
"""
AUTO-GENERATED TOOL: learning_performance_monitor
=================================================
Self-monitoring tool for autonomous learning system performance
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any

def analyze_learning_performance() -> dict:
    """
    Analyze the autonomous learning system's performance metrics
    
    Returns:
        dict: Performance analysis with metrics and suggestions
    """
    try:
        # Load learning logs
        logs_path = "/Users/mahendrabahubali/chotu/memory/learning_logs.json"
        
        if not os.path.exists(logs_path):
            return {"error": "Learning logs not found"}
        
        with open(logs_path, 'r') as f:
            logs = json.load(f)
        
        # Calculate performance metrics
        total_attempts = logs.get('total_attempts', 0)
        successful_attempts = logs.get('successful_attempts', 0)
        success_rate = logs.get('success_rate', 0.0)
        
        generated_tools = logs.get('generated_tools', [])
        learning_sessions = logs.get('learning_sessions', [])
        
        # Analyze tool generation patterns
        tool_categories = {}
        for tool in generated_tools:
            intent = tool.get('intent', 'unknown')
            category = categorize_intent(intent)
            tool_categories[category] = tool_categories.get(category, 0) + 1
        
        # Performance analysis
        performance = {
            "overall_performance": {
                "success_rate": success_rate,
                "total_attempts": total_attempts,
                "successful_attempts": successful_attempts,
                "efficiency_score": calculate_efficiency_score(logs)
            },
            "tool_generation_analysis": {
                "tools_generated": len(generated_tools),
                "categories_covered": list(tool_categories.keys()),
                "most_common_category": max(tool_categories.items(), key=lambda x: x[1])[0] if tool_categories else "none"
            },
            "learning_patterns": {
                "average_confidence": calculate_average_confidence(learning_sessions),
                "validation_success_rate": calculate_validation_success_rate(learning_sessions)
            },
            "improvement_suggestions": generate_improvement_suggestions(logs),
            "system_health": assess_system_health(logs),
            "timestamp": datetime.now().isoformat()
        }
        
        return performance
        
    except Exception as e:
        return {"error": f"Performance analysis failed: {str(e)}"}

def categorize_intent(intent: str) -> str:
    """Categorize user intent into broad categories"""
    intent_lower = intent.lower()
    
    if any(word in intent_lower for word in ['battery', 'power', 'charge']):
        return 'system_monitoring'
    elif any(word in intent_lower for word in ['network', 'connectivity', 'internet']):
        return 'network_tools'
    elif any(word in intent_lower for word in ['file', 'folder', 'directory']):
        return 'file_operations'
    elif any(word in intent_lower for word in ['music', 'audio', 'sound']):
        return 'media_control'
    elif any(word in intent_lower for word in ['email', 'message', 'communication']):
        return 'communication'
    else:
        return 'other'

def calculate_efficiency_score(logs: dict) -> float:
    """Calculate learning efficiency score"""
    success_rate = logs.get('success_rate', 0.0)
    total_attempts = logs.get('total_attempts', 1)
    
    # Efficiency based on success rate and number of attempts
    base_score = success_rate
    
    # Bonus for more attempts (shows active learning)
    attempt_bonus = min(total_attempts * 5, 20)  # Max 20 bonus points
    
    return min(100.0, base_score + attempt_bonus)

def calculate_average_confidence(sessions: List[dict]) -> float:
    """Calculate average confidence score across learning sessions"""
    if not sessions:
        return 0.0
    
    confidence_scores = []
    for session in sessions:
        for step in session.get('steps', []):
            if step.get('step') == 'analysis':
                result = step.get('result', {})
                confidence = result.get('confidence_score', 0)
                confidence_scores.append(confidence)
    
    return sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0

def calculate_validation_success_rate(sessions: List[dict]) -> float:
    """Calculate validation success rate"""
    if not sessions:
        return 0.0
    
    validation_successes = 0
    total_validations = 0
    
    for session in sessions:
        for step in session.get('steps', []):
            if step.get('step') == 'final_validation':
                total_validations += 1
                if step.get('status') == 'completed':
                    validation_successes += 1
    
    return (validation_successes / total_validations * 100) if total_validations > 0 else 0.0

def generate_improvement_suggestions(logs: dict) -> List[str]:
    """Generate suggestions for improving learning performance"""
    suggestions = []
    
    success_rate = logs.get('success_rate', 0.0)
    total_attempts = logs.get('total_attempts', 0)
    
    if success_rate < 80:
        suggestions.append("Consider improving capability gap analysis accuracy")
    
    if total_attempts < 5:
        suggestions.append("More learning attempts needed to establish patterns")
    
    validation_errors = logs.get('validation_errors', [])
    if validation_errors:
        suggestions.append("Review and address validation failures")
    
    generated_tools = logs.get('generated_tools', [])
    if len(generated_tools) < 3:
        suggestions.append("Expand tool generation to cover more capability areas")
    
    if not suggestions:
        suggestions.append("Performance is good - continue current learning approach")
    
    return suggestions

def assess_system_health(logs: dict) -> dict:
    """Assess overall system health"""
    success_rate = logs.get('success_rate', 0.0)
    validation_errors = logs.get('validation_errors', [])
    
    if success_rate >= 90 and not validation_errors:
        health_status = "excellent"
        health_color = "🟢"
    elif success_rate >= 70:
        health_status = "good"
        health_color = "🟡"
    elif success_rate >= 50:
        health_status = "fair"
        health_color = "🟠"
    else:
        health_status = "needs_attention"
        health_color = "🔴"
    
    return {
        "status": health_status,
        "indicator": health_color,
        "error_count": len(validation_errors),
        "last_updated": logs.get('system_metadata', {}).get('last_updated', 'unknown')
    }

def generate_performance_report() -> str:
    """Generate a formatted performance report"""
    performance = analyze_learning_performance()
    
    if "error" in performance:
        return f"❌ Error generating report: {performance['error']}"
    
    report = []
    report.append("🤖 AUTONOMOUS LEARNING PERFORMANCE REPORT")
    report.append("=" * 50)
    
    # Overall performance
    overall = performance['overall_performance']
    report.append(f"📊 Overall Performance:")
    report.append(f"   Success Rate: {overall['success_rate']:.1f}%")
    report.append(f"   Total Attempts: {overall['total_attempts']}")
    report.append(f"   Efficiency Score: {overall['efficiency_score']:.1f}/100")
    
    # Tool generation
    tools = performance['tool_generation_analysis']
    report.append(f"\\n🛠️ Tool Generation:")
    report.append(f"   Tools Created: {tools['tools_generated']}")
    report.append(f"   Categories: {', '.join(tools['categories_covered'])}")
    report.append(f"   Most Common: {tools['most_common_category']}")
    
    # Learning patterns
    learning = performance['learning_patterns']
    report.append(f"\\n🧠 Learning Patterns:")
    report.append(f"   Average Confidence: {learning['average_confidence']:.1f}%")
    report.append(f"   Validation Success: {learning['validation_success_rate']:.1f}%")
    
    # System health
    health = performance['system_health']
    report.append(f"\\n{health['indicator']} System Health: {health['status'].title()}")
    
    # Suggestions
    suggestions = performance['improvement_suggestions']
    report.append(f"\\n💡 Improvement Suggestions:")
    for suggestion in suggestions:
        report.append(f"   • {suggestion}")
    
    return "\\n".join(report)

# Tool metadata
TOOL_METADATA = {
    "name": "learning_performance_monitor",
    "category": "self_monitoring",
    "description": "Monitor and analyze autonomous learning system performance",
    "version": "1.0.0",
    "auto_generated": True,
    "created_at": "2025-08-09T07:30:00Z",
    "functions": ["analyze_learning_performance", "generate_performance_report"],
    "self_learning": True
}

if __name__ == "__main__":
    print("🤖 Testing Learning Performance Monitor")
    print("=" * 50)
    
    print("📊 Performance Analysis:")
    print(generate_performance_report())
'''
    
    # Save the tool
    tool_path = "/Users/mahendrabahubali/chotu/mcp/tools/learning_performance_monitor.py"
    
    with open(tool_path, 'w') as f:
        f.write(tool_content)
    
    print(f"✅ Manual self-monitoring tool created: {tool_path}")
    
    # Test the tool
    try:
        import subprocess
        result = subprocess.run(
            ['python3', tool_path], 
            capture_output=True, 
            text=True, 
            cwd='/Users/mahendrabahubali/chotu'
        )
        
        if result.returncode == 0:
            print(f"🧪 Tool test successful:")
            print(result.stdout)
        else:
            print(f"❌ Tool test failed: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Tool test error: {e}")

if __name__ == "__main__":
    test_self_learning_capability()
