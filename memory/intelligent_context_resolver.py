#!/usr/bin/env python3
"""
🧠 INTELLIGENT CONTEXT RESOLVER
==============================
Comprehensive context resolution system for ambiguous commands like "increase it"
Checks both ROM (long-term memory) and RAM (short-term memory) for context clues
"""

import json
import re
import sys
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple

# Add the parent directory to the path so we can import from memory module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory.memory_manager import load_ram, load_rom
from memory.context_manager import ContextManager

class IntelligentContextResolver:
    """Advanced context resolution system that mimics human reasoning"""
    
    def __init__(self):
        self.context_manager = ContextManager()
        self.ambiguous_words = ['it', 'this', 'that', 'them', 'these', 'those']
        self.action_words = ['increase', 'decrease', 'set', 'make', 'change', 'turn', 'open', 'close', 'start', 'stop']
        self.subjects_cache = {}  # Cache for frequently referenced subjects
        
    def resolve_ambiguous_command(self, user_input: str) -> Dict[str, Any]:
        """
        Main method to resolve ambiguous commands like "increase it"
        
        Returns:
        {
            "resolved": bool,
            "confidence": int (0-100),
            "resolved_command": str,
            "context_source": str (RAM/ROM/cache),
            "reasoning": str,
            "alternatives": List[str],
            "needs_clarification": bool
        }
        """
        
        # Step 1: Check if command is actually ambiguous
        ambiguity_analysis = self._analyze_ambiguity(user_input)
        
        if not ambiguity_analysis['is_ambiguous']:
            return {
                "resolved": True,
                "confidence": 100,
                "resolved_command": user_input,
                "context_source": "direct",
                "reasoning": "Command is clear and specific",
                "alternatives": [],
                "needs_clarification": False
            }
        
        # Step 2: Multi-layer context search
        context_results = self._search_all_context_layers(user_input, ambiguity_analysis)
        
        # Step 3: Evaluate and rank possible resolutions
        resolution = self._evaluate_context_matches(context_results, user_input)
        
        return resolution
    
    def _analyze_ambiguity(self, command: str) -> Dict[str, Any]:
        """Analyze if command contains ambiguous references"""
        
        command_lower = command.lower().strip()
        words = command_lower.split()
        
        # Check for ambiguous pronouns
        has_ambiguous_pronoun = any(word in self.ambiguous_words for word in words)
        
        # Check for action without explicit subject
        has_action = any(word in self.action_words for word in words)
        
        # Extract the action and ambiguous reference
        action = None
        ambiguous_ref = None
        
        for word in words:
            if word in self.action_words:
                action = word
            if word in self.ambiguous_words:
                ambiguous_ref = word
        
        # Check for numeric values (might provide additional context)
        numeric_values = re.findall(r'\d+%?', command)
        
        return {
            "is_ambiguous": has_ambiguous_pronoun and has_action,
            "action": action,
            "ambiguous_reference": ambiguous_ref,
            "numeric_values": numeric_values,
            "command_words": words
        }
    
    def _search_all_context_layers(self, command: str, ambiguity_analysis: Dict) -> Dict[str, Any]:
        """Search all context layers: RAM, ROM, recent interactions, preferences"""
        
        results = {
            "ram_matches": [],
            "rom_matches": [],
            "recent_interactions": [],
            "preference_matches": [],
            "cached_subjects": []
        }
        
        # Layer 1: Check current RAM (immediate context)
        ram_data = load_ram()
        if ram_data:
            ram_context = self._extract_subjects_from_ram(ram_data)
            results["ram_matches"] = ram_context
        
        # Layer 2: Check recent interactions (last 9 conversations)
        recent_subjects = self._get_recent_interaction_subjects()
        results["recent_interactions"] = recent_subjects
        
        # Layer 3: Check ROM for pattern matches
        rom_subjects = self._search_rom_for_subjects(ambiguity_analysis["action"])
        results["rom_matches"] = rom_subjects
        
        # Layer 4: Check user preferences
        preference_subjects = self._get_preference_subjects()
        results["preference_matches"] = preference_subjects
        
        # Layer 5: Check cached frequently used subjects
        cached_subjects = self._get_cached_subjects(ambiguity_analysis["action"])
        results["cached_subjects"] = cached_subjects
        
        return results
    
    def _extract_subjects_from_ram(self, ram_data: Dict) -> List[Dict]:
        """Extract potential subjects from current RAM data"""
        subjects = []
        
        # Check raw input for subjects
        if 'raw_input' in ram_data:
            detected_subjects = self._detect_subjects_in_text(ram_data['raw_input'])
            subjects.extend(detected_subjects)
        
        # Check NLP analysis if available
        if 'nlp_analysis' in ram_data:
            nlp_subjects = self._extract_subjects_from_nlp(ram_data['nlp_analysis'])
            subjects.extend(nlp_subjects)
        
        # Check memory context
        if 'memory_context' in ram_data:
            memory_subjects = self._detect_subjects_in_text(ram_data['memory_context'])
            subjects.extend(memory_subjects)
        
        return subjects
    
    def _get_recent_interaction_subjects(self) -> List[Dict]:
        """Get subjects from last 9 interactions with timestamps and confidence"""
        subjects = []
        
        # Get conversation history from context manager
        context_summary = self.context_manager.get_conversation_summary()
        
        if hasattr(self.context_manager, 'session_context'):
            recent_interactions = self.context_manager.session_context[-9:]  # Last 9 interactions
            
            for i, interaction in enumerate(recent_interactions):
                timestamp = interaction.get('timestamp', '')
                user_input = interaction.get('user_input', '')
                chotu_response = interaction.get('chotu_response', '')
                
                # Calculate recency score (more recent = higher score)
                recency_score = (i + 1) * 10  # 10, 20, 30... up to 90 for most recent
                
                # Extract subjects from both user input and response
                input_subjects = self._detect_subjects_in_text(user_input)
                response_subjects = self._detect_subjects_in_text(chotu_response)
                
                # Add recency and success info
                for subject in input_subjects + response_subjects:
                    subject.update({
                        "source": "recent_interaction",
                        "recency_score": recency_score,
                        "timestamp": timestamp,
                        "interaction_index": i,
                        "success": interaction.get('success', True)
                    })
                    subjects.append(subject)
        
        return subjects
    
    def _search_rom_for_subjects(self, action: str) -> List[Dict]:
        """Search ROM for subjects related to the action"""
        subjects = []
        rom_data = load_rom()
        
        for entry in rom_data:
            # Check input patterns
            input_pattern = entry.get('input_pattern', '')
            if action and action in input_pattern.lower():
                detected_subjects = self._detect_subjects_in_text(input_pattern)
                for subject in detected_subjects:
                    subject.update({
                        "source": "rom_pattern",
                        "confidence_boost": entry.get('confidence_boost', 0),
                        "success_count": entry.get('success_count', 0),
                        "security_profile": entry.get('security_profile', 'unknown')
                    })
                    subjects.append(subject)
            
            # Check intent and action flow
            intent = entry.get('intent', '')
            action_flow = entry.get('action_flow', [])
            
            context_text = f"{intent} {' '.join(action_flow)}"
            if action and action in context_text.lower():
                detected_subjects = self._detect_subjects_in_text(context_text)
                for subject in detected_subjects:
                    subject.update({
                        "source": "rom_intent",
                        "confidence_boost": entry.get('confidence_boost', 0),
                        "success_count": entry.get('success_count', 0)
                    })
                    subjects.append(subject)
        
        return subjects
    
    def _detect_subjects_in_text(self, text: str) -> List[Dict]:
        """Detect controllable subjects in text using comprehensive patterns"""
        subjects = []
        text_lower = text.lower()
        
        # System controls
        system_controls = {
            'brightness': {'patterns': ['brightness', 'screen brightness', 'display brightness'], 'category': 'system', 'controllable': True},
            'volume': {'patterns': ['volume', 'sound', 'audio volume'], 'category': 'system', 'controllable': True},
            'bluetooth': {'patterns': ['bluetooth', 'bt'], 'category': 'system', 'controllable': True},
            'wifi': {'patterns': ['wifi', 'wi-fi', 'wireless'], 'category': 'system', 'controllable': True},
            'battery': {'patterns': ['battery', 'power'], 'category': 'system', 'controllable': False}
        }
        
        # Applications
        applications = {
            'chrome': {'patterns': ['chrome', 'google chrome', 'browser'], 'category': 'application', 'controllable': True},
            'safari': {'patterns': ['safari'], 'category': 'application', 'controllable': True},
            'finder': {'patterns': ['finder'], 'category': 'application', 'controllable': True},
            'terminal': {'patterns': ['terminal', 'command line'], 'category': 'application', 'controllable': True},
            'youtube': {'patterns': ['youtube', 'video'], 'category': 'media', 'controllable': True}
        }
        
        # Check for all patterns
        all_controls = {**system_controls, **applications}
        
        for subject_name, info in all_controls.items():
            for pattern in info['patterns']:
                if pattern in text_lower:
                    subjects.append({
                        "subject": subject_name,
                        "category": info['category'],
                        "controllable": info['controllable'],
                        "confidence": 80 + (len(pattern) * 2),  # Longer patterns = higher confidence
                        "matched_pattern": pattern,
                        "source_text": text[:100]  # First 100 chars for context
                    })
        
        return subjects
    
    def _get_preference_subjects(self) -> List[Dict]:
        """Get subjects from user preferences"""
        subjects = []
        
        if hasattr(self.context_manager, 'user_preferences'):
            preferences = self.context_manager.user_preferences
            
            for pref_type, value in preferences.items():
                subjects.append({
                    "subject": pref_type,
                    "category": "preference",
                    "controllable": True,
                    "confidence": 70,
                    "source": "user_preference",
                    "current_value": value
                })
        
        return subjects
    
    def _get_cached_subjects(self, action: str) -> List[Dict]:
        """Get frequently used subjects from cache"""
        # This could be implemented with a persistent cache
        # For now, return common defaults based on action
        
        common_subjects = {
            'increase': ['brightness', 'volume'],
            'decrease': ['brightness', 'volume'],
            'set': ['brightness', 'volume', 'wifi', 'bluetooth'],
            'turn': ['bluetooth', 'wifi'],
            'open': ['chrome', 'safari', 'finder', 'terminal'],
            'close': ['chrome', 'safari', 'finder', 'terminal']
        }
        
        subjects = []
        if action in common_subjects:
            for subject in common_subjects[action]:
                subjects.append({
                    "subject": subject,
                    "category": "common_default",
                    "controllable": True,
                    "confidence": 50,
                    "source": "cached_common"
                })
        
        return subjects
    
    def _extract_subjects_from_nlp(self, nlp_analysis: Dict) -> List[Dict]:
        """Extract subjects from NLP analysis"""
        subjects = []
        
        # Check parameters for control types
        if 'parameters' in nlp_analysis:
            params = nlp_analysis['parameters']
            if 'control_type' in params:
                subjects.append({
                    "subject": params['control_type'],
                    "category": "nlp_parameter",
                    "controllable": True,
                    "confidence": 85,
                    "source": "nlp_analysis"
                })
            
            if 'app_name' in params:
                subjects.append({
                    "subject": params['app_name'],
                    "category": "application",
                    "controllable": True,
                    "confidence": 85,
                    "source": "nlp_analysis"
                })
        
        # Check entities
        if 'entities' in nlp_analysis:
            for entity in nlp_analysis['entities']:
                if isinstance(entity, dict) and 'text' in entity:
                    detected = self._detect_subjects_in_text(entity['text'])
                    subjects.extend(detected)
        
        return subjects
    
    def _evaluate_context_matches(self, context_results: Dict, original_command: str) -> Dict[str, Any]:
        """Evaluate and rank all context matches to determine best resolution"""
        
        # Collect all subjects with scores
        all_subjects = []
        
        # Process each layer with different weight multipliers
        layer_weights = {
            "ram_matches": 1.0,           # Highest priority - current context
            "recent_interactions": 0.8,   # High priority - recent conversation
            "rom_matches": 0.6,          # Medium priority - learned patterns
            "preference_matches": 0.4,    # Lower priority - user preferences
            "cached_subjects": 0.2       # Lowest priority - common defaults
        }
        
        for layer, subjects in context_results.items():
            weight = layer_weights.get(layer, 0.1)
            
            for subject in subjects:
                if subject['controllable']:  # Only consider controllable subjects
                    
                    # Calculate composite score
                    base_confidence = subject.get('confidence', 50)
                    recency_score = subject.get('recency_score', 0)
                    success_bonus = subject.get('success_count', 0) * 5
                    
                    # Time decay for older interactions
                    time_bonus = 0
                    if 'timestamp' in subject:
                        time_bonus = self._calculate_time_bonus(subject['timestamp'])
                    
                    composite_score = (base_confidence * weight) + recency_score + success_bonus + time_bonus
                    
                    subject['composite_score'] = composite_score
                    subject['layer'] = layer
                    all_subjects.append(subject)
        
        # Remove duplicates and sort by score
        unique_subjects = self._deduplicate_subjects(all_subjects)
        unique_subjects.sort(key=lambda x: x['composite_score'], reverse=True)
        
        # Determine resolution
        if not unique_subjects:
            return {
                "resolved": False,
                "confidence": 0,
                "resolved_command": original_command,
                "context_source": "none",
                "reasoning": "No relevant context found in any layer",
                "alternatives": [],
                "needs_clarification": True
            }
        
        # Get top candidate
        top_subject = unique_subjects[0]
        alternatives = [s['subject'] for s in unique_subjects[1:4]]  # Top 3 alternatives
        
        # Generate resolved command
        resolved_command = self._generate_resolved_command(original_command, top_subject)
        
        # Determine confidence level
        confidence = min(int(top_subject['composite_score']), 100)
        
        # Generate reasoning
        reasoning = self._generate_reasoning(top_subject, len(unique_subjects))
        
        return {
            "resolved": confidence >= 60,
            "confidence": confidence,
            "resolved_command": resolved_command,
            "context_source": top_subject['layer'],
            "reasoning": reasoning,
            "alternatives": alternatives,
            "needs_clarification": confidence < 60
        }
    
    def _calculate_time_bonus(self, timestamp: str) -> float:
        """Calculate time-based bonus (more recent = higher bonus)"""
        try:
            if 'T' in timestamp:
                interaction_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            else:
                interaction_time = datetime.fromisoformat(timestamp)
            
            now = datetime.now()
            if interaction_time.tzinfo is None:
                interaction_time = interaction_time.replace(tzinfo=now.tzinfo)
            
            time_diff = now - interaction_time
            hours_ago = time_diff.total_seconds() / 3600
            
            # Exponential decay: recent interactions get much higher bonus
            if hours_ago < 0.1:    # < 6 minutes
                return 30
            elif hours_ago < 0.5:  # < 30 minutes
                return 20
            elif hours_ago < 2:    # < 2 hours
                return 10
            elif hours_ago < 6:    # < 6 hours
                return 5
            else:
                return 0
        except:
            return 0
    
    def _deduplicate_subjects(self, subjects: List[Dict]) -> List[Dict]:
        """Remove duplicate subjects, keeping the highest scoring one"""
        seen_subjects = {}
        
        for subject in subjects:
            subject_name = subject['subject']
            
            if subject_name not in seen_subjects or subject['composite_score'] > seen_subjects[subject_name]['composite_score']:
                seen_subjects[subject_name] = subject
        
        return list(seen_subjects.values())
    
    def _generate_resolved_command(self, original_command: str, subject: Dict) -> str:
        """Generate the resolved command by replacing ambiguous reference"""
        
        # Extract action and numeric value from original command
        words = original_command.lower().split()
        action = None
        numeric_value = ""
        
        for word in words:
            if word in self.action_words:
                action = word
        
        # Extract numeric values
        numeric_matches = re.findall(r'\d+%?', original_command)
        if numeric_matches:
            numeric_value = f" {numeric_matches[0]}"
        
        # Generate resolved command
        subject_name = subject['subject']
        
        if action:
            resolved = f"{action} {subject_name}{numeric_value}"
        else:
            resolved = f"control {subject_name}{numeric_value}"
        
        return resolved.strip()
    
    def _generate_reasoning(self, subject: Dict, total_candidates: int) -> str:
        """Generate human-readable reasoning for the resolution"""
        
        source_explanations = {
            "ram_matches": "found in current session data",
            "recent_interactions": f"mentioned in recent conversation (interaction #{subject.get('interaction_index', '?')})",
            "rom_matches": "found in learned patterns from past successful commands",
            "preference_matches": "matches your saved preferences",
            "cached_subjects": "common default for this type of command"
        }
        
        source = subject.get('layer', 'unknown')
        base_reason = source_explanations.get(source, f"found in {source}")
        
        confidence = subject.get('composite_score', 0)
        additional_context = []
        
        if 'timestamp' in subject:
            additional_context.append(f"last mentioned recently")
        
        if subject.get('success_count', 0) > 0:
            additional_context.append(f"previously used successfully {subject['success_count']} times")
        
        if total_candidates > 1:
            additional_context.append(f"selected from {total_candidates} possible options")
        
        reasoning = f"'{subject['subject']}' was {base_reason}"
        if additional_context:
            reasoning += f" ({', '.join(additional_context)})"
        
        return reasoning
    
    def get_clarification_question(self, alternatives: List[str], original_command: str) -> str:
        """Generate a clarification question when context is unclear"""
        
        if not alternatives:
            return f"I'm not sure what you want me to {original_command}. Could you be more specific?"
        
        if len(alternatives) <= 3:
            options = ", ".join(alternatives[:-1])
            if len(alternatives) > 1:
                options += f", or {alternatives[-1]}"
            else:
                options = alternatives[0]
            
            return f"Do you want me to {original_command} {options}?"
        else:
            return f"I found several possibilities: {', '.join(alternatives[:3])}, and others. Which one did you mean?"

