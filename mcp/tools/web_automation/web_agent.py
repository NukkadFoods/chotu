#!/usr/bin/env python3
"""
🧠 CHOTU WEB TASK PLANNER
========================
Intelligent web task breakdown and planning using GPT
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

try:
    from utils.gpt_interface import call_gpt_system, call_gpt_learning
except ImportError:
    print("⚠️ GPT interface not available. Web planning will be limited.")
    call_gpt_system = None
    call_gpt_learning = None

class WebTaskPlanner:
    """Intelligent web task planner using GPT"""
    
    def __init__(self):
        self.learning_memory = self._load_web_learnings()
        self.known_sites = self._load_site_profiles()
        
        print("🧠 WebTaskPlanner initialized")
        print(f"   Known sites: {len(self.known_sites)}")
        print(f"   Learned workflows: {len(self.learning_memory.get('successful_flows', []))}")
    
    def _load_web_learnings(self) -> Dict:
        """Load previous web interaction learnings"""
        memory_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                  "memory", "web_learnings.json")
        
        try:
            if os.path.exists(memory_file):
                with open(memory_file, 'r') as f:
                    return json.load(f)
            else:
                return {
                    "successful_flows": [],
                    "failed_attempts": [],
                    "site_patterns": {},
                    "learned_selectors": {}
                }
        except Exception as e:
            print(f"⚠️ Failed to load web learnings: {e}")
            return {"successful_flows": [], "failed_attempts": []}
    
    def _load_site_profiles(self) -> Dict:
        """Load site-specific configuration profiles"""
        profiles = {}
        profiles_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                   "config", "web_profiles")
        
        if os.path.exists(profiles_dir):
            for file in os.listdir(profiles_dir):
                if file.endswith('.json'):
                    site_name = file[:-5]
                    try:
                        with open(os.path.join(profiles_dir, file), 'r') as f:
                            profiles[site_name] = json.load(f)
                    except Exception as e:
                        print(f"⚠️ Failed to load profile {site_name}: {e}")
        
        return profiles
    
    def plan_web_task(self, user_command: str, context: Dict = None) -> Dict[str, Any]:
        """
        Plan a web task by breaking it down into actionable steps
        
        Args:
            user_command: Natural language command from user
            context: Additional context about the task
            
        Returns:
            Dict: Structured plan with steps and metadata
        """
        
        print(f"🧠 Planning web task: {user_command}")
        
        if not call_gpt_system:
            return self._fallback_planning(user_command)
        
        # Check if we've done this before
        similar_flow = self._find_similar_flow(user_command)
        
        # Build context for GPT
        planning_context = {
            "user_command": user_command,
            "known_sites": list(self.known_sites.keys()),
            "similar_experience": similar_flow,
            "context": context or {}
        }
        
        prompt = f"""
You are Chotu's web task planner. Break down this web command into executable steps.

USER COMMAND: "{user_command}"

AVAILABLE SITE PROFILES: {list(self.known_sites.keys())}

SIMILAR PAST EXPERIENCE: {json.dumps(similar_flow, indent=2) if similar_flow else "None"}

Break this down into a detailed plan with these considerations:
1. Identify the target website/service
2. Plan navigation steps
3. Identify interaction points (search boxes, buttons, forms)
4. Consider safety checks for destructive actions
5. Plan data extraction if needed

Output as JSON:
{{
    "task_type": "search|extraction|form_filling|navigation|shopping",
    "target_site": "website domain or name",
    "confidence": 85,
    "safety_level": "safe|caution|dangerous",
    "steps": [
        {{
            "step_number": 1,
            "action": "navigate|search|click|fill|extract|wait",
            "target": "URL or element description",
            "value": "input value if needed",
            "selector_hint": "CSS selector or XPath hint",
            "safety_check": true/false,
            "description": "human readable step description"
        }}
    ],
    "expected_outcome": "what should happen when successful",
    "fallback_plan": "what to do if primary plan fails",
    "estimated_time": "seconds",
    "required_permissions": ["none|camera|microphone|location|notifications"]
}}

