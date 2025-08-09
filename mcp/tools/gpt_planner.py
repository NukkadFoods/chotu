# mcp/tools/gpt_planner.py
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from utils.gpt_interface import call_gpt_system, call_gpt_context, call_gpt_learning, call_gpt_coding
import subprocess

def generate_and_run(intent: str) -> str:
    """Generate and execute system commands using specialized GPT model"""
    prompt = f"""
    Generate a macOS terminal or AppleScript command to achieve:
    '{intent}'
    Only return the command, nothing else.
    Example: open -a Safari
    """
    cmd = call_gpt_system(prompt)  # Use system model for quick command generation
    if "ERROR" not in cmd:
        try:
            subprocess.run(cmd.split(), capture_output=True)
            return f"Executed via GPT: {cmd}"
        except:
            return f"GPT suggested: {cmd}, but failed to run."
    return "Could not determine action."

# Export specialized GPT functions for use by other modules
def call_gpt(prompt: str) -> str:
    """Default GPT call - uses thinking model"""
    from utils.gpt_interface import call_gpt_thinking
    return call_gpt_thinking(prompt)

def call_gpt_context(prompt: str) -> str:
    """Context understanding GPT call"""
    from utils.gpt_interface import call_gpt_context as gpt_context
    return gpt_context(prompt)

def call_gpt_learning(prompt: str) -> str:
    """Learning and capability generation GPT call"""
    from utils.gpt_interface import call_gpt_learning as gpt_learning
    return gpt_learning(prompt)

def call_gpt_coding(prompt: str) -> str:
    """Coding and development GPT call"""
    from utils.gpt_interface import call_gpt_coding as gpt_coding
    return gpt_coding(prompt)
