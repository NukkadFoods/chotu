"""
Chotu Procedural Memory - Learning and Storing Task Workflows
Implements task recording, storage, and retrieval with visual element signatures
"""
import json
import time
import hashlib
from typing import List, Dict, Tuple, Optional, Any, Union
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime
import logging

@dataclass
class ActionStep:
    """Individual step in a task workflow"""
    step_id: str
    action_type: str  # navigate, click, type, scroll, wait, verify
    target: str  # element name or URL
    value: Optional[str] = None  # text to type, scroll amount, etc.
    confirmation: Optional[str] = None  # verification method
    timeout: Optional[int] = 10
    retry_count: int = 3
    human_readable: str = ""
    
@dataclass
class TaskRecipe:
    """Complete task workflow with context and metadata"""
    task_name: str
    trigger_phrases: List[str]
    description: str
    prerequisites: List[str]
    action_sequence: List[ActionStep]
    credentials: Dict[str, str]  # References to credential vault
    success_indicators: List[str]
    failure_handlers: List[Dict[str, str]]
    created_at: str
    updated_at: str
    success_rate: float = 1.0
    execution_count: int = 0
    average_duration: float = 0.0
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []

@dataclass
class ExecutionContext:
    """Context for task execution"""
    user_id: str
    session_id: str
    environment: str  # development, staging, production
    browser_profile: str
    stealth_level: str  # conservative, normal, aggressive
    
