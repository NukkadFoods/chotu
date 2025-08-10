#!/usr/bin/env python3
"""
🌐 CHOTU WEB AUTOMATION COORDINATOR
==================================
Main coordinator that combines all web automation components
"""

import os
import sys
import time
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

# Import web automation components
try:
    from .browser import WebCommander
    from .web_agent import WebTaskPlanner
    from .vision_engine import VisualFinder
except ImportError:
    # Handle relative imports for direct execution
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from browser import WebCommander
    from web_agent import WebTaskPlanner
    from vision_engine import VisualFinder

class WebAutomationCoordinator:
    """Main coordinator for all web automation tasks"""
    
    def __init__(self, headless: bool = False):
        self.commander = None
        self.planner = WebTaskPlanner()
        self.vision = VisualFinder()
        self.headless = headless
        
        # Session tracking
        self.session_active = False
        self.current_task = None
        self.task_history = []
        
        # Safety settings
        self.safety_mode = True
        self.max_task_duration = 300  # 5 minutes max per task
        self.require_confirmation = True
        
        print("🌐 WebAutomationCoordinator initialized")
        print(f"   Headless mode: {'ON' if headless else 'OFF'}")
        print(f"   Safety mode: {'ON' if self.safety_mode else 'OFF'}")
    
    def click_first_search_result(self, search_query: str = "") -> Dict[str, Any]:
        """
        Directly click the first search result using WebDriver
        This is a specialized method for search result clicking
        """
        try:
            # Ensure browser is started
            if not self.session_active:
                self._ensure_browser_ready()
            
            if not self.commander or not self.commander.driver:
                return {
                    "success": False,
                    "error": "Browser not available",
                    "search_query": search_query
                }
            
            # Use the browser's click first search result method
            success = self.commander.click_first_search_result(search_query)
            
            if success:
                return {
                    "success": True,
                    "message": f"Successfully clicked first search result for '{search_query}'",
                    "action": "clicked_first_result",
                    "search_query": search_query,
                    "browser": "WebDriver Chrome"
                }
            else:
                return {
                    "success": False,
                    "error": "Could not find or click first search result",
                    "message": f"Failed to click first search result for '{search_query}'",
                    "search_query": search_query
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Error clicking first search result for '{search_query}': {e}",
                "search_query": search_query
            }
    
    def _ensure_browser_ready(self):
        """Ensure the browser is ready for automation"""
        try:
            if not self.commander:
                self.commander = WebCommander(headless=self.headless)
            
            if not self.session_active:
                success = self.commander.start_session()
                if success:
                    self.session_active = True
                    print("🚀 Browser session started successfully")
                else:
                    print("❌ Failed to start browser session")
                    
        except Exception as e:
            print(f"❌ Error starting browser: {e}")
            raise
    
    def handle_web_command(self, command: str, context: Dict = None) -> Dict[str, Any]:
        """
        Main entry point for handling web automation commands
        
        Args:
            command: Natural language command from user
            context: Additional context about the task
            
        Returns:
            Dict: Result of the web automation task
        """
        
        print(f"\n🌐 HANDLING WEB COMMAND: {command}")
        print("=" * 60)
        
        task_start_time = datetime.now()
        
        try:
            # Step 1: Plan the task
            print("📋 Step 1: Planning web task...")
            plan = self.planner.plan_web_task(command, context)
            
            if not plan or not plan.get('steps'):
                return {
                    "success": False,
                    "error": "Could not create execution plan",
                    "command": command
                }
            
            # Step 2: Safety assessment
            print("🛡️ Step 2: Safety assessment...")
            if not self._assess_task_safety(plan, command):
                return {
                    "success": False,
                    "error": "Task blocked by safety assessment",
                    "plan": plan,
                    "command": command
                }
            
            # Step 3: Initialize browser session
            print("🚀 Step 3: Starting browser session...")
            if not self._start_session():
                return {
                    "success": False,
                    "error": "Could not start browser session",
                    "command": command
                }
            
            # Step 4: Execute the plan
            print("⚙️ Step 4: Executing plan...")
            execution_result = self._execute_plan(plan, command)
            
            # Step 5: Cleanup and reporting
            print("📊 Step 5: Task completion...")
            task_duration = (datetime.now() - task_start_time).total_seconds()
            
            result = {
                "success": execution_result.get("success", False),
                "command": command,
                "plan": plan,
                "execution_details": execution_result,
                "duration_seconds": task_duration,
                "timestamp": task_start_time.isoformat()
            }
            
            # Save successful workflows for learning
            if result["success"]:
                self.planner.save_successful_flow(command, plan, True)
                print("✅ Task completed successfully!")
            else:
                print("❌ Task failed")
            
            # Record in history
            self.task_history.append(result)
            
            return result
            
        except Exception as e:
            print(f"❌ Web automation failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "command": command,
                "timestamp": task_start_time.isoformat()
            }
        
        finally:
            # Always cleanup
            self._end_session()
    
    def _assess_task_safety(self, plan: Dict, command: str) -> bool:
        """Assess if the task is safe to execute"""
        
        safety_level = plan.get('safety_level', 'caution')
        
        if safety_level == 'dangerous':
            print("🚫 Task blocked: Marked as dangerous")
            return False
        
        # Check for risky actions
        risky_actions = ['purchase', 'buy', 'delete', 'remove', 'pay', 'transfer']
        
        for step in plan.get('steps', []):
            step_desc = step.get('description', '').lower()
            if any(risky in step_desc for risky in risky_actions):
                if self.require_confirmation:
                    print(f"⚠️ Risky action detected: {step.get('description')}")
                    print("   This action has been blocked for safety")
                    return False
        
        # Check target site reputation (basic)
        target_site = plan.get('target_site', '').lower()
        suspicious_patterns = ['temp', 'fake', 'phishing', 'scam']
        
        if any(pattern in target_site for pattern in suspicious_patterns):
            print(f"🚫 Suspicious target site: {target_site}")
            return False
        
        print(f"✅ Safety assessment passed (Level: {safety_level})")
        return True
    
    def _start_session(self) -> bool:
        """Start browser session"""
        
        if self.session_active and self.commander:
            return True
        
        try:
            self.commander = WebCommander(headless=self.headless)
            
            if self.commander.start_session():
                self.session_active = True
                print("✅ Browser session started")
                return True
            else:
                print("❌ Failed to start browser session")
                return False
                
        except Exception as e:
            print(f"❌ Session start error: {e}")
            return False
    
    def _end_session(self):
        """End browser session safely"""
        
        if self.commander:
            try:
                self.commander.end_session()
                self.commander = None
                self.session_active = False
                print("✅ Browser session ended")
            except Exception as e:
                print(f"⚠️ Session cleanup error: {e}")
    
    def _execute_plan(self, plan: Dict, original_command: str) -> Dict[str, Any]:
        """Execute the planned web automation steps"""
        
        steps = plan.get('steps', [])
        results = []
        overall_success = True
        
        print(f"⚙️ Executing {len(steps)} steps...")
        
        for i, step in enumerate(steps, 1):
            print(f"\n🔧 Step {i}/{len(steps)}: {step.get('description', step.get('action'))}")
            
            # Execute the step
            step_success = self.planner.execute_plan_step(step, self.commander)
            
            step_result = {
                "step_number": i,
                "action": step.get('action'),
                "success": step_success,
                "description": step.get('description', ''),
                "timestamp": datetime.now().isoformat()
            }
            
            results.append(step_result)
            
            if not step_success:
                print(f"❌ Step {i} failed")
                
                # Try recovery strategies
                recovery_success = self._attempt_step_recovery(step, i)
                
                if not recovery_success:
                    overall_success = False
                    break
            else:
                print(f"✅ Step {i} completed")
            
            # Small delay between steps
            time.sleep(0.5)
        
        # Take final screenshot for debugging
        if self.commander:
            screenshot_path = self.commander.take_screenshot(f"final_result_{int(time.time())}.png")
            
            # Optional: Analyze final page state
            if screenshot_path and overall_success:
                layout_analysis = self.vision.analyze_page_layout(screenshot_path)
                print(f"📊 Final page analysis: {layout_analysis.get('complexity')} layout")
        
        execution_result = {
            "success": overall_success,
            "steps_completed": len([r for r in results if r['success']]),
            "total_steps": len(steps),
            "step_results": results,
            "final_url": self.commander.get_page_info().get('url') if self.commander else None
        }
        
        return execution_result
    
    def _attempt_step_recovery(self, failed_step: Dict, step_number: int) -> bool:
        """Attempt to recover from a failed step"""
        
        print(f"🔄 Attempting recovery for step {step_number}...")
        
        action = failed_step.get('action')
        
        # Strategy 1: Take screenshot and try visual fallback
        if self.commander and action in ['click', 'fill']:
            screenshot = self.commander.take_screenshot(f"recovery_step_{step_number}.png")
            
            if screenshot and action == 'click':
                # Try to find the element visually
                target_text = failed_step.get('target', '')
                coords = self.vision.find_text_element(screenshot, target_text)
                
                if coords:
                    print(f"🎯 Found element visually at {coords}")
                    # Could implement click at coordinates here
                    return False  # For now, just report the finding
        
        # Strategy 2: Wait and retry
        if action in ['navigate', 'wait']:
            print("⏳ Waiting 3 seconds before retry...")
            time.sleep(3)
            return self.planner.execute_plan_step(failed_step, self.commander)
        
        # Strategy 3: Try alternative selectors
        if action in ['click', 'fill'] and 'selector_hint' in failed_step:
            print("🔍 Trying alternative element selection...")
            # This would need more sophisticated fallback logic
            return False
        
        print(f"❌ Recovery failed for step {step_number}")
        return False
    
    def get_session_status(self) -> Dict[str, Any]:
        """Get current session status"""
        
        status = {
            "session_active": self.session_active,
            "tasks_completed": len(self.task_history),
            "current_task": self.current_task,
            "safety_mode": self.safety_mode
        }
        
        if self.commander:
            page_info = self.commander.get_page_info()
            status.update({
                "current_url": page_info.get('url'),
                "page_title": page_info.get('title'),
                "page_ready": page_info.get('ready_state') == 'complete'
            })
        
        return status
    
    def emergency_stop(self):
        """Emergency stop all web automation"""
        
        print("🚨 EMERGENCY STOP - Halting all web automation")
        
        self.current_task = None
        self._end_session()
        
        print("✅ Emergency stop completed")

# Example usage and testing
if __name__ == "__main__":
    coordinator = WebAutomationCoordinator(headless=False)
    
    test_commands = [
        "Search Google for Python tutorials",
        "Go to YouTube and search for machine learning",
        "Navigate to GitHub"
    ]
    
    for command in test_commands:
        print(f"\n🧪 Testing: {command}")
        result = coordinator.handle_web_command(command)
        
        print(f"Result: {'SUCCESS' if result.get('success') else 'FAILED'}")
        if result.get('error'):
            print(f"Error: {result['error']}")
        
        time.sleep(2)  # Pause between tests
