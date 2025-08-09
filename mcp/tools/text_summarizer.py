# mcp/tools/text_summarizer.py
import subprocess
import os

def text_summarizer(text):
    """
    Summarizes the given text using transformers pipeline
    
    Args:
        text: The text to be summarized
    
    Returns:
        str: Success/error message
    """
    try:
        summarizer = pipeline('summarization')
        result = summarizer(text, max_length=50, min_length=10, do_sample=False)
        return f"✅ Success: {result[0]['summary_text']}"
    except Exception as e:
        return f"❌ Error: {e}"

# Add any helper functions if needed