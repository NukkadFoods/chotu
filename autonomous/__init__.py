"""
Chotu Autonomous System - Computer Vision & Task Automation
Implements the complete autonomous task execution pipeline
"""

from .vision_engine import VisionEngine, ElementSignature, ScreenRegion
from .action_engine import ActionEngine, HumanBehavior, StealthSettings  
from .procedural_memory import ProceduralMemory, TaskRecipe, ActionStep, ExecutionContext
from .credential_vault import CredentialVault, CredentialEntry, AccessRule
from .task_executor import AutonomousTaskExecutor, TaskExecutionResult

__all__ = [
    'VisionEngine',
    'ElementSignature', 
    'ScreenRegion',
    'ActionEngine',
    'HumanBehavior',
    'StealthSettings',
    'ProceduralMemory',
    'TaskRecipe',
    'ActionStep',
    'ExecutionContext',
    'CredentialVault',
    'CredentialEntry',
    'AccessRule',
    'AutonomousTaskExecutor',
    'TaskExecutionResult'
]

# Version info
__version__ = "1.0.0"
__author__ = "Chotu AI Assistant"
__description__ = "Autonomous task execution with computer vision and procedural learning"