Focus on being practical and safe. Avoid any potentially harmful actions.
"""
        
        try:
            response = call_gpt_system(prompt)
            
            # Clean and parse response
            response = response.strip()
            if response.startswith('```json'):
                response = response[7:]
            if response.endswith('```'):
                response = response[:-3]
            
            plan = json.loads(response.strip())
            
            # Validate and enhance plan
            plan = self._validate_and_enhance_plan(plan, user_command)
            
            print(f"✅ Task plan created:")
            print(f"   Type: {plan.get('task_type', 'unknown')}")
            print(f"   Target: {plan.get('target_site', 'unknown')}")
            print(f"   Steps: {len(plan.get('steps', []))}")
            print(f"   Safety: {plan.get('safety_level', 'unknown')}")
            
            return plan
            
        except Exception as e:
            print(f"❌ GPT planning failed: {e}")
            return self._fallback_planning(user_command)
    
    def _find_similar_flow(self, command: str) -> Optional[Dict]:
        """Find similar past successful flows"""
        command_lower = command.lower()
        
        for flow in self.learning_memory.get('successful_flows', []):
            flow_command = flow.get('command', '').lower()
            
            # Simple similarity check
            if any(word in flow_command for word in command_lower.split() if len(word) > 3):
                return flow
        
        return None
    
    def _validate_and_enhance_plan(self, plan: Dict, original_command: str) -> Dict:
        """Validate and enhance the generated plan"""
        
        # Add metadata
        plan['created_at'] = datetime.now().isoformat()
        plan['original_command'] = original_command
        plan['plan_version'] = '2.1'
        
        # Validate safety level
        if plan.get('safety_level') not in ['safe', 'caution', 'dangerous']:
            plan['safety_level'] = 'caution'
        
        # Enhance steps with site-specific knowledge
        target_site = plan.get('target_site', '').lower()
        if target_site in self.known_sites:
            site_profile = self.known_sites[target_site]
            
            for step in plan.get('steps', []):
                if step.get('action') == 'search' and 'search_box' in site_profile:
                    step['selector_hint'] = site_profile['search_box']
                elif step.get('action') == 'extract' and step.get('target') == 'price':
                    if 'price_element' in site_profile:
                        step['selector_hint'] = site_profile['price_element']
        
        # Add safety checks
        for step in plan.get('steps', []):
            if step.get('action') in ['click', 'fill']:
                step['safety_check'] = True
                step['retry_attempts'] = 3
        
        return plan
    
    def _fallback_planning(self, command: str) -> Dict:
        """Fallback planning when GPT is not available"""
        
        print("⚠️ Using fallback planning (limited functionality)")
        
        # Basic pattern matching
        command_lower = command.lower()
        
        if 'search' in command_lower and 'google' in command_lower:
            query = command_lower.replace('search', '').replace('google', '').replace('for', '').strip()
            return {
                "task_type": "search",
                "target_site": "google.com",
                "confidence": 70,
                "safety_level": "safe",
                "steps": [
                    {
                        "step_number": 1,
                        "action": "navigate",
                        "target": "https://google.com",
                        "description": "Navigate to Google"
                    },
                    {
                        "step_number": 2,
                        "action": "search",
                        "target": "q",
                        "value": query,
                        "description": f"Search for: {query}"
                    }
                ],
                "expected_outcome": f"Google search results for: {query}",
                "fallback_plan": "Manual navigation if automation fails"
            }
        
        # Default fallback
        return {
            "task_type": "unknown",
            "target_site": "unknown",
            "confidence": 30,
            "safety_level": "caution",
            "steps": [
                {
                    "step_number": 1,
                    "action": "manual",
                    "description": "This task requires manual intervention"
                }
            ],
            "expected_outcome": "Manual completion required",
            "fallback_plan": "User assistance needed"
        }
    
    def execute_plan_step(self, step: Dict, web_commander) -> bool:
        """Execute a single step of the plan"""
        
        action = step.get('action')
        target = step.get('target')
        value = step.get('value')
        
        print(f"🔧 Executing step {step.get('step_number', '?')}: {step.get('description', action)}")
        
        try:
            if action == 'navigate':
                return web_commander.navigate_to(target)
            
            elif action == 'search':
                if target == 'q' and 'google.com' in web_commander.driver.current_url:
                    return web_commander.search_google(value)
                else:
                    return web_commander.fill_form_field(target, value)
            
            elif action == 'click':
                return web_commander.click_element(target, confirm=step.get('safety_check', True))
            
            elif action == 'fill':
                return web_commander.fill_form_field(target, value)
            
            elif action == 'extract':
                text = web_commander.extract_text(target)
                return text is not None
            
            elif action == 'wait':
                timeout = int(value) if value else 5
                return web_commander.wait_for_element(target, timeout)
            
            else:
                print(f"⚠️ Unknown action: {action}")
                return False
                
        except Exception as e:
            print(f"❌ Step execution failed: {e}")
            return False
    
    def save_successful_flow(self, command: str, plan: Dict, execution_result: bool):
        """Save successful workflow for future learning"""
        
        if execution_result and plan.get('safety_level') == 'safe':
            flow_record = {
                "timestamp": datetime.now().isoformat(),
                "command": command,
                "task_type": plan.get('task_type'),
                "target_site": plan.get('target_site'),
                "steps": [step.get('action') for step in plan.get('steps', [])],
                "success": True
            }
            
            self.learning_memory['successful_flows'].append(flow_record)
            self._save_web_learnings()
            
            print(f"💾 Saved successful workflow: {command}")
    
    def _save_web_learnings(self):
        """Save learning memory to file"""
        memory_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                  "memory", "web_learnings.json")
        
        try:
            os.makedirs(os.path.dirname(memory_file), exist_ok=True)
            with open(memory_file, 'w') as f:
                json.dump(self.learning_memory, f, indent=2)
        except Exception as e:
            print(f"⚠️ Failed to save web learnings: {e}")

# Example usage
if __name__ == "__main__":
    planner = WebTaskPlanner()
    
    test_commands = [
        "Search for Python tutorials on YouTube",
        "Find the latest Bitcoin price on CoinMarketCap",
        "Search Google for weather in San Francisco"
    ]
    
    for command in test_commands:
        plan = planner.plan_web_task(command)
        print(f"\nPlan for: {command}")
        print(json.dumps(plan, indent=2))
