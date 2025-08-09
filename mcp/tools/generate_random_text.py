# mcp/tools/generate_random_text.py
import subprocess
import os
from datetime import datetime

def generate_random_text(length=10, language='en'):
    """
    random text generation
    
    Args:
        length: Length of the random text (default 10)
        language: Language of the random text (default 'en')
    
    Returns:
        str: Success/error message with ✅/❌ prefix
    """
    try:
        # Check if imagesnap exists
        subprocess.run(['which', 'imagesnap'], capture_output=True, check=True)
        
        # Generate random text using built-in Python libraries
        text = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        
        return f"✅ Success: Random text generated - {text}"
    except subprocess.CalledProcessError as e:
        return f"❌ Error: imagesnap tool not found"
    except Exception as e:
        return f"❌ Error: {str(e)}"