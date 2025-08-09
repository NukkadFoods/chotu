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
        
        # Keep only last 50 interactions in memory
        if len(self.session_context) > 50:
            self.session_context = self.session_context[-50:]
        
        self.save_context()
    
    def get_relevant_context(self, current_input: str) -> str:
        """Get relevant context for current input"""
        context_summary = []
        
        # Add user preferences
        if self.user_preferences:
            context_summary.append(f"User preferences: {self.user_preferences}")
        
        # Add recent similar interactions
        similar_interactions = []
        for interaction in self.session_context[-10:]:  # Last 10 interactions
            if any(word in interaction['user_input'].lower() for word in current_input.lower().split()):
                similar_interactions.append(interaction)
        
        if similar_interactions:
            context_summary.append("Recent similar interactions:")
            for interaction in similar_interactions[-3:]:  # Last 3 similar
                context_summary.append(f"- User: {interaction['user_input']} | Success: {interaction['success']}")
        
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
        
        recent = self.session_context[-5:]  # Last 5 interactions
        summary = f"Recent conversation ({len(recent)} interactions):\n"
        for i, interaction in enumerate(recent, 1):
            summary += f"{i}. User: {interaction['user_input'][:50]}...\n"
        
        return summary
