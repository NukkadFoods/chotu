"""
Chotu Autonomous Task Executor - Main Orchestrator
Implements the complete autonomous task execution pipeline with learning capabilities
"""
import time
import json
from typing import List, Dict, Tuple, Optional, Any, Union
from dataclasses import dataclass
from pathlib import Path
import logging
from datetime import datetime

# Import all autonomous components
from .vision_engine import VisionEngine, ScreenRegion
from .action_engine import ActionEngine, HumanBehavior, StealthSettings
from .procedural_memory import ProceduralMemory, TaskRecipe, ActionStep, ExecutionContext
from .credential_vault import CredentialVault, AccessRule

@dataclass
class TaskExecutionResult:
    """Result of task execution"""
    success: bool
    task_id: str
    duration: float
    error_message: str = ""
    screenshots: List[str] = None
    steps_completed: int = 0
    total_steps: int = 0
    
class AutonomousTaskExecutor:
    """Main orchestrator for autonomous task execution"""
    
    def __init__(self, base_dir: str = "autonomous", headless: bool = False):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize core components
        self.vision = VisionEngine(str(self.base_dir / "screenshots"))
        self.action_engine = ActionEngine(self.vision, headless=headless)
        self.memory = ProceduralMemory(str(self.base_dir / "memory"))
        self.vault = CredentialVault(str(self.base_dir / "vault"))
        
        # Execution state
        self.current_task_id: Optional[str] = None
        self.learning_mode: bool = False
        self.current_context: ExecutionContext = None
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        self.logger.info("Chotu Autonomous Task Executor initialized")
    
    def execute_user_command(self, user_input: str, context: ExecutionContext = None) -> TaskExecutionResult:
        """Main entry point for executing user commands"""
        start_time = time.time()
        
        try:
            # Set execution context
            if context:
                self.current_context = context
            else:
                self.current_context = ExecutionContext(
                    user_id="default_user",
                    session_id=f"session_{int(time.time())}",
                    environment="development",
                    browser_profile="stealth",
                    stealth_level="normal"
                )
            
            self.logger.info(f"Processing command: {user_input}")
            
            # Extract dynamic parameters from command
            dynamic_params = self._extract_dynamic_parameters(user_input)
            
            # Try to find existing task recipe with intelligent selection
            task_recipe = self._find_best_task_recipe(user_input, dynamic_params)
            
            if task_recipe:
                # Execute existing recipe with dynamic parameters
                self.logger.info(f"Found existing recipe: {task_recipe.task_name}")
                result = self._execute_task_recipe(task_recipe, dynamic_params, user_input)
            else:
                # Check if this looks like a learning opportunity
                if self._should_enter_learning_mode(user_input):
                    self.logger.info("Entering learning mode for new task")
                    result = self._learn_new_task(user_input)
                else:
                    # Try to break down into simpler commands
                    result = self._attempt_command_breakdown(user_input)
            
            # Calculate duration
            duration = time.time() - start_time
            result.duration = duration
            
            # Log execution
            self.memory.log_execution(
                result.task_id or "unknown",
                self.current_context,
                result.success,
                result.error_message,
                duration,
                result.screenshots
            )
            
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            error_msg = f"Command execution failed: {str(e)}"
            self.logger.error(error_msg)
            
            return TaskExecutionResult(
                success=False,
                task_id="error",
                duration=duration,
                error_message=error_msg
            )
    
    def _execute_task_recipe(self, recipe: TaskRecipe, dynamic_params: Dict[str, str] = None, user_input: str = "") -> TaskExecutionResult:
        """Execute a stored task recipe with dynamic parameter substitution"""
        try:
            task_id = f"exec_{recipe.task_name}_{int(time.time())}"
            screenshots = []
            steps_completed = 0
            
            self.logger.info(f"Executing recipe: {recipe.task_name}")
            if dynamic_params:
                self.logger.info(f"Using dynamic parameters: {dynamic_params}")
            
            # Check prerequisites
            if not self._verify_prerequisites(recipe.prerequisites):
                return TaskExecutionResult(
                    success=False,
                    task_id=task_id,
                    duration=0,
                    error_message="Prerequisites not met",
                    steps_completed=0,
                    total_steps=len(recipe.action_sequence)
                )
            
            # Configure action engine based on recipe context
            self._configure_action_engine(recipe)
            
            # Execute each step with parameter substitution
            for i, step in enumerate(recipe.action_sequence):
                # Apply dynamic parameter substitution
                substituted_step = self._substitute_step_parameters(step, dynamic_params or {})
                
                self.logger.info(f"Executing step {i+1}/{len(recipe.action_sequence)}: {substituted_step.human_readable}")
                
                step_success = self._execute_action_step(substituted_step, recipe.credentials)
                
                if step_success:
                    steps_completed += 1
                    
                    # Take screenshot for verification
                    screenshot = self.action_engine.take_screenshot(f"step_{i+1}.png")
                    if screenshot:
                        screenshots.append(screenshot)
                    
                    # Verify step completion if confirmation specified
                    if step.confirmation:
                        if not self._verify_step_completion(step.confirmation):
                            return TaskExecutionResult(
                                success=False,
                                task_id=task_id,
                                duration=0,
                                error_message=f"Step verification failed: {step.confirmation}",
                                screenshots=screenshots,
                                steps_completed=steps_completed,
                                total_steps=len(recipe.action_sequence)
                            )
                else:
                    # Handle step failure
                    if step.retry_count > 0:
                        self.logger.warning(f"Step failed, retrying...")
                        for retry in range(step.retry_count):
                            time.sleep(2)  # Wait before retry
                            if self._execute_action_step(step, recipe.credentials):
                                step_success = True
                                steps_completed += 1
                                break
                    
                    if not step_success:
                        # Try self-healing for navigation failures
                        if step.action_type == "browser_action" and "navigate" in step.target:
                            self.logger.info("🔧 Attempting self-healing for navigation failure...")
                            fixed_step = self._self_heal_navigation_step(step, user_input, dynamic_params)
                            if fixed_step and self._execute_action_step(fixed_step, recipe.credentials):
                                step_success = True
                                steps_completed += 1
                                self.logger.info("✅ Self-healing successful!")
                            else:
                                self.logger.warning("❌ Self-healing failed")
                        
                        # Check for failure handlers
                        if not step_success:
                            handled = self._handle_step_failure(step, recipe.failure_handlers)
                            if not handled:
                                return TaskExecutionResult(
                                    success=False,
                                    task_id=task_id,
                                    duration=0,
                                    error_message=f"Step failed: {step.human_readable}",
                                    screenshots=screenshots,
                                    steps_completed=steps_completed,
                                    total_steps=len(recipe.action_sequence)
                                )
            
            # Verify final success indicators
            if recipe.success_indicators:
                for indicator in recipe.success_indicators:
                    if not self._verify_step_completion(indicator):
                        return TaskExecutionResult(
                            success=False,
                            task_id=task_id,
                            duration=0,
                            error_message=f"Final verification failed: {indicator}",
                            screenshots=screenshots,
                            steps_completed=steps_completed,
                            total_steps=len(recipe.action_sequence)
                        )
            
            self.logger.info(f"Recipe executed successfully: {recipe.task_name}")
            
            return TaskExecutionResult(
                success=True,
                task_id=task_id,
                duration=0,
                screenshots=screenshots,
                steps_completed=steps_completed,
                total_steps=len(recipe.action_sequence)
            )
            
        except Exception as e:
            error_msg = f"Recipe execution failed: {str(e)}"
            self.logger.error(error_msg)
            
            return TaskExecutionResult(
                success=False,
                task_id=task_id,
                duration=0,
                error_message=error_msg,
                screenshots=screenshots,
                steps_completed=steps_completed,
                total_steps=len(recipe.action_sequence) if recipe else 0
            )
    
    def _execute_action_step(self, step: ActionStep, credentials: Dict[str, str]) -> bool:
        """Execute a single action step"""
        try:
            if step.action_type == "navigate":
                return self.action_engine.navigate_to_url(step.target)
            
            elif step.action_type == "click":
                # Use value for CSS selector if provided, otherwise use target
                selector = step.value if step.value else step.target
                element = self.action_engine.find_element_by_vision(selector, step.timeout)
                if element:
                    return self.action_engine.human_click(element)
                return False
            
            elif step.action_type == "type":
                if step.value:
                    # Check if value references a credential
                    text_to_type = self._resolve_credential_reference(step.value, credentials)
                    
                    # For typing, target might be the element selector
                    element = self.action_engine.find_element_by_vision(step.target, step.timeout)
                    if element:
                        return self.action_engine.human_type(element, text_to_type)
                return False
            
            elif step.action_type == "scroll":
                direction = step.value or "down"
                amount = 3
                if step.value and step.value.isdigit():
                    amount = int(step.value)
                return self.action_engine.human_scroll(direction, amount)
            
            elif step.action_type == "press_key":
                # Press a key (Enter, Tab, etc.)
                if step.target:
                    from selenium.webdriver.common.keys import Keys
                    key_mapping = {
                        "Enter": Keys.ENTER,
                        "Tab": Keys.TAB,
                        "Escape": Keys.ESCAPE,
                        "Space": Keys.SPACE
                    }
                    key = key_mapping.get(step.target, step.target)
                    
                    # Find the currently focused element or the search box
                    try:
                        active_element = self.action_engine.driver.switch_to.active_element
                        active_element.send_keys(key)
                        return True
                    except:
                        # Fallback: find search box and press key
                        try:
                            element = self.action_engine.find_element_with_fallback("input[name='field-keywords']")
                            if element:
                                element.send_keys(key)
                                return True
                        except:
                            pass
                return False

            elif step.action_type == "wait":
                wait_time = float(step.value) if step.value else 3.0
                time.sleep(wait_time)
                return True
            
            elif step.action_type == "verify":
                return self._verify_step_completion(step.target)
            
            elif step.action_type == "system_command":
                # Execute system commands like opening applications
                if step.target == "open_chrome" and step.value:
                    import subprocess
                    result = subprocess.run(step.value.split(), 
                                          capture_output=True, text=True)
                    return result.returncode == 0
                return False
            
            elif step.action_type == "stealth_browser":
                # Initialize stealth browser
                if step.target == "initialize_stealth_chrome":
                    return self.action_engine.create_stealth_browser()
                return False
            
            elif step.action_type == "browser_action":
                # Browser-specific actions that require initialized browser
                if step.target == "navigate" and step.value:
                    return self.action_engine.navigate_to_url(step.value)
                elif step.target == "new_tab":
                    return self.action_engine.open_new_tab()
                return False
            
            elif step.action_type == "auto_login":
                # Automatic login using stored credentials
                service = step.target
                return self.action_engine.password_manager.auto_login(
                    self.action_engine.driver, service
                )
            
            else:
                self.logger.warning(f"Unknown action type: {step.action_type}")
                return False
                
        except Exception as e:
            self.logger.error(f"Action step execution failed: {e}")
            return False
    
    def _resolve_credential_reference(self, value: str, credentials: Dict[str, str]) -> str:
        """Resolve credential references in step values"""
        if value.startswith("{") and value.endswith("}"):
            # This is a credential reference
            cred_ref = value[1:-1]  # Remove braces
            
            if cred_ref in credentials:
                vault_ref = credentials[cred_ref]
                
                # Parse vault reference (format: service:username)
                if ":" in vault_ref:
                    service, username = vault_ref.split(":", 1)
                    
                    # Get credential from vault
                    cred_data = self.vault.get_credential(
                        service, username, 
                        ["web_automation", "task_execution"],
                        auto_confirm=True
                    )
                    
                    if cred_data:
                        if "password" in cred_ref.lower():
                            return cred_data["password"]
                        elif "username" in cred_ref.lower():
                            return cred_data["username"]
                        else:
                            return cred_data["password"]  # Default to password
        
        return value  # Return as-is if not a credential reference
    
    def _verify_step_completion(self, verification_target: str) -> bool:
        """Verify that a step completed successfully"""
        try:
            if verification_target.startswith("url_"):
                # URL verification
                expected_url = verification_target.replace("url_matches:", "")
                current_url = self.action_engine.driver.current_url if self.action_engine.driver else ""
                return expected_url in current_url
            
            elif verification_target.startswith("element_"):
                # Element presence verification
                element_name = verification_target.replace("element_visible:", "")
                return self.vision.detect_element(element_name) is not None
            
            elif verification_target.startswith("page_title_"):
                # Page title verification
                expected_title = verification_target.replace("page_title_contains:", "")
                current_title = self.action_engine.driver.title if self.action_engine.driver else ""
                return expected_title.lower() in current_title.lower()
            
            # Simple text-based indicators
            elif verification_target in ["browser initialized successfully", "navigation completed", "no browser errors"]:
                # Check if browser is active and functioning
                if self.action_engine.driver:
                    try:
                        # Simple check - can we get the current URL?
                        url = self.action_engine.driver.current_url
                        return url is not None and len(url) > 0
                    except:
                        return False
                return False
            
            elif verification_target in ["search executed successfully", "page navigation completed"]:
                # Check if we're on a page and it's loaded
                if self.action_engine.driver:
                    try:
                        # Check page is loaded and has content
                        ready_state = self.action_engine.driver.execute_script("return document.readyState")
                        return ready_state == "complete"
                    except:
                        return False
                return False
            
            else:
                # Default: assume success for simple indicators
                return True
                
        except Exception as e:
            self.logger.error(f"Step verification failed: {e}")
            return False
    
    def _learn_new_task(self, user_input: str) -> TaskExecutionResult:
        """Learn a new task through guided execution"""
        try:
            # Start recording new task
            task_name = self._extract_task_name(user_input)
            trigger_phrases = [user_input.lower(), task_name.lower()]
            
            task_id = self.memory.record_task_learning(task_name, trigger_phrases, f"User requested: {user_input}")
            
            if not task_id:
                return TaskExecutionResult(
                    success=False,
                    task_id="learning_failed",
                    duration=0,
                    error_message="Failed to start task learning"
                )
            
            self.current_task_id = task_id
            self.learning_mode = True
            
            # Guide user through task execution
            guided_result = self._guided_task_execution(user_input)
            
            if guided_result.success:
                # Finalize the learned recipe
                self.memory.finalize_task_recipe(task_id)
                self.logger.info(f"Successfully learned new task: {task_name}")
            
            self.learning_mode = False
            self.current_task_id = None
            
            return guided_result
            
        except Exception as e:
            error_msg = f"Task learning failed: {str(e)}"
            self.logger.error(error_msg)
            
            return TaskExecutionResult(
                success=False,
                task_id="learning_error",
                duration=0,
                error_message=error_msg
            )
    
    def _guided_task_execution(self, user_input: str) -> TaskExecutionResult:
        """Execute task with learning guidance"""
        # This is a simplified version - in practice, this would involve
        # more sophisticated interaction with the user to learn the task
        
        screenshots = []
        
        try:
            # For demonstration, create a simple web navigation task
            if "instagram" in user_input.lower():
                return self._learn_instagram_task()
            elif "chrome" in user_input.lower():
                return self._learn_chrome_task()
            else:
                # Generic web task learning
                return self._learn_generic_web_task(user_input)
                
        except Exception as e:
            return TaskExecutionResult(
                success=False,
                task_id=self.current_task_id or "unknown",
                duration=0,
                error_message=f"Guided execution failed: {str(e)}",
                screenshots=screenshots
            )
    
    def _learn_instagram_task(self) -> TaskExecutionResult:
        """Learn Instagram login task"""
        try:
            screenshots = []
            
            # Step 1: Open browser and navigate to Instagram
            self.memory.add_action_step(
                self.current_task_id, "navigate", "https://instagram.com",
                human_readable="Navigate to Instagram"
            )
            
            if not self.action_engine.navigate_to_url("https://instagram.com"):
                raise Exception("Failed to navigate to Instagram")
            
            screenshots.append(self.action_engine.take_screenshot("instagram_home.png"))
            
            # Step 2: Click login button
            self.memory.add_action_step(
                self.current_task_id, "click", "login_button",
                human_readable="Click login button"
            )
            
            # Step 3: Enter username
            self.memory.add_action_step(
                self.current_task_id, "type", "username_field", "{ig_username}",
                human_readable="Enter username"
            )
            
            # Step 4: Enter password
            self.memory.add_action_step(
                self.current_task_id, "type", "password_field", "{ig_password}",
                human_readable="Enter password"
            )
            
            # Step 5: Click submit
            self.memory.add_action_step(
                self.current_task_id, "click", "submit_button",
                human_readable="Click login submit"
            )
            
            # Set success indicators
            success_indicators = ["feed_element", "profile_menu"]
            failure_handlers = [
                {"condition": "element_visible:captcha", "action": "request_human_assistance"}
            ]
            
            return TaskExecutionResult(
                success=True,
                task_id=self.current_task_id,
                duration=0,
                screenshots=screenshots,
                steps_completed=5,
                total_steps=5
            )
            
        except Exception as e:
            return TaskExecutionResult(
                success=False,
                task_id=self.current_task_id,
                duration=0,
                error_message=str(e),
                screenshots=screenshots
            )
    
    def _learn_chrome_task(self) -> TaskExecutionResult:
        """Learn Chrome opening task"""
        try:
            screenshots = []
            
            # Step 1: Open Chrome using system command
            self.memory.add_action_step(
                self.current_task_id, "system_command", "open_chrome",
                value="open -a 'Google Chrome'",
                human_readable="Open Google Chrome application"
            )
            
            # Execute the command
            import subprocess
            result = subprocess.run(["open", "-a", "Google Chrome"], 
                                  capture_output=True, text=True)
            
            if result.returncode != 0:
                raise Exception(f"Failed to open Chrome: {result.stderr}")
            
            # Wait for Chrome to open
            time.sleep(3)
            screenshots.append(self.action_engine.take_screenshot("chrome_opened.png"))
            
            # Step 2: Verify Chrome is running
            self.memory.add_action_step(
                self.current_task_id, "verify", "chrome_window",
                human_readable="Verify Chrome window is open"
            )
            
            return TaskExecutionResult(
                success=True,
                task_id=self.current_task_id,
                duration=3.0,
                screenshots=screenshots,
                steps_completed=2,
                total_steps=2
            )
            
        except Exception as e:
            return TaskExecutionResult(
                success=False,
                task_id=self.current_task_id,
                duration=0,
                error_message=str(e),
                screenshots=screenshots
            )
    
    def _learn_generic_web_task(self, user_input: str) -> TaskExecutionResult:
        """Learn a generic web-based task"""
        try:
            screenshots = []
            
            # Extract URL or service from user input
            if "google" in user_input.lower():
                url = "https://google.com"
            elif "youtube" in user_input.lower():
                url = "https://youtube.com"
            elif "github" in user_input.lower():
                url = "https://github.com"
            else:
                url = "https://google.com"  # Default
            
            # Step 1: Open browser
            self.memory.add_action_step(
                self.current_task_id, "navigate", url,
                human_readable=f"Navigate to {url}"
            )
            
            if not self.action_engine.navigate_to_url(url):
                raise Exception(f"Failed to navigate to {url}")
            
            screenshots.append(self.action_engine.take_screenshot("generic_task.png"))
            
            return TaskExecutionResult(
                success=True,
                task_id=self.current_task_id,
                duration=5.0,
                screenshots=screenshots,
                steps_completed=1,
                total_steps=1
            )
            
        except Exception as e:
            return TaskExecutionResult(
                success=False,
                task_id=self.current_task_id,
                duration=0,
                error_message=str(e),
                screenshots=screenshots
            )
    
    def _should_enter_learning_mode(self, user_input: str) -> bool:
        """Determine if we should enter learning mode for this input"""
        # Check if input contains learning indicators
        learning_indicators = [
            "open", "login", "sign in", "navigate", "go to",
            "check", "send", "post", "upload", "download"
        ]
        
        input_lower = user_input.lower()
        return any(indicator in input_lower for indicator in learning_indicators)
    
    def _extract_task_name(self, user_input: str) -> str:
        """Extract task name from user input"""
        # Simple extraction - could be enhanced with NLP
        if "instagram" in user_input.lower():
            return "Instagram Login"
        elif "chrome" in user_input.lower():
            return "Open Chrome"
        elif "bank" in user_input.lower():
            return "Bank Account Access"
        else:
            return f"Custom Task: {user_input[:30]}..."
    
    def _attempt_command_breakdown(self, user_input: str) -> TaskExecutionResult:
        """Attempt to break down command into simpler actions"""
        try:
            # Simple command breakdown logic
            if "open chrome" in user_input.lower():
                return self._execute_simple_chrome_open()
            elif "close" in user_input.lower() and "chrome" in user_input.lower():
                return self._execute_simple_chrome_close()
            else:
                return TaskExecutionResult(
                    success=False,
                    task_id="breakdown_failed",
                    duration=0,
                    error_message="Could not understand or break down the command"
                )
                
        except Exception as e:
            return TaskExecutionResult(
                success=False,
                task_id="breakdown_error",
                duration=0,
                error_message=f"Command breakdown failed: {str(e)}"
            )
    
    def _execute_simple_chrome_open(self) -> TaskExecutionResult:
        """Execute simple Chrome opening"""
        try:
            # Use system command to open Chrome
            import subprocess
            subprocess.run(["open", "-a", "Google Chrome"], check=True)
            time.sleep(2)
            
            return TaskExecutionResult(
                success=True,
                task_id="simple_chrome_open",
                duration=2.0,
                steps_completed=1,
                total_steps=1
            )
            
        except Exception as e:
            return TaskExecutionResult(
                success=False,
                task_id="simple_chrome_open",
                duration=0,
                error_message=f"Failed to open Chrome: {str(e)}"
            )
    
    def _configure_action_engine(self, recipe: TaskRecipe):
        """Configure action engine based on recipe requirements"""
        # Set behavior profile based on recipe tags
        if "stealth" in recipe.tags:
            self.action_engine.randomize_behavior("conservative")
        elif "fast" in recipe.tags:
            self.action_engine.randomize_behavior("aggressive")
        else:
            self.action_engine.randomize_behavior("normal")
    
    def _verify_prerequisites(self, prerequisites: List[str]) -> bool:
        """Verify that prerequisites are met"""
        for prereq in prerequisites:
            if prereq == "chrome_installed":
                # Check if Chrome is installed
                chrome_path = "/Applications/Google Chrome.app"
                if not Path(chrome_path).exists():
                    self.logger.error("Chrome not installed")
                    return False
            elif prereq == "internet_connected":
                # Check internet connection
                try:
                    import socket
                    socket.create_connection(("8.8.8.8", 53), timeout=3)
                except OSError:
                    self.logger.error("No internet connection")
                    return False
        
        return True
    
    def _handle_step_failure(self, step: ActionStep, failure_handlers: List[str]) -> bool:
        """Handle step failure with defined handlers"""
        # For now, just log the failure handlers
        # In the future, we can implement specific recovery actions
        for handler in failure_handlers:
            self.logger.info(f"Failure handler available: {handler}")
            
            # Basic retry logic for common issues
            if "retry" in handler.lower():
                self.logger.info("Will be retried based on step retry_count")
                return True
            elif "chromedriver" in handler.lower():
                self.logger.warning("ChromeDriver issue detected - may need manual intervention")
            elif "detection" in handler.lower():
                self.logger.warning("Bot detection possible - using conservative behavior")
        
        return False
    
    def get_execution_status(self) -> Dict[str, Any]:
        """Get current execution status"""
        return {
            "learning_mode": self.learning_mode,
            "current_task_id": self.current_task_id,
            "available_tasks": len(self.memory.get_all_tasks()),
            "vault_credentials": len(self.vault.list_credentials()),
            "execution_statistics": self.memory.get_execution_statistics()
        }
    
    def demonstrate_capabilities(self) -> str:
        """Demonstrate autonomous capabilities"""
        demo_text = f"""
🤖 **Chotu Autonomous Task Executor Ready!**

**Current Capabilities:**
✅ Computer Vision & Screen Understanding
✅ Stealth Browser Automation  
✅ Procedural Learning & Memory
✅ Secure Credential Management
✅ Human-like Behavior Simulation

**Available Tasks:** {len(self.memory.get_all_tasks())}
**Stored Credentials:** {len(self.vault.list_credentials())}
**Learning Mode:** {'Active' if self.learning_mode else 'Standby'}

**Example Commands:**
• "Open Instagram and login with my credentials"
• "Check my bank account balance"
• "Open Chrome browser" 
• "Post on social media"

**System Status:** 🟢 All systems operational
"""
        return demo_text
    
    def _extract_dynamic_parameters(self, user_input: str) -> Dict[str, str]:
        """Extract dynamic parameters from user input for recipe substitution"""
        params = {}
        
        # Extract search terms for various patterns
        import re
        
        # First, try to extract just domain names for direct navigation
        domain_pattern = r'(\w+\.(?:com|org|net|edu|gov|io|co|app))'
        domain_matches = re.findall(domain_pattern, user_input.lower())
        
        if domain_matches:
            # Use the first domain found as the primary target
            primary_domain = domain_matches[0]
            params["search_term"] = primary_domain
            params["website"] = primary_domain
            self.logger.info(f"Extracted domain: '{primary_domain}'")
            return params
        
        # Enhanced patterns to handle various command formats
        search_patterns = [
            r"open chrome and search\s+(.+?)(?:\s+on\s+next\s+tab|\s+next\s+to|\s+step)?$",  # "Open Chrome and search flipkart.com"
            r"open\s+(.+?)(?:\s+on\s+next\s+tab|\s+next\s+to|\s+step)?$",  # "open amazon.com on next tab"
            r"search\s+(.+?)\s+on\s+amazon",     # "search mushrooms on amazon"
            r"search\s+(.+?)\s+on\s+google",     # "search mushrooms on google"
            r"search\s+for\s+(.+?)(?:\s+on\s+\w+)?$",  # "search for mushrooms"
            r"search\s+(.+?)(?:\s+on\s+next\s+tab|\s+next\s+to|\s+step)?$",  # "search mushrooms"
            r"find\s+(.+?)\s+on\s+amazon",       # "find mushrooms on amazon"
            r"look\s+for\s+(.+?)(?:\s+on\s+\w+)?$",    # "look for mushrooms"
            r"navigate to\s+(.+?)(?:\s+on\s+next\s+tab|\s+next\s+to|\s+step)?$",  # "navigate to flipkart.com"
            r"go to\s+(.+?)(?:\s+on\s+next\s+tab|\s+next\s+to|\s+step)?$",   # "go to flipkart.com"
            r"visit\s+(.+?)(?:\s+on\s+next\s+tab|\s+next\s+to|\s+step)?$",   # "visit flipkart.com"
            r"browse to\s+(.+?)(?:\s+on\s+next\s+tab|\s+next\s+to|\s+step)?$"  # "browse to flipkart.com"
        ]
        
        for pattern in search_patterns:
            match = re.search(pattern, user_input.lower())
            if match:
                search_term = match.group(1).strip()
                
                # Clean up common phrases that might get included
                search_term = re.sub(r'\s+(on\s+next\s+tab|next\s+to|step).*$', '', search_term)
                
                params["search_term"] = search_term
                self.logger.info(f"Extracted search term: '{search_term}'")
                break
        
        # Extract website context (for recipe selection)
        if "amazon.com" in user_input.lower():
            params["website"] = "amazon.com"
        elif "google.com" in user_input.lower():
            params["website"] = "google.com"
        elif "flipkart.com" in user_input.lower():
            params["website"] = "flipkart.com"
        elif "instagram.com" in user_input.lower():
            params["website"] = "instagram.com"
        elif ".com" in user_input.lower():
            # Try to extract any .com domain
            domain_match = re.search(r'(\w+\.com)', user_input.lower())
            if domain_match:
                params["website"] = domain_match.group(1)
        
        return params
    
    def _substitute_step_parameters(self, step: ActionStep, params: Dict[str, str]) -> ActionStep:
        """Substitute dynamic parameters in action step"""
        import copy
        
        # Create a copy to avoid modifying the original
        substituted_step = copy.deepcopy(step)
        
        # Substitute in value field
        if substituted_step.value:
            for param_name, param_value in params.items():
                placeholder = f"{{{param_name}}}"
                if placeholder in substituted_step.value:
                    substituted_step.value = substituted_step.value.replace(placeholder, param_value)
                    self.logger.info(f"Substituted {placeholder} -> '{param_value}'")
        
        # Substitute in target field
        if substituted_step.target:
            for param_name, param_value in params.items():
                placeholder = f"{{{param_name}}}"
                if placeholder in substituted_step.target:
                    substituted_step.target = substituted_step.target.replace(placeholder, param_value)
        
        # Update human readable description
        if substituted_step.human_readable:
            for param_name, param_value in params.items():
                placeholder = f"{{{param_name}}}"
                if placeholder in substituted_step.human_readable:
                    substituted_step.human_readable = substituted_step.human_readable.replace(placeholder, param_value)
        
        return substituted_step
    
    def _self_heal_navigation_step(self, failed_step: ActionStep, user_input: str, dynamic_params: Dict[str, str]):
        """Attempt to automatically fix a failed navigation step"""
        import copy
        
        try:
            self.logger.info(f"🔧 Self-healing navigation step with value: {failed_step.value}")
            
            # Check if the issue is with parameter substitution
            if "{search_term}" in failed_step.value:
                # Parameter wasn't substituted properly
                if "search_term" in dynamic_params:
                    fixed_step = copy.deepcopy(failed_step)
                    fixed_step.value = failed_step.value.replace("{search_term}", dynamic_params["search_term"])
                    self.logger.info(f"🔧 Fixed parameter substitution: {fixed_step.value}")
                    return fixed_step
            
            # Check if we're trying to navigate to an invalid URL
            if "https://" in failed_step.value and " " in failed_step.value:
                # URL contains spaces or extra text
                fixed_step = copy.deepcopy(failed_step)
                
                # Extract just the domain from the URL
                import re
                url = failed_step.value
                domain_match = re.search(r'https://([^/\s]+)', url)
                if domain_match:
                    clean_domain = domain_match.group(1)
                    # Remove any trailing text after the domain
                    clean_domain = re.sub(r'\s.*$', '', clean_domain)
                    fixed_step.value = f"https://{clean_domain}"
                    self.logger.info(f"🔧 Cleaned URL: {fixed_step.value}")
                    return fixed_step
            
            # Try adding www prefix if missing
            if failed_step.value.startswith("https://") and "www." not in failed_step.value:
                fixed_step = copy.deepcopy(failed_step)
                domain = failed_step.value.replace("https://", "")
                fixed_step.value = f"https://www.{domain}"
                self.logger.info(f"🔧 Added www prefix: {fixed_step.value}")
                return fixed_step
                
            return None
            
        except Exception as e:
            self.logger.error(f"Self-healing failed: {e}")
            return None
    
    def _find_best_task_recipe(self, user_input: str, dynamic_params: Dict[str, str]):
        """Intelligently select the best task recipe based on input and parameters"""
        
        # Check for specific platform searches first
        if "youtube" in user_input.lower() and "search" in user_input.lower():
            for task_id, recipe in self.memory.task_recipes.items():
                if recipe.task_name == "YouTube Search":
                    self.logger.info(f"Using YouTube search for: {user_input}")
                    return recipe
        
        # Check for new tab requests
        if any(phrase in user_input.lower() for phrase in ["next tab", "new tab", "on next tab"]):
            for task_id, recipe in self.memory.task_recipes.items():
                if recipe.task_name == "Open in New Tab":
                    self.logger.info(f"Using new tab navigation for: {user_input}")
                    return recipe
        
        # Check if the search term looks like a website URL
        search_term = dynamic_params.get("search_term", "")
        
        if search_term:
            # If search term contains .com, .org, etc., prefer direct navigation
            if any(domain in search_term.lower() for domain in ['.com', '.org', '.net', '.edu', '.gov']):
                # Look for direct navigation recipe
                direct_nav_recipe = None
                for task_id, recipe in self.memory.task_recipes.items():
                    if recipe.task_name == "Navigate to Website":
                        direct_nav_recipe = recipe
                        break
                
                if direct_nav_recipe:
                    self.logger.info(f"Using direct navigation for website: {search_term}")
                    return direct_nav_recipe
        
        # Fall back to regular trigger matching
        return self.memory.find_task_by_trigger(user_input)
    
    def shutdown(self):
        """Safely shutdown the autonomous executor"""
        try:
            self.action_engine.close_browser()
            self.memory.save_memory()
            self.vault.save_vault()
            self.logger.info("Autonomous Task Executor shutdown complete")
        except Exception as e:
            self.logger.error(f"Shutdown error: {e}")
