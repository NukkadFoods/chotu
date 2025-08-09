# utils/nlp_processor.py
import re
from typing import Dict, List, Tuple
from datetime import datetime, timedelta

class NLPProcessor:
    """Advanced natural language processing for Chotu"""
    
    def __init__(self):
        # Intent patterns
        self.intent_patterns = {
            'system_control': [
                r'(turn|set|adjust|change)\s+(up|down|volume|brightness)',
                r'(increase|decrease|raise|lower)\s+(volume|brightness)',
                r'(mute|unmute|silent|quiet)',
                r'(sleep|shutdown|restart|reboot)'
            ],
            'app_control': [
                r'(open|launch|start|run)\s+(\w+)',
                r'(close|quit|exit|stop)\s+(\w+)',
                r'(switch to|go to)\s+(\w+)'
            ],
            'file_operations': [
                r'(open|show|find|search)\s+(file|folder|directory)',
                r'(create|make|new)\s+(file|folder|document)',
                r'(delete|remove|trash)\s+'
            ],
            'information': [
                r'(what|who|when|where|how|why)',
                r'(tell me|show me|explain)',
                r'(weather|time|date|news)'
            ],
            'communication': [
                r'(send|write|compose)\s+(email|message|text)',
                r'(call|phone|dial)',
                r'(schedule|calendar|meeting|appointment)'
            ],
            'web_search': [
                r'(search|google|find|look up)',
                r'(browse|navigate|visit)\s+(website|url|site)'
            ]
        }
        
        # Entity extraction patterns
        self.entity_patterns = {
            'app_name': r'(safari|chrome|firefox|code|vscode|visual studio|finder|spotify|music|calculator|notes|calendar|mail)',
            'time': r'(\d{1,2}:\d{2}|\d{1,2}\s*(am|pm)|now|today|tomorrow|yesterday)',
            'number': r'\b(\d+)\b',
            'url': r'(https?://[\w\.-]+|[\w\.-]+\.(com|org|net|edu|gov))',
            'file_type': r'\.(pdf|doc|txt|jpg|png|mp3|mp4|zip|py|js|html)'
        }
    
    def extract_intent(self, text: str) -> str:
        """Extract primary intent from user input"""
        text_lower = text.lower()
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return intent
        
        return 'general'
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract entities from user input"""
        entities = {}
        
        for entity_type, pattern in self.entity_patterns.items():
            matches = re.findall(pattern, text.lower())
            if matches:
                entities[entity_type] = matches
        
        return entities
    
    def analyze_sentiment(self, text: str) -> str:
        """Basic sentiment analysis"""
        positive_words = ['good', 'great', 'awesome', 'excellent', 'perfect', 'love', 'like', 'happy', 'thanks']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'dislike', 'sad', 'angry', 'frustrated', 'error']
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
    
    def extract_parameters(self, text: str, intent: str) -> Dict[str, str]:
        """Extract parameters based on intent"""
        parameters = {}
        text_lower = text.lower()
        
        if intent == 'system_control':
            if 'volume' in text_lower:
                parameters['control_type'] = 'volume'
                if any(word in text_lower for word in ['up', 'increase', 'raise']):
                    parameters['action'] = 'increase'
                elif any(word in text_lower for word in ['down', 'decrease', 'lower']):
                    parameters['action'] = 'decrease'
                elif 'mute' in text_lower:
                    parameters['action'] = 'mute'
            
            elif 'brightness' in text_lower:
                parameters['control_type'] = 'brightness'
                if any(word in text_lower for word in ['up', 'increase', 'raise']):
                    parameters['action'] = 'increase'
                elif any(word in text_lower for word in ['down', 'decrease', 'lower']):
                    parameters['action'] = 'decrease'
        
        elif intent == 'app_control':
            app_match = re.search(r'(open|launch|start|run|close|quit|exit|stop)\s+(\w+)', text_lower)
            if app_match:
                parameters['action'] = app_match.group(1)
                parameters['app_name'] = app_match.group(2)
        
        return parameters
    
    def generate_response_context(self, text: str) -> Dict[str, str]:
        """Generate context for response generation"""
        intent = self.extract_intent(text)
        entities = self.extract_entities(text)
        sentiment = self.analyze_sentiment(text)
        parameters = self.extract_parameters(text, intent)
        
        return {
            'intent': intent,
            'entities': entities,
            'sentiment': sentiment,
            'parameters': parameters,
            'complexity': 'high' if len(text.split()) > 10 else 'low',
            'timestamp': datetime.now().isoformat()
        }
