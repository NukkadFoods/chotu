#!/usr/bin/env python3
"""
🧠 ENHANCED CONTEXT MANAGER
==========================
Selective enhancements to Chotu's existing context system
"""

import json
import os
import time
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

# Optional semantic embeddings
try:
    from sentence_transformers import SentenceTransformer
    SEMANTIC_AVAILABLE = True
except ImportError:
    SEMANTIC_AVAILABLE = False
    SentenceTransformer = None

class EnhancedContextManager:
    """Enhanced context management building on existing Chotu architecture"""
    
    def __init__(self):
        # Keep existing functionality
        self.context_file = "memory/context.json"
        self.session_context = []
        self.user_preferences = {}
        
        # Add semantic embeddings for better similarity
        if SEMANTIC_AVAILABLE:
            try:
                self.embedder = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight model
                self.semantic_enabled = True
                print("🧠 Semantic embeddings enabled")
            except Exception as e:
                self.semantic_enabled = False
                print(f"⚠️ Semantic embeddings error: {e}")
        else:
            self.semantic_enabled = False
            print("⚠️ Semantic embeddings disabled (install sentence-transformers)")
        
        # Enhanced confidence thresholds (building on existing system)
        self.confidence_thresholds = {
            'immediate_action': 90,    # Existing high confidence threshold
            'clarify_and_act': 70,     # New: moderate confidence with clarification
            'ask_questions': 40,       # Existing medium confidence threshold  
            'suggest_alternatives': 20  # New: very low confidence with suggestions
        }
        
        self.load_context()
    
    def load_context(self):
        """Enhanced context loading with semantic analysis"""
        try:
            if os.path.exists(self.context_file):
                with open(self.context_file, 'r') as f:
                    data = json.load(f)
                    self.user_preferences = data.get('preferences', {})
                    
                    # Load recent context (keep existing 24-hour window)
                    recent_context = []
                    cutoff = datetime.now() - timedelta(hours=24)
                    for item in data.get('session_history', []):
                        item_time = datetime.fromisoformat(item['timestamp'])
                        if item_time > cutoff:
                            recent_context.append(item)
                    
                    self.session_context = recent_context
                    
                    # Add semantic embeddings to existing interactions
                    if self.semantic_enabled:
                        self._add_semantic_embeddings()
                        
        except Exception as e:
            print(f"⚠️ Enhanced context load error: {e}")
    
    def _add_semantic_embeddings(self):
        """Add semantic embeddings to interactions that don't have them"""
        for interaction in self.session_context:
            if 'embedding' not in interaction and self.semantic_enabled:
                try:
                    text = f"{interaction['user_input']} {interaction.get('chotu_response', '')}"
                    embedding = self.embedder.encode(text).tolist()
                    interaction['embedding'] = embedding
                except Exception as e:
                    print(f"⚠️ Embedding error: {e}")
    
    def get_enhanced_context(self, current_input: str, confidence_score: float) -> Dict[str, Any]:
        """Enhanced context retrieval based on confidence level"""
        
        context_data = {
            'textual_context': self._get_textual_context(current_input),
            'semantic_context': self._get_semantic_context(current_input) if self.semantic_enabled else None,
            'confidence_analysis': self._analyze_confidence_gaps(current_input, confidence_score),
            'clarification_needed': confidence_score < self.confidence_thresholds['clarify_and_act'],
            'suggested_questions': self._generate_clarifying_questions(current_input, confidence_score)
        }
        
        return context_data
    
    def _get_textual_context(self, current_input: str) -> Dict[str, Any]:
        """Enhanced version of existing textual context (builds on current implementation)"""
        context = {
            'recent_interactions': self.session_context[-9:],  # Keep existing 9-interaction window
            'user_preferences': self.user_preferences,
            'ambiguity_resolution': self._resolve_ambiguous_references(current_input),
            'conversation_topics': self._extract_conversation_topics()
        }
        
        return context
    
    def _get_semantic_context(self, current_input: str) -> Optional[Dict[str, Any]]:
        """Semantic similarity search for better context matching"""
        if not self.semantic_enabled or not self.session_context:
            return None
        
        try:
            # Encode current input
            current_embedding = self.embedder.encode(current_input)
            
            # Find most similar interactions
            similarities = []
            for interaction in self.session_context:
                if 'embedding' in interaction:
                    similarity = np.dot(current_embedding, interaction['embedding'])
                    similarities.append({
                        'interaction': interaction,
                        'similarity': float(similarity),
                        'timestamp': interaction['timestamp']
                    })
            
            # Sort by similarity and recency (weighted)
            similarities.sort(key=lambda x: x['similarity'] * 0.7 + 
                            (time.time() - time.mktime(datetime.fromisoformat(x['timestamp']).timetuple())) / 86400 * 0.3, 
                            reverse=True)
            
            return {
                'most_similar': similarities[:3],  # Top 3 most similar
                'similarity_threshold': 0.7,  # Configurable threshold
                'semantic_patterns': self._extract_semantic_patterns(similarities[:5])
            }
            
        except Exception as e:
            print(f"⚠️ Semantic context error: {e}")
            return None
    
    def _analyze_confidence_gaps(self, user_input: str, confidence: float) -> Dict[str, Any]:
        """Analyze what's causing low confidence and suggest improvements"""
        
        gaps = {
            'clarity_issues': [],
            'missing_context': [],
            'ambiguous_terms': [],
            'suggestions': []
        }
        
        # Clarity analysis
        words = user_input.lower().split()
        if len(words) < 3:
            gaps['clarity_issues'].append("Command is very short")
        
        if any(word in words for word in ['it', 'that', 'this', 'them']):
            gaps['ambiguous_terms'].extend([word for word in words if word in ['it', 'that', 'this', 'them']])
        
        # Context analysis based on confidence level
        if confidence < self.confidence_thresholds['ask_questions']:
            gaps['missing_context'].append("Low confidence suggests unclear intent")
            
        if confidence < self.confidence_thresholds['suggest_alternatives']:
            gaps['suggestions'].append("Consider rephrasing with specific action words")
            gaps['suggestions'].append("Try being more specific about what you want")
        
        return gaps
    
    def _generate_clarifying_questions(self, user_input: str, confidence: float) -> List[str]:
        """Generate contextual clarifying questions based on confidence gaps"""
        
        questions = []
        
        # If very low confidence
        if confidence < self.confidence_thresholds['suggest_alternatives']:
            questions.extend([
                "Could you be more specific about what you'd like me to do?",
                "What specific action would you like me to perform?",
                "Are you asking me to control something, get information, or manage an application?"
            ])
        
        # If medium-low confidence with ambiguous references
        elif confidence < self.confidence_thresholds['clarify_and_act']:
            words = user_input.lower().split()
            if any(word in words for word in ['it', 'that', 'this']):
                # Look at recent context to suggest what "it" might refer to
                recent_topics = self._extract_conversation_topics()
                if recent_topics:
                    questions.append(f"Are you referring to {', '.join(recent_topics[:2])}?")
                else:
                    questions.append("What specifically are you referring to?")
            
            if any(word in words for word in ['increase', 'decrease', 'change', 'set']):
                questions.append("What would you like me to adjust - volume, brightness, or something else?")
        
        return questions[:2]  # Return max 2 questions to avoid overwhelming
    
    def _resolve_ambiguous_references(self, current_input: str) -> Dict[str, Any]:
        """Enhanced ambiguity resolution (builds on existing functionality)"""
        resolution = {
            'ambiguous_terms_found': [],
            'possible_references': {},
            'confidence_in_resolution': 0.0
        }
        
        words = current_input.lower().split()
        ambiguous_terms = [word for word in words if word in ['it', 'that', 'this', 'them']]
        
        if ambiguous_terms:
            resolution['ambiguous_terms_found'] = ambiguous_terms
            
            # Look at recent interactions for context (enhanced from existing)
            recent_subjects = []
            for interaction in self.session_context[-5:]:  # Last 5 interactions
                text = interaction['user_input'].lower()
                if 'brightness' in text: recent_subjects.append('brightness')
                if 'volume' in text: recent_subjects.append('volume')
                if any(app in text for app in ['chrome', 'safari', 'finder']):
                    for app in ['chrome', 'safari', 'finder']:
                        if app in text: recent_subjects.append(f'{app} application')
            
            if recent_subjects:
                # Get most recent subject
                resolution['possible_references'] = {
                    'most_likely': recent_subjects[-1],
                    'alternatives': list(set(recent_subjects[:-1])),
                    'context_basis': 'recent_conversation'
                }
                resolution['confidence_in_resolution'] = 0.8 if len(recent_subjects) >= 2 else 0.6
        
        return resolution
    
    def _extract_conversation_topics(self) -> List[str]:
        """Extract main topics from recent conversation"""
        topics = []
        
        for interaction in self.session_context[-5:]:
            text = interaction['user_input'].lower()
            
            # System control topics
            if any(word in text for word in ['brightness', 'bright']): topics.append('brightness')
            if any(word in text for word in ['volume', 'sound', 'audio']): topics.append('volume')
            if any(word in text for word in ['bluetooth', 'wireless']): topics.append('bluetooth')
            
            # Application topics
            apps = ['chrome', 'safari', 'finder', 'terminal', 'vscode', 'code']
            for app in apps:
                if app in text: topics.append(f'{app} app')
            
            # Information topics
            if any(word in text for word in ['weather', 'time', 'date']): topics.append('information')
        
        # Return unique topics in reverse order (most recent first)
        return list(dict.fromkeys(reversed(topics)))
    
    def _extract_semantic_patterns(self, similar_interactions: List[Dict]) -> Dict[str, Any]:
        """Extract patterns from semantically similar interactions"""
        if not similar_interactions:
            return {}
        
        patterns = {
            'common_intents': [],
            'successful_patterns': [],
            'failure_patterns': []
        }
        
        for item in similar_interactions:
            interaction = item['interaction']
            if interaction.get('success', False):
                patterns['successful_patterns'].append({
                    'input': interaction['user_input'],
                    'response': interaction['chotu_response'][:50] + "...",
                    'similarity': item['similarity']
                })
            else:
                patterns['failure_patterns'].append({
                    'input': interaction['user_input'],
                    'error': interaction.get('chotu_response', 'Unknown error'),
                    'similarity': item['similarity']
                })
        
        return patterns
    
    def add_interaction_with_analysis(self, user_input: str, chotu_response: str, 
                                    success: bool = True, confidence: float = 0.0):
        """Enhanced interaction logging with confidence tracking"""
        
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'user_input': user_input,
            'chotu_response': chotu_response,
            'success': success,
            'confidence': confidence,
            'session_id': len(self.session_context)
        }
        
        # Add semantic embedding if available
        if self.semantic_enabled:
            try:
                text = f"{user_input} {chotu_response}"
                embedding = self.embedder.encode(text).tolist()
                interaction['embedding'] = embedding
            except Exception as e:
                print(f"⚠️ Embedding error: {e}")
        
        self.session_context.append(interaction)
        
        # Keep last 100 interactions (same as existing)
        if len(self.session_context) > 100:
            self.session_context = self.session_context[-100:]
        
        self.save_context()
    
    def get_confidence_enhancement_suggestions(self, user_input: str, current_confidence: float) -> Dict[str, Any]:
        """Suggest how to improve confidence for unclear commands"""
        
        suggestions = {
            'current_confidence': current_confidence,
            'target_confidence': self.confidence_thresholds['immediate_action'],
            'improvements_needed': [],
            'example_rephrasings': []
        }
        
        # Analyze why confidence is low
        if current_confidence < self.confidence_thresholds['clarify_and_act']:
            if len(user_input.split()) < 3:
                suggestions['improvements_needed'].append("Add more descriptive words")
                suggestions['example_rephrasings'].append(f"Instead of '{user_input}', try 'Please {user_input} the system volume'")
            
            if any(word in user_input.lower() for word in ['it', 'that', 'this']):
                suggestions['improvements_needed'].append("Replace ambiguous references with specific terms")
                suggestions['example_rephrasings'].append("Instead of 'increase it', try 'increase the brightness'")
        
        return suggestions

# Global enhanced context manager
_enhanced_context = None

def get_enhanced_context_manager():
    """Get global enhanced context manager instance"""
    global _enhanced_context
    if _enhanced_context is None:
        _enhanced_context = EnhancedContextManager()
    return _enhanced_context