class ProceduralMemory:
    """Memory system for storing and managing task workflows"""
    
    def __init__(self, memory_dir: str = "autonomous/memory"):
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        self.recipes_file = self.memory_dir / "task_recipes.json"
        self.execution_log_file = self.memory_dir / "execution_log.json"
        self.element_registry_file = self.memory_dir / "element_registry.json"
        
        # Initialize logger first
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # In-memory storage
        self.task_recipes: Dict[str, TaskRecipe] = {}
        self.execution_log: List[Dict] = []
        self.element_registry: Dict[str, Dict] = {}
        
        # Load existing data
        self.load_memory()
    
    def record_task_learning(self, task_name: str, trigger_phrases: List[str], 
                           description: str = "") -> str:
        """Start recording a new task workflow"""
        try:
            task_id = self._generate_task_id(task_name)
            
            # Create new recipe
            recipe = TaskRecipe(
                task_name=task_name,
                trigger_phrases=trigger_phrases,
                description=description,
                prerequisites=[],
                action_sequence=[],
                credentials={},
                success_indicators=[],
                failure_handlers=[],
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat()
            )
            
            self.task_recipes[task_id] = recipe
            self.logger.info(f"Started recording task: {task_name} (ID: {task_id})")
            
            return task_id
            
        except Exception as e:
            self.logger.error(f"Failed to start task recording: {e}")
            return ""
    
    def add_action_step(self, task_id: str, action_type: str, target: str, 
                       value: Optional[str] = None, confirmation: Optional[str] = None,
                       human_readable: str = "") -> bool:
        """Add an action step to a task recipe"""
        try:
            if task_id not in self.task_recipes:
                self.logger.error(f"Task ID not found: {task_id}")
                return False
            
            step_id = f"step_{len(self.task_recipes[task_id].action_sequence) + 1}"
            
            action_step = ActionStep(
                step_id=step_id,
                action_type=action_type,
                target=target,
                value=value,
                confirmation=confirmation,
                human_readable=human_readable or f"{action_type} on {target}"
            )
            
            self.task_recipes[task_id].action_sequence.append(action_step)
            self.task_recipes[task_id].updated_at = datetime.now().isoformat()
            
            self.logger.info(f"Added step to task {task_id}: {human_readable}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add action step: {e}")
            return False
    
    def finalize_task_recipe(self, task_id: str, prerequisites: List[str] = None,
                           success_indicators: List[str] = None,
                           failure_handlers: List[Dict] = None) -> bool:
        """Finalize and save a task recipe"""
        try:
            if task_id not in self.task_recipes:
                return False
            
            recipe = self.task_recipes[task_id]
            
            if prerequisites:
                recipe.prerequisites = prerequisites
            if success_indicators:
                recipe.success_indicators = success_indicators
            if failure_handlers:
                recipe.failure_handlers = failure_handlers
            
            recipe.updated_at = datetime.now().isoformat()
            
            self.save_memory()
            self.logger.info(f"Finalized task recipe: {recipe.task_name}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to finalize task recipe: {e}")
            return False
    
    def find_task_by_trigger(self, user_input: str) -> Optional[TaskRecipe]:
        """Find task recipe based on user input with improved matching"""
        user_input_lower = user_input.lower()
        
        # Store all matches with their scores for ranking
        matches = []
        
        # Direct matches first (highest priority)
        for task_id, recipe in self.task_recipes.items():
            for trigger in recipe.trigger_phrases:
                if trigger.lower() == user_input_lower:
                    matches.append((recipe, 100, len(trigger)))  # Perfect match
        
        # Exact substring matches (prioritize longer triggers)
        for task_id, recipe in self.task_recipes.items():
            for trigger in recipe.trigger_phrases:
                trigger_lower = trigger.lower()
                if trigger_lower in user_input_lower:
                    # Bonus points for longer triggers and exact phrase matches
                    score = 80 + len(trigger_lower)
                    if user_input_lower.startswith(trigger_lower):
                        score += 10  # Bonus for starting with trigger
                    matches.append((recipe, score, len(trigger_lower)))
                elif user_input_lower in trigger_lower:
                    score = 70 + len(user_input_lower)
                    matches.append((recipe, score, len(trigger_lower)))
        
        # Keyword matching (lower priority)
        for task_id, recipe in self.task_recipes.items():
            for trigger in recipe.trigger_phrases:
                trigger_words = set(trigger.lower().split())
                input_words = set(user_input_lower.split())
                
                # Calculate overlap percentage
                overlap = len(trigger_words.intersection(input_words))
                overlap_pct = overlap / len(trigger_words) if trigger_words else 0
                
                if overlap_pct >= 0.7:  # 70% word overlap
                    score = 50 + (overlap_pct * 20) + len(trigger.lower())
                    matches.append((recipe, score, len(trigger.lower())))
        
        # Sort by score (highest first), then by trigger length (longest first)
        matches.sort(key=lambda x: (x[1], x[2]), reverse=True)
        
        # Return the best match
        if matches:
            return matches[0][0]
        
        return None
    
    def get_task_by_name(self, task_name: str) -> Optional[TaskRecipe]:
        """Get task recipe by name"""
        for task_id, recipe in self.task_recipes.items():
            if recipe.task_name.lower() == task_name.lower():
                return recipe
        return None
    
    def get_all_tasks(self) -> List[TaskRecipe]:
        """Get all task recipes"""
        return list(self.task_recipes.values())
    
    def update_task_statistics(self, task_id: str, success: bool, duration: float):
        """Update task execution statistics"""
        try:
            if task_id not in self.task_recipes:
                return
            
            recipe = self.task_recipes[task_id]
            recipe.execution_count += 1
            
            # Update success rate
            if success:
                current_successes = recipe.success_rate * (recipe.execution_count - 1)
                recipe.success_rate = (current_successes + 1) / recipe.execution_count
            else:
                current_successes = recipe.success_rate * (recipe.execution_count - 1)
                recipe.success_rate = current_successes / recipe.execution_count
            
            # Update average duration
            current_total_time = recipe.average_duration * (recipe.execution_count - 1)
            recipe.average_duration = (current_total_time + duration) / recipe.execution_count
            
            recipe.updated_at = datetime.now().isoformat()
            
        except Exception as e:
            self.logger.error(f"Failed to update task statistics: {e}")
    
    def log_execution(self, task_id: str, context: ExecutionContext, 
                     success: bool, error_message: str = "", 
                     duration: float = 0.0, screenshots: List[str] = None):
        """Log task execution for audit trail"""
        try:
            execution_record = {
                "timestamp": datetime.now().isoformat(),
                "task_id": task_id,
                "task_name": self.task_recipes.get(task_id, {}).task_name if task_id in self.task_recipes else "Unknown",
                "context": asdict(context),
                "success": success,
                "error_message": error_message,
                "duration": duration,
                "screenshots": screenshots or []
            }
            
            self.execution_log.append(execution_record)
            
            # Keep only last 1000 execution records
            if len(self.execution_log) > 1000:
                self.execution_log = self.execution_log[-1000:]
            
            # Update task statistics
            if task_id in self.task_recipes:
                self.update_task_statistics(task_id, success, duration)
            
            self.save_memory()
            
        except Exception as e:
            self.logger.error(f"Failed to log execution: {e}")
    
    def register_element(self, element_name: str, website: str, 
                        element_data: Dict[str, Any]):
        """Register visual element signature for reuse"""
        try:
            key = f"{website}:{element_name}"
            
            self.element_registry[key] = {
                "element_name": element_name,
                "website": website,
                "data": element_data,
                "created_at": datetime.now().isoformat(),
                "usage_count": self.element_registry.get(key, {}).get("usage_count", 0)
            }
            
            self.save_memory()
            
        except Exception as e:
            self.logger.error(f"Failed to register element: {e}")
    
    def get_element_data(self, element_name: str, website: str) -> Optional[Dict]:
        """Get registered element data"""
        key = f"{website}:{element_name}"
        
        if key in self.element_registry:
            # Increment usage count
            self.element_registry[key]["usage_count"] += 1
            return self.element_registry[key]["data"]
        
        return None
    
    def create_task_from_template(self, template_name: str, 
                                custom_values: Dict[str, str] = None) -> Optional[str]:
        """Create task from predefined template"""
        templates = {
            "web_login": {
                "task_name": "Generic Web Login",
                "trigger_phrases": ["login to website", "sign in"],
                "description": "Generic web login workflow",
                "action_sequence": [
                    {"action_type": "navigate", "target": "{website_url}"},
                    {"action_type": "click", "target": "login_button"},
                    {"action_type": "type", "target": "username_field", "value": "{username}"},
                    {"action_type": "type", "target": "password_field", "value": "{password}"},
                    {"action_type": "click", "target": "submit_button"},
                    {"action_type": "verify", "target": "dashboard_element"}
                ],
                "success_indicators": ["dashboard_element", "profile_menu"]
            },
            "social_media_post": {
                "task_name": "Social Media Post",
                "trigger_phrases": ["post on social media", "share post"],
                "description": "Post content on social media",
                "action_sequence": [
                    {"action_type": "navigate", "target": "{social_platform_url}"},
                    {"action_type": "click", "target": "new_post_button"},
                    {"action_type": "type", "target": "post_content_field", "value": "{post_text}"},
                    {"action_type": "click", "target": "publish_button"},
                    {"action_type": "verify", "target": "post_confirmation"}
                ]
            }
        }
        
        if template_name not in templates:
            return None
        
        try:
            template = templates[template_name]
            task_id = self.record_task_learning(
                template["task_name"],
                template["trigger_phrases"],
                template["description"]
            )
            
            # Add action steps
            for step_data in template["action_sequence"]:
                # Replace template variables
                target = step_data["target"]
                value = step_data.get("value", "")
                
                if custom_values:
                    for key, custom_value in custom_values.items():
                        target = target.replace(f"{{{key}}}", custom_value)
                        value = value.replace(f"{{{key}}}", custom_value)
                
                self.add_action_step(
                    task_id,
                    step_data["action_type"],
                    target,
                    value if value else None
                )
            
            # Finalize with template settings
            self.finalize_task_recipe(
                task_id,
                success_indicators=template.get("success_indicators", [])
            )
            
            return task_id
            
        except Exception as e:
            self.logger.error(f"Failed to create task from template: {e}")
            return None
    
    def export_task_recipe(self, task_id: str) -> Optional[Dict]:
        """Export task recipe for sharing or backup"""
        if task_id in self.task_recipes:
            return asdict(self.task_recipes[task_id])
        return None
    
    def import_task_recipe(self, recipe_data: Dict) -> Optional[str]:
        """Import task recipe from external source"""
        try:
            recipe = TaskRecipe(**recipe_data)
            task_id = self._generate_task_id(recipe.task_name)
            
            self.task_recipes[task_id] = recipe
            self.save_memory()
            
            return task_id
            
        except Exception as e:
            self.logger.error(f"Failed to import task recipe: {e}")
            return None
    
    def _generate_task_id(self, task_name: str) -> str:
        """Generate unique task ID"""
        timestamp = str(int(time.time()))
        name_hash = hashlib.md5(task_name.encode()).hexdigest()[:8]
        return f"task_{timestamp}_{name_hash}"
    
    def save_memory(self):
        """Save all memory data to disk"""
        try:
            # Save task recipes
            recipes_data = {}
            for task_id, recipe in self.task_recipes.items():
                recipes_data[task_id] = asdict(recipe)
            
            with open(self.recipes_file, 'w') as f:
                json.dump(recipes_data, f, indent=2)
            
            # Save execution log
            with open(self.execution_log_file, 'w') as f:
                json.dump(self.execution_log, f, indent=2)
            
            # Save element registry
            with open(self.element_registry_file, 'w') as f:
                json.dump(self.element_registry, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Failed to save memory: {e}")
    
    def load_memory(self):
        """Load memory data from disk"""
        try:
            # Load task recipes
            if self.recipes_file.exists():
                with open(self.recipes_file, 'r') as f:
                    recipes_data = json.load(f)
                
                for task_id, recipe_data in recipes_data.items():
                    # Convert action_sequence back to ActionStep objects
                    action_sequence = []
                    for i, step_data in enumerate(recipe_data["action_sequence"]):
                        # Generate step_id if not present
                        if "step_id" not in step_data:
                            step_data["step_id"] = f"{task_id}_step_{i+1}"
                        
                        action_sequence.append(ActionStep(**step_data))
                    
                    recipe_data["action_sequence"] = action_sequence
                    self.task_recipes[task_id] = TaskRecipe(**recipe_data)
            
            # Load execution log
            if self.execution_log_file.exists():
                with open(self.execution_log_file, 'r') as f:
                    self.execution_log = json.load(f)
            
            # Load element registry
            if self.element_registry_file.exists():
                with open(self.element_registry_file, 'r') as f:
                    self.element_registry = json.load(f)
                    
        except Exception as e:
            self.logger.error(f"Failed to load memory: {e}")
    
    def get_execution_statistics(self) -> Dict[str, Any]:
        """Get overall execution statistics"""
        try:
            total_executions = len(self.execution_log)
            successful_executions = sum(1 for log in self.execution_log if log["success"])
            
            if total_executions == 0:
                return {"total": 0, "success_rate": 0, "average_duration": 0}
            
            success_rate = successful_executions / total_executions
            average_duration = sum(log["duration"] for log in self.execution_log) / total_executions
            
            # Task-specific statistics
            task_stats = {}
            for task_id, recipe in self.task_recipes.items():
                task_stats[recipe.task_name] = {
                    "execution_count": recipe.execution_count,
                    "success_rate": recipe.success_rate,
                    "average_duration": recipe.average_duration
                }
            
            return {
                "total_executions": total_executions,
                "overall_success_rate": success_rate,
                "overall_average_duration": average_duration,
                "task_statistics": task_stats
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get execution statistics: {e}")
            return {}
    
    def cleanup_old_data(self, days_to_keep: int = 30):
        """Clean up old execution logs and unused elements"""
        try:
            from datetime import datetime, timedelta
            
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            
            # Clean execution log
            self.execution_log = [
                log for log in self.execution_log
                if datetime.fromisoformat(log["timestamp"]) > cutoff_date
            ]
            
            # Clean unused elements (keep only if used in last 30 days)
            active_elements = {}
            for key, element_data in self.element_registry.items():
                created_date = datetime.fromisoformat(element_data["created_at"])
                if created_date > cutoff_date or element_data["usage_count"] > 0:
                    active_elements[key] = element_data
            
            self.element_registry = active_elements
            
            self.save_memory()
            self.logger.info(f"Cleaned up data older than {days_to_keep} days")
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup old data: {e}")
