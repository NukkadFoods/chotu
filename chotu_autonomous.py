"""
Enhanced Chotu with Autonomous Task Execution Capabilities
Integrates computer vision, stealth automation, and procedural learning
"""
import asyncio
import json
import time
from typing import Dict, List, Optional, Any
from pathlib import Path
import logging

# Import existing Chotu components
try:
    from memory.enhanced_intelligent_processor import EnhancedIntelligentProcessor
    from vision.vision_system import VisionSystem
    from browser.stealth_browser import StealthBrowser
except ImportError:
    # Fallback for standalone execution
    pass

# Import autonomous components
from autonomous import (
    AutonomousTaskExecutor, 
    TaskExecutionResult,
    ExecutionContext,
    VisionEngine,
    ActionEngine,
    ProceduralMemory,
    CredentialVault
)

class ChouAutonomous:
    """Enhanced Chotu with full autonomous task execution capabilities"""
    
    def __init__(self, config_path: str = "config/chotu_config.json"):
        self.config_path = config_path
        self.config = self._load_config()
        
        # Initialize autonomous executor
        self.autonomous_executor = AutonomousTaskExecutor(
            base_dir="autonomous",
            headless=self.config.get("headless_mode", False)
        )
        
        # Initialize enhanced processor if available
        try:
            self.intelligent_processor = EnhancedIntelligentProcessor()
        except:
            self.intelligent_processor = None
        
        # Session state
        self.session_id = f"session_{int(time.time())}"
        self.autonomous_mode = False
        self.learning_mode = False
        
        # Context tracking for follow-up commands
        self.recent_commands = []
        self.current_context = {}
        self.last_website = None
        self.last_action = None
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        self.logger.info("Chotu Autonomous System initialized")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration file"""
        try:
            config_file = Path(self.config_path)
            if config_file.exists():
                with open(config_file, 'r') as f:
                    return json.load(f)
            else:
                # Default configuration
                default_config = {
                    "autonomous_mode": True,
                    "learning_mode": True,
                    "headless_mode": False,
                    "stealth_level": "normal",
                    "vision_confidence": 0.8,
                    "max_task_duration": 300,
                    "auto_confirm_credentials": False,
                    "screenshot_all_steps": True
                }
                
                # Save default config
                config_file.parent.mkdir(parents=True, exist_ok=True)
                with open(config_file, 'w') as f:
                    json.dump(default_config, f, indent=2)
                
                return default_config
        except Exception as e:
            self.logger.error(f"Failed to load config: {e}")
            return {}
    
    async def process_user_input(self, user_input: str, context: Dict[str, Any] = None) -> str:
        """Main entry point for processing user input with autonomous capabilities"""
        try:
            self.logger.info(f"Processing: {user_input}")
            
            # Add command to recent history
            self._add_to_recent_commands(user_input)
            
            # Check if this is a follow-up command
            enhanced_command = self._enhance_with_context(user_input)
            if enhanced_command != user_input:
                self.logger.info(f"Enhanced command with context: {enhanced_command}")
                user_input = enhanced_command
            
            # First, try intelligent context analysis if available
            if self.intelligent_processor:
                # Analyze if this is an autonomous task request
                analysis = await self._analyze_autonomous_intent(user_input, context)
                
                if analysis.get("requires_autonomous_execution", False):
                    result = await self._handle_autonomous_request(user_input, context)
                    self._update_context_from_result(user_input, result)
                    return result
            
            # Check for direct autonomous commands
            if self._is_autonomous_command(user_input):
                result = await self._handle_autonomous_request(user_input, context)
                self._update_context_from_result(user_input, result)
                return result
            
            # Check for system commands
            if self._is_system_command(user_input):
                return self._handle_system_command(user_input)
            
            # Fallback to regular conversation
            return self._handle_regular_conversation(user_input)
            
        except Exception as e:
            error_msg = f"Error processing input: {str(e)}"
            self.logger.error(error_msg)
            return f"❌ {error_msg}"
    
    async def _analyze_autonomous_intent(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze if user input requires autonomous execution"""
        try:
            # Define autonomous intent indicators
            autonomous_keywords = [
                "open", "close", "login", "sign in", "navigate", "go to",
                "click", "type", "enter", "submit", "check", "verify",
                "upload", "download", "send", "post", "share", "buy",
                "order", "book", "reserve", "pay", "transfer"
            ]
            
            # Web automation indicators
            web_indicators = [
                "website", "browser", "chrome", "safari", "firefox",
                "instagram", "facebook", "twitter", "gmail", "youtube",
                "amazon", "google", "linkedin", "github", "slack"
            ]
            
            # System automation indicators
            system_indicators = [
                "finder", "application", "app", "file", "folder",
                "screenshot", "screen", "window", "desktop"
            ]
            
            user_lower = user_input.lower()
            
            # Score autonomous intent
            autonomous_score = sum(1 for keyword in autonomous_keywords if keyword in user_lower)
            web_score = sum(1 for indicator in web_indicators if indicator in user_lower)
            system_score = sum(1 for indicator in system_indicators if indicator in user_lower)
            
            total_score = autonomous_score + web_score + system_score
            
            # Determine if autonomous execution is needed
            requires_autonomous = total_score >= 2 or any(
                phrase in user_lower for phrase in [
                    "open and login", "go to", "check my", "login to"
                ]
            )
            
            return {
                "requires_autonomous_execution": requires_autonomous,
                "autonomous_score": autonomous_score,
                "web_score": web_score,
                "system_score": system_score,
                "total_score": total_score,
                "task_type": "web" if web_score > system_score else "system",
                "confidence": min(total_score / 5.0, 1.0)
            }
            
        except Exception as e:
            self.logger.error(f"Intent analysis failed: {e}")
            return {"requires_autonomous_execution": False}
    
    async def _handle_autonomous_request(self, user_input: str, context: Dict[str, Any] = None) -> str:
        """Handle autonomous task execution requests"""
        try:
            # Create execution context
            execution_context = ExecutionContext(
                user_id=context.get("user_id", "default_user") if context else "default_user",
                session_id=self.session_id,
                environment=self.config.get("environment", "development"),
                browser_profile="stealth",
                stealth_level=self.config.get("stealth_level", "normal")
            )
            
            # Execute the task
            self.logger.info(f"🤖 Executing autonomous task: {user_input}")
            
            result = self.autonomous_executor.execute_user_command(user_input, execution_context)
            
            # Format response based on result
            if result.success:
                response = f"✅ **Task Completed Successfully!**\n\n"
                response += f"**Task:** {user_input}\n"
                response += f"**Duration:** {result.duration:.2f} seconds\n"
                response += f"**Steps Completed:** {result.steps_completed}/{result.total_steps}\n"
                
                if result.screenshots:
                    response += f"**Screenshots:** {len(result.screenshots)} captured\n"
                
                # Add learning information if in learning mode
                if self.autonomous_executor.learning_mode:
                    response += f"\n🧠 **New task learned and can be reused!**"
                
                return response
            else:
                response = f"❌ **Task Failed**\n\n"
                response += f"**Task:** {user_input}\n"
                response += f"**Error:** {result.error_message}\n"
                response += f"**Steps Completed:** {result.steps_completed}/{result.total_steps}\n"
                
                if result.steps_completed > 0:
                    response += f"\n💡 **Partial progress was made. You can try again or provide more specific instructions.**"
                
                return response
                
        except Exception as e:
            error_msg = f"Autonomous execution failed: {str(e)}"
            self.logger.error(error_msg)
            return f"❌ {error_msg}"
    
    def _is_autonomous_command(self, user_input: str) -> bool:
        """Check if input is a direct autonomous command"""
        autonomous_commands = [
            "open chrome", "close chrome", "open instagram", "login to",
            "navigate to", "go to", "click on", "type in", "scroll",
            "check my", "open my", "send email", "post on"
        ]
        
        user_lower = user_input.lower()
        return any(cmd in user_lower for cmd in autonomous_commands)
    
    def _is_system_command(self, user_input: str) -> bool:
        """Check if input is a system command"""
        system_commands = [
            "status", "stats", "statistics", "show tasks", "list tasks",
            "learning mode", "autonomous mode", "help", "capabilities",
            "demonstrate", "config", "settings"
        ]
        
        user_lower = user_input.lower()
        return any(cmd in user_lower for cmd in system_commands)
    
    def _handle_system_command(self, user_input: str) -> str:
        """Handle system commands"""
        user_lower = user_input.lower()
        
        if "status" in user_lower or "stats" in user_lower:
            return self._get_system_status()
        
        elif "show tasks" in user_lower or "list tasks" in user_lower:
            return self._list_available_tasks()
        
        elif "learning mode" in user_lower:
            if "on" in user_lower or "enable" in user_lower:
                self.learning_mode = True
                return "🧠 Learning mode enabled. Chotu will learn new tasks as you demonstrate them."
            elif "off" in user_lower or "disable" in user_lower:
                self.learning_mode = False
                return "🧠 Learning mode disabled."
            else:
                return f"🧠 Learning mode is currently: {'ON' if self.learning_mode else 'OFF'}"
        
        elif "autonomous mode" in user_lower:
            if "on" in user_lower or "enable" in user_lower:
                self.autonomous_mode = True
                return "🤖 Autonomous mode enabled. Chotu can now execute tasks independently."
            elif "off" in user_lower or "disable" in user_lower:
                self.autonomous_mode = False
                return "🤖 Autonomous mode disabled."
            else:
                return f"🤖 Autonomous mode is currently: {'ON' if self.autonomous_mode else 'OFF'}"
        
        elif "capabilities" in user_lower or "demonstrate" in user_lower:
            return self.autonomous_executor.demonstrate_capabilities()
        
        elif "help" in user_lower:
            return self._get_help_text()
        
        else:
            return "❓ Unknown system command. Type 'help' for available commands."
    
    def _handle_regular_conversation(self, user_input: str) -> str:
        """Handle regular conversation when not autonomous"""
        # If intelligent processor is available, use it
        if self.intelligent_processor:
            # This would integrate with the existing intelligent conversation
            return "🤖 I understand. Would you like me to help you with that task autonomously?"
        else:
            return f"I heard: {user_input}. I can help you execute tasks autonomously. Try commands like 'open Instagram' or 'check my email'."
    
    def _get_system_status(self) -> str:
        """Get comprehensive system status"""
        try:
            status = self.autonomous_executor.get_execution_status()
            
            response = "🔍 **Chotu Autonomous System Status**\n\n"
            response += f"**Session ID:** {self.session_id}\n"
            response += f"**Autonomous Mode:** {'🟢 Active' if self.autonomous_mode else '🔴 Standby'}\n"
            response += f"**Learning Mode:** {'🟢 Active' if self.learning_mode else '🔴 Standby'}\n"
            response += f"**Available Tasks:** {status.get('available_tasks', 0)}\n"
            response += f"**Stored Credentials:** {status.get('vault_credentials', 0)}\n"
            
            # Execution statistics
            exec_stats = status.get('execution_statistics', {})
            if exec_stats:
                response += f"\n**📊 Execution Statistics:**\n"
                response += f"• Total Executions: {exec_stats.get('total_executions', 0)}\n"
                response += f"• Success Rate: {exec_stats.get('overall_success_rate', 0):.1%}\n"
                response += f"• Average Duration: {exec_stats.get('overall_average_duration', 0):.1f}s\n"
            
            # System health
            response += f"\n**System Health:** 🟢 All systems operational"
            
            return response
            
        except Exception as e:
            return f"❌ Failed to get system status: {str(e)}"
    
    def _list_available_tasks(self) -> str:
        """List all available learned tasks"""
        try:
            tasks = self.autonomous_executor.memory.get_all_tasks()
            
            if not tasks:
                return "📝 No tasks learned yet. Start by asking me to do something and I'll learn it!"
            
            response = f"📝 **Available Tasks ({len(tasks)}):**\n\n"
            
            for i, task in enumerate(tasks, 1):
                response += f"**{i}. {task.task_name}**\n"
                response += f"   • Trigger phrases: {', '.join(task.trigger_phrases)}\n"
                response += f"   • Steps: {len(task.action_sequence)}\n"
                response += f"   • Success rate: {task.success_rate:.1%}\n"
                response += f"   • Executed: {task.execution_count} times\n\n"
            
            return response
            
        except Exception as e:
            return f"❌ Failed to list tasks: {str(e)}"
    
    def _get_help_text(self) -> str:
        """Get help text for autonomous features"""
        help_text = """
🤖 **Chotu Autonomous System Help**

**Basic Commands:**
• `open [app/website]` - Open applications or websites
• `login to [service]` - Login to websites with stored credentials  
• `navigate to [url]` - Go to specific URLs
• `check my [account/email]` - Access your accounts
• `send [message/email]` - Send communications
• `post on [platform]` - Share content on social media

**System Commands:**
• `status` - Show system status and statistics
• `list tasks` - Show all learned tasks
• `learning mode on/off` - Toggle learning mode
• `autonomous mode on/off` - Toggle autonomous execution
• `capabilities` - Demonstrate system capabilities

**Examples:**
• "Open Instagram and login with my credentials"
• "Check my Gmail inbox"
• "Navigate to github.com"
• "Post 'Hello world' on Twitter"
• "Open Chrome browser"

**Features:**
✅ Computer Vision & Element Detection
✅ Stealth Browser Automation
✅ Secure Credential Storage
✅ Task Learning & Memory
✅ Human-like Behavior Simulation

Type any task and I'll either execute it or learn how to do it!
"""
        return help_text
    
    def store_credential(self, service: str, username: str, password: str, 
                        context: List[str] = None) -> str:
        """Store encrypted credentials"""
        try:
            if context is None:
                context = ["web_automation", "task_execution"]
            
            success = self.autonomous_executor.vault.store_credential(
                service, username, password, context
            )
            
            if success:
                return f"✅ Credentials stored securely for {service}:{username}"
            else:
                return f"❌ Failed to store credentials for {service}:{username}"
                
        except Exception as e:
            return f"❌ Credential storage failed: {str(e)}"
    
    def get_learned_tasks_summary(self) -> Dict[str, Any]:
        """Get summary of learned tasks for API/integration use"""
        try:
            tasks = self.autonomous_executor.memory.get_all_tasks()
            status = self.autonomous_executor.get_execution_status()
            
            return {
                "total_tasks": len(tasks),
                "tasks": [
                    {
                        "name": task.task_name,
                        "triggers": task.trigger_phrases,
                        "steps": len(task.action_sequence),
                        "success_rate": task.success_rate,
                        "executions": task.execution_count
                    }
                    for task in tasks
                ],
                "system_status": status,
                "capabilities": [
                    "Computer Vision",
                    "Stealth Automation", 
                    "Credential Management",
                    "Task Learning",
                    "Human Behavior Simulation"
                ]
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get tasks summary: {e}")
            return {"error": str(e)}
    
    def _add_to_recent_commands(self, command: str):
        """Add command to recent history for context"""
        self.recent_commands.append({
            'command': command,
            'timestamp': time.time()
        })
        
        # Keep only last 5 commands
        if len(self.recent_commands) > 5:
            self.recent_commands = self.recent_commands[-5:]
    
    def _enhance_with_context(self, user_input: str) -> str:
        """Enhance command with context from recent actions"""
        try:
            # Check for follow-up patterns
            follow_up_patterns = [
                "in the search box",
                "search for",
                "type",
                "write",
                "enter",
                "click on",
                "in search",
                "search box",
                "right"  # as in "right Alka Yagnik songs"
            ]
            
            # If it's a follow-up command
            is_follow_up = any(pattern in user_input.lower() for pattern in follow_up_patterns)
            
            if is_follow_up and self.last_website:
                # Common follow-up scenarios
                if any(phrase in user_input.lower() for phrase in ["search box", "search for", "type", "write", "right"]):
                    if self.last_website == "youtube":
                        # Extract what to search for
                        search_term = self._extract_search_term(user_input)
                        if search_term:
                            return f"search for {search_term} on YouTube"
                    elif self.last_website == "google":
                        search_term = self._extract_search_term(user_input)
                        if search_term:
                            return f"search for {search_term} on Google"
                    elif self.last_website == "amazon":
                        search_term = self._extract_search_term(user_input)
                        if search_term:
                            return f"search for {search_term} on Amazon"
            
            return user_input
            
        except Exception as e:
            self.logger.error(f"Context enhancement failed: {e}")
            return user_input
    
    def _extract_search_term(self, command: str) -> str:
        """Extract search term from follow-up command"""
        import re
        
        # Patterns to extract search terms
        patterns = [
            r"search for\s+(.+?)(?:\s+on\s+|$)",
            r"search\s+(.+?)(?:\s+on\s+|$)",
            r"type\s+(.+?)(?:\s+in\s+|$)",
            r"write\s+(.+?)(?:\s+in\s+|$)",
            r"right\s+(.+?)(?:\s+in\s+|\s+on\s+|$)",  # "right Alka Yagnik songs"
            r"(?:search box|searchbox).*?(?:write|type|enter|right)\s+(.+?)$",
            r"in.*?search.*?(?:write|type|enter|right)\s+(.+?)$",
            r"(?:YouTube|youtube).*?(?:search|searchbox).*?(?:write|type|right)\s+(.+?)$"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, command.lower())
            if match:
                return match.group(1).strip()
        
        # If no pattern matches but it's clearly a search term, extract everything after certain keywords
        if any(word in command.lower() for word in ["right", "type", "write", "search for"]):
            # Split on these keywords and take the last part
            for keyword in ["right ", "type ", "write ", "search for "]:
                if keyword in command.lower():
                    parts = command.lower().split(keyword)
                    if len(parts) > 1:
                        return parts[-1].strip()
        
        return ""
    
    def _update_context_from_result(self, command: str, result: str):
        """Update context based on command execution result"""
        try:
            # Extract website from successful navigation
            if "youtube" in command.lower() and "successful" in result.lower():
                self.last_website = "youtube"
                self.last_action = "navigation"
            elif "google" in command.lower() and "successful" in result.lower():
                self.last_website = "google"
                self.last_action = "navigation"
            elif "amazon" in command.lower() and "successful" in result.lower():
                self.last_website = "amazon"
                self.last_action = "navigation"
            elif "instagram" in command.lower() and "successful" in result.lower():
                self.last_website = "instagram"
                self.last_action = "navigation"
            
            # Update current context
            self.current_context = {
                'last_command': command,
                'last_result': result,
                'timestamp': time.time()
            }
            
        except Exception as e:
            self.logger.error(f"Context update failed: {e}")
    
    def shutdown(self):
        """Safely shutdown the autonomous system"""
        try:
            self.autonomous_executor.shutdown()
            self.logger.info("Chotu Autonomous System shutdown complete")
        except Exception as e:
            self.logger.error(f"Shutdown error: {e}")

# Global instance for easy access
chotu_autonomous = None

def get_chotu_autonomous() -> ChouAutonomous:
    """Get global Chotu Autonomous instance"""
    global chotu_autonomous
    if chotu_autonomous is None:
        chotu_autonomous = ChouAutonomous()
    return chotu_autonomous

# Convenience functions for integration
async def execute_autonomous_task(user_input: str, context: Dict[str, Any] = None) -> str:
    """Execute autonomous task - convenience function"""
    chotu = get_chotu_autonomous()
    return await chotu.process_user_input(user_input, context)

def get_system_capabilities() -> str:
    """Get system capabilities - convenience function"""
    chotu = get_chotu_autonomous()
    return chotu.autonomous_executor.demonstrate_capabilities()

def get_task_statistics() -> Dict[str, Any]:
    """Get execution statistics - convenience function"""
    chotu = get_chotu_autonomous()
    return chotu.get_learned_tasks_summary()

if __name__ == "__main__":
    # Demo mode
    async def demo():
        chotu = ChouAutonomous()
        
        print("🤖 Chotu Autonomous System Demo")
        print("="*50)
        
        # Show capabilities
        print(await chotu.process_user_input("capabilities"))
        print("\n" + "="*50)
        
        # Demo commands
        demo_commands = [
            "status",
            "list tasks", 
            "open chrome",
            "help"
        ]
        
        for cmd in demo_commands:
            print(f"\n> {cmd}")
            result = await chotu.process_user_input(cmd)
            print(result)
            print("-"*30)
    
    asyncio.run(demo())