# Singleton instance
_resolver = IntelligentContextResolver()

def resolve_ambiguous_command(user_input: str) -> Dict[str, Any]:
    """Main function to resolve ambiguous commands"""
    return _resolver.resolve_ambiguous_command(user_input)

def get_clarification_question(alternatives: List[str], original_command: str) -> str:
    """Get clarification question for ambiguous commands"""
    return _resolver.get_clarification_question(alternatives, original_command)

if __name__ == "__main__":
    # Test the context resolver
    print("🧠 Testing Intelligent Context Resolver")
    print("=" * 50)
    
    test_commands = [
        "increase it",
        "decrease it by 20%",
        "set it to 70",
        "turn it off",
        "open it",
        "close it",
        "make it brighter",
        "turn up the volume"  # Not ambiguous
    ]
    
    resolver = IntelligentContextResolver()
    
    for cmd in test_commands:
        print(f"\n🔍 Testing: '{cmd}'")
        result = resolver.resolve_ambiguous_command(cmd)
        
        print(f"   Resolved: {result['resolved']}")
        print(f"   Confidence: {result['confidence']}%")
        print(f"   Command: '{result['resolved_command']}'")
        print(f"   Source: {result['context_source']}")
        print(f"   Reasoning: {result['reasoning']}")
        
        if result['alternatives']:
            print(f"   Alternatives: {result['alternatives']}")
        
        if result['needs_clarification']:
            question = get_clarification_question(result['alternatives'], cmd)
            print(f"   Question: {question}")
