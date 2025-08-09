# memory/memory_manager.py
import json

def load_ram():
    try:
        with open("memory/ram.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_ram(data):
    with open("memory/ram.json", "w") as f:
        json.dump(data, f, indent=2)

def load_rom():
    try:
        with open("memory/rom.json", "r") as f:
            return json.load(f)
    except:
        return []

def save_rom(data):
    with open("memory/rom.json", "w") as f:
        json.dump(data, f, indent=2)
