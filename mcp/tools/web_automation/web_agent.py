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
    
    def _validate_json_response(self, response: str) -> str:
        """Pre-validate and clean JSON response before parsing"""
        
        # Remove common GPT response artifacts
        response = response.strip()
        
        # Remove markdown code blocks
        if response.startswith('```json'):
            response = response[7:]
        elif response.startswith('```'):
            response = response[3:]
        if response.endswith('```'):
            response = response[:-3]
        
        response = response.strip()
        
        # Ensure it starts and ends with braces
        if not response.startswith('{'):
            brace_pos = response.find('{')
            if brace_pos > 0:
                response = response[brace_pos:]
        
        if not response.endswith('}'):
            brace_pos = response.rfind('}')
            if brace_pos > 0:
                response = response[:brace_pos + 1]
        
        return response

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
        
        prompt = f"""Create web automation plan for: "{user_command}"

CRITICAL: Return ONLY valid JSON. No explanations, no comments, no extra text.
Start with {{ and end with }}. Use double quotes only.

Example response format:
{{
    "task_type": "search",
    "target_site": "google", 
    "steps": [
        {{
            "action": "open_browser",
            "params": {{}},
            "description": "open browser"
        }},
        {{
            "action": "search_google",
            "params": {{"query": "cats"}},
            "description": "search for cats"
        }}
    ],
    "safety_level": "safe",
    "expected_outcome": "search results displayed"
}}

Available actions:
- open_browser: {{}} 
- search_google: {{"query": "search terms"}}
- go_to_url: {{"url": "https://site.com"}}
- click_element: {{"text": "button text", "type": "button"}}
- type_text: {{"text": "input text", "element": "search"}}
- scroll_down: {{}}
- wait: {{"seconds": 2}}

Task types: search, navigation, interaction, automation
Target sites: google, youtube, other
Safety levels: safe, moderate, careful

Now create JSON plan for: "{user_command}"
"""
        
        try:
            response = call_gpt_system(prompt)
            
            # Pre-validate and clean the response
            response = self._validate_json_response(response)
            
            # Enhanced JSON parsing with multiple fallback strategies
            
            # Try direct parsing first
            try:
                plan = json.loads(response)
            except json.JSONDecodeError as e:
                print(f"⚠️ Initial JSON parse failed: {e}")
                
                # Advanced JSON cleanup for GPT response issues
                import re
                
                # Step 1: Extract only the JSON part
                # Remove any text before the first {
                first_brace = response.find('{')
                if first_brace > 0:
                    response = response[first_brace:]
                
                # Remove any text after the last }
                last_brace = response.rfind('}')
                if last_brace > 0:
                    response = response[:last_brace + 1]
                
                # Step 2: Fix common GPT JSON formatting issues
                
                # Fix unterminated strings by adding missing quotes
                lines = response.split('\n')
                fixed_lines = []
                for line_num, line in enumerate(lines):
                    original_line = line
                    line = line.strip()
                    
                    # Skip empty lines
                    if not line:
                        fixed_lines.append(original_line)
                        continue
                    
                    # Handle incomplete string values
                    if ':' in line and not line.endswith(',') and not line.endswith('}') and not line.endswith(']'):
                        # Check if this line has an opening quote but no closing quote
                        colon_pos = line.find(':')
                        value_part = line[colon_pos + 1:].strip()
                        
                        if value_part.startswith('"') and not (value_part.endswith('"') or value_part.endswith('",') or value_part.endswith('"}')):
                            # Add missing closing quote and comma
                            if line_num < len(lines) - 1:  # Not the last line
                                line = line + '",'
                            else:
                                line = line + '"'
                    
                    # Add missing commas after complete lines
                    if (line.endswith('"') or line.endswith('}') or line.endswith(']')) and not line.endswith(','):
                        # Check if next line exists and starts with a key or closing brace
                        if line_num < len(lines) - 1:
                            next_line = lines[line_num + 1].strip()
                            if next_line and (next_line.startswith('"') or next_line.startswith('{')):
                                line = line + ','
                    
                    fixed_lines.append(line)
                
                response = '\n'.join(fixed_lines)
                
                # Step 3: Additional cleanup
                # Fix trailing commas before closing brackets
                response = re.sub(r',(\s*[}\]])', r'\1', response)
                
                # Fix boolean values
                response = response.replace('True', 'true').replace('False', 'false').replace('None', 'null')
                
                # Fix single quotes (but be careful not to break content)
                response = re.sub(r"'([^']*)'(\s*:)", r'"\1"\2', response)  # Keys
                response = re.sub(r":\s*'([^']*)'", r': "\1"', response)  # Values
                
                # Try parsing the cleaned JSON
                try:
                    plan = json.loads(response)
                    print("✅ JSON fixed and parsed successfully")
                except json.JSONDecodeError as e2:
                    print(f"⚠️ Secondary JSON parse failed: {e2}")
                    print(f"Cleaned JSON snippet:\n{response[:300]}...")
                    
                    # Step 4: Emergency fallback - create minimal valid JSON
                    try:
                        # Extract basic info using regex
                        task_type_match = re.search(r'"task_type":\s*"([^"]*)"', response)
                        target_match = re.search(r'"target_site":\s*"([^"]*)"', response)
                        
                        # Create a minimal valid plan
                        plan = {
                            "task_type": task_type_match.group(1) if task_type_match else "automation",
                            "target_site": target_match.group(1) if target_match else "unknown",
                            "steps": [
                                {"action": "open_browser", "params": {}, "description": "open browser"},
                                {"action": "wait", "params": {"seconds": 2}, "description": "wait for page load"}
                            ],
                            "safety_level": "safe",
                            "expected_outcome": "basic automation completed"
                        }
                        print("🔧 Created emergency fallback plan")
                    except:
                        raise e2
            
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
            print("🔄 Using fallback planning...")
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
