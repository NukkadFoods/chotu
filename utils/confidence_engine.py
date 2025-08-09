# utils/confidence_engine.py
import difflib
from memory.memory_manager import load_rom

def calculate_confidence(user_input: str) -> int:
    rom = load_rom()
    patterns = []
    for entry in rom:
        if "input_pattern" in entry:
            patterns.append(entry["input_pattern"].lower())
    
    if not patterns:
        return 30  # No past data → low confidence
    
    matches = difflib.get_close_matches(user_input.lower(), patterns, n=1, cutoff=0.4)
    
    if matches:
        similarity = difflib.SequenceMatcher(None, user_input.lower(), matches[0]).ratio()
        return int(similarity * 100)
    return 30
