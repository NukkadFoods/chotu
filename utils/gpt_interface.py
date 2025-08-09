# utils/gpt_interface.py
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Model configurations for different use cases
MODEL_CONFIG = {
    # For coding tasks - use cost-effective GPT-3.5-turbo
    "coding": {
        "model": "gpt-3.5-turbo",
        "max_tokens": 2000,
        "temperature": 0.3,
        "description": "Cost-effective coding with GPT-3.5-turbo - good code quality, lower cost"
    },
    
    # For learning and autonomous capability generation - use cost-effective GPT-3.5-turbo
    "learning": {
        "model": "gpt-3.5-turbo", 
        "max_tokens": 1500,
        "temperature": 0.4,
        "description": "Learning new capabilities with cost-effective GPT-3.5-turbo"
    },
    
    # For context understanding and command clarification - use GPT-3.5-turbo
    "context": {
        "model": "gpt-3.5-turbo",
        "max_tokens": 500,
        "temperature": 0.6,
        "description": "Command clarification, intent understanding, context analysis"
    },
    
    # For simple thinking and basic responses - use GPT-3.5-turbo
    "thinking": {
        "model": "gpt-3.5-turbo",
        "max_tokens": 300,
        "temperature": 0.7,
        "description": "Basic reasoning and responses with cost-effective GPT-3.5-turbo"
    },
    
    # For system commands and quick decisions - use GPT-3.5-turbo
    "system": {
        "model": "gpt-3.5-turbo",
        "max_tokens": 150,
        "temperature": 0.2,
        "description": "System commands, quick decisions, factual responses"
    }
}

# Initialize OpenAI client
try:
    api_key = os.getenv('apiKey')
    if not api_key:
        raise ValueError("OpenAI API key not found in .env file")
    
    # Initialize client with just the API key
    client = OpenAI(api_key=api_key)
    print("✅ OpenAI client initialized successfully")
    print("🤖 Available models:")
    for task, config in MODEL_CONFIG.items():
        print(f"   • {task}: {config['model']} - {config['description']}")
except Exception as e:
    print(f"❌ Failed to load OpenAI API key: {e}")
    client = None

def call_gpt(prompt: str, task_type: str = "thinking") -> str:
    """
    Call GPT with specialized models for different tasks
    
    Args:
        prompt: The prompt to send to GPT
        task_type: Type of task - 'coding', 'learning', 'context', 'thinking', 'system'
    
    Returns:
        GPT response string
    """
    if not client:
        return "ERROR: OpenAI client not initialized"
    
    # Get model configuration for the task type
    config = MODEL_CONFIG.get(task_type, MODEL_CONFIG["thinking"])
    
    try:
        print(f"🧠 Using {config['model']} for {task_type} task")
        response = client.chat.completions.create(
            model=config["model"],
            messages=[{"role": "user", "content": prompt}],
            max_tokens=config["max_tokens"],
            temperature=config["temperature"]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"ERROR: {str(e)}"

# Specialized functions for different use cases
def call_gpt_coding(prompt: str) -> str:
    """Use GPT-3.5-turbo for coding tasks - cost-effective with good quality"""
    return call_gpt(prompt, "coding")

def call_gpt_learning(prompt: str) -> str:
    """Use GPT-3.5-turbo for learning tasks - cost-effective for autonomous capability generation"""
    return call_gpt(prompt, "learning")

def call_gpt_context(prompt: str) -> str:
    """Use GPT-3.5-turbo for context understanding - balanced performance and cost"""
    return call_gpt(prompt, "context")

def call_gpt_thinking(prompt: str) -> str:
    """Use GPT-3.5-turbo for basic thinking - most cost effective"""
    return call_gpt(prompt, "thinking")

def call_gpt_system(prompt: str) -> str:
    """Use GPT-3.5-turbo for system commands - ultra fast and cost effective"""
    return call_gpt(prompt, "system")
