# memory/context_manager.py
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any

class ContextManager:
    """Advanced context management for Chotu's conversations and learning"""
    
    def __init__(self):
        self.context_file = "memory/context.json"
        self.session_context = []
        self.user_preferences = {}
        self.load_context()
    
    def load_context(self):
        """Load existing context and preferences"""
        try:
            if os.path.exists(self.context_file):
                with open(self.context_file, 'r') as f:
                    data = json.load(f)
                    self.user_preferences = data.get('preferences', {})
                    # Load recent context (last 24 hours)
                    recent_context = []
                    cutoff = datetime.now() - timedelta(hours=24)
                    for item in data.get('session_history', []):
                        item_time = datetime.fromisoformat(item['timestamp'])
                        if item_time > cutoff:
                            recent_context.append(item)
                    self.session_context = recent_context
        except Exception as e:
            print(f"⚠️  Context load error: {e}")
    
    def save_context(self):
        """Save current context to file"""
        try:
            data = {
                'preferences': self.user_preferences,
                'session_history': self.session_context,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.context_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"⚠️  Context save error: {e}")
    
    def add_interaction(self, user_input: str, chotu_response: str, success: bool = True):
        """Add new interaction to context"""
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'user_input': user_input,
            'chotu_response': chotu_response,
            'success': success,
            'session_id': len(self.session_context)
        }
        self.session_context.append(interaction)
        
        # Keep more interactions in memory for better context (increased from 50 to 100)
        if len(self.session_context) > 100:
            self.session_context = self.session_context[-100:]
        
        self.save_context()
    
    def get_relevant_context(self, current_input: str) -> str:
        """Get relevant context for current input"""
        context_summary = []
        
        # Add user preferences
        if self.user_preferences:
            context_summary.append(f"User preferences: {self.user_preferences}")
        
        # Get last 9 interactions for conversation flow (increased from 5)
        recent_conversation = self.session_context[-9:] if self.session_context else []
        
        if recent_conversation:
            context_summary.append("Recent conversation (last 9 interactions):")
            for i, interaction in enumerate(recent_conversation, 1):
                timestamp = interaction['timestamp'].split('T')[1][:8] if 'T' in interaction['timestamp'] else 'recent'
                context_summary.append(f"{i}. [{timestamp}] User: '{interaction['user_input']}' → Chotu: '{interaction['chotu_response'][:60]}...'")
        
        # Extract subjects from recent conversation for ambiguous commands
        if any(word in current_input.lower() for word in ['it', 'that', 'this', 'increase', 'decrease', 'set', 'make']):
            subjects = []
            for interaction in recent_conversation:
                user_input = interaction['user_input'].lower()
                if 'brightness' in user_input:
                    subjects.append('brightness')
                elif 'volume' in user_input:
                    subjects.append('volume')
                elif 'bluetooth' in user_input:
                    subjects.append('bluetooth')
                elif any(app in user_input for app in ['chrome', 'safari', 'finder', 'terminal']):
                    for app in ['chrome', 'safari', 'finder', 'terminal']:
                        if app in user_input:
                            subjects.append(f'{app} application')
            
            if subjects:
                context_summary.append(f"Recent subjects discussed: {', '.join(set(subjects))}")
        
        # Add keyword-based similar interactions from extended history
        similar_interactions = []
        for interaction in self.session_context[-15:]:  # Look at last 15 interactions for patterns
            if any(word in interaction['user_input'].lower() for word in current_input.lower().split()):
                similar_interactions.append(interaction)
        
        if similar_interactions and len(similar_interactions) > len(recent_conversation):
            context_summary.append("Additional similar interactions:")
            for interaction in similar_interactions[-3:]:  # Last 3 additional similar
                if interaction not in recent_conversation:
                    context_summary.append(f"- User: '{interaction['user_input']}' | Response: '{interaction['chotu_response'][:40]}...'")
        
        return " | ".join(context_summary) if context_summary else "No relevant context"
    
    def learn_preference(self, preference_type: str, value: Any):
        """Learn user preference"""
        self.user_preferences[preference_type] = value
        self.save_context()
        print(f"📝 Learned preference: {preference_type} = {value}")
    
    def get_conversation_summary(self) -> str:
        """Get summary of recent conversation"""
        if not self.session_context:
            return "No recent conversation"
        
        recent = self.session_context[-9:]  # Last 9 interactions (increased from 5)
        summary = f"Recent conversation ({len(recent)} interactions):\n"
        for i, interaction in enumerate(recent, 1):
            summary += f"{i}. User: {interaction['user_input'][:50]}...\n"
        
        return summary
