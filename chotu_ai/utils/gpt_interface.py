# utils/gpt_interface.py
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
try:
    api_key = os.getenv('apiKey')
    if not api_key:
        raise ValueError("OpenAI API key not found in .env file")
    client = OpenAI(api_key=api_key)
    print("✅ OpenAI client initialized successfully")
except Exception as e:
    print(f"❌ Failed to load OpenAI API key: {e}")
    client = None

def call_gpt(prompt: str) -> str:
    if not client:
        return "ERROR: OpenAI client not initialized"
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"ERROR: {str(e)}"
