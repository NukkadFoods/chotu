#!/usr/bin/env python3
"""
🔍 CONTEXT VALIDATOR
===================
Uses GPT to validate if resolved context makes logical sense
and provides intelligent reasoning for ambiguous commands
"""

import json
import sys
import os
from typing import Dict, List, Any, Optional

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.gpt_interface import call_gpt

class ContextValidator:
    """Validates resolved context using GPT for logical reasoning"""
    
    def __init__(self):
        self.controllable_properties = {
            'brightness': ['increase', 'decrease', 'set', 'adjust'],
            'volume': ['increase', 'decrease', 'set', 'turn up', 'turn down', 'mute'],
            'bluetooth': ['turn on', 'turn off', 'enable', 'disable', 'connect', 'disconnect'],
            'wifi': ['turn on', 'turn off', 'enable', 'disable', 'connect', 'disconnect'],
            'chrome': ['open', 'close', 'quit', 'restart', 'refresh'],
            'safari': ['open', 'close', 'quit', 'restart', 'refresh'],
            'finder': ['open', 'close', 'quit', 'restart'],
            'terminal': ['open', 'close', 'quit', 'restart'],
            'youtube': ['play', 'pause', 'stop', 'open', 'close']
        }
    
    def validate_context_resolution(self, 
                                  original_command: str,
                                  resolved_command: str, 
                                  context_data: Dict[str, Any],
                                  alternatives: List[str]) -> Dict[str, Any]:
        """
        Validate if the resolved context makes logical sense
        
        Args:
            original_command: The original ambiguous command
            resolved_command: The resolved command from context
            context_data: Context resolution data
            alternatives: Alternative subjects found
        
        Returns:
            Dict with validation results and reasoning
        """
        
        # Extract action and subject from resolved command
        action, subject = self._extract_action_subject(resolved_command)
        
        # Check if the action-subject combination makes sense
        logical_validation = self._check_logical_validity(action, subject)
        
        if logical_validation['makes_sense']:
            return {
                "valid": True,
                "confidence": context_data.get('confidence', 80),
                "final_command": resolved_command,
                "reasoning": f"'{action} {subject}' is a valid operation",
                "needs_clarification": False,
                "suggested_action": resolved_command
            }
        
        # If it doesn't make sense, use GPT to analyze and suggest alternatives
        gpt_analysis = self._get_gpt_context_analysis(
            original_command, 
            resolved_command,
            alternatives,
            context_data,
            logical_validation
        )
        
        return gpt_analysis
    
    def _extract_action_subject(self, command: str) -> tuple:
        """Extract action and subject from command"""
        words = command.lower().split()
        
        action_words = ['increase', 'decrease', 'set', 'make', 'turn', 'open', 'close', 'start', 'stop']
        
        action = None
        subject = None
        
        for i, word in enumerate(words):
            if word in action_words:
                action = word
                # Subject is usually the next word(s)
                if i + 1 < len(words):
                    subject = words[i + 1]
                break
        
        return action or words[0] if words else "", subject or ""
    
    def _check_logical_validity(self, action: str, subject: str) -> Dict[str, Any]:
        """Check if action-subject combination makes logical sense"""
        
        if subject in self.controllable_properties:
            valid_actions = self.controllable_properties[subject]
            
            # Check for exact match
            if action in valid_actions:
                return {
                    "makes_sense": True,
                    "reason": f"'{action}' is a valid operation for {subject}",
                    "valid_actions": valid_actions
                }
            
            # Check for semantic similarity
            semantic_matches = {
                'increase': ['turn up', 'raise', 'boost'],
                'decrease': ['turn down', 'lower', 'reduce'],
                'turn': ['enable', 'disable', 'toggle']
            }
            
            for valid_action in valid_actions:
                if action in semantic_matches.get(valid_action, []):
                    return {
                        "makes_sense": True,
                        "reason": f"'{action}' is semantically equivalent to '{valid_action}' for {subject}",
                        "valid_actions": valid_actions,
                        "suggested_action": valid_action
                    }
        
        return {
            "makes_sense": False,
            "reason": f"'{action}' is not a valid operation for {subject}",
            "valid_actions": self.controllable_properties.get(subject, []),
            "subject_category": self._categorize_subject(subject)
        }
    
    def _categorize_subject(self, subject: str) -> str:
        """Categorize the subject type"""
        categories = {
            'system_control': ['brightness', 'volume', 'bluetooth', 'wifi'],
            'application': ['chrome', 'safari', 'finder', 'terminal'],
            'media': ['youtube', 'spotify', 'music'],
            'unknown': []
        }
        
        for category, subjects in categories.items():
            if subject in subjects:
                return category
        
        return 'unknown'
    
    def _get_gpt_context_analysis(self, 
                                original_command: str,
                                resolved_command: str, 
                                alternatives: List[str],
                                context_data: Dict[str, Any],
                                logical_validation: Dict[str, Any]) -> Dict[str, Any]:
        """Use GPT to analyze context and provide intelligent reasoning"""
        
        prompt = f"""
You are Chotu, an advanced AI assistant with intelligent context reasoning capabilities.

SITUATION ANALYSIS:
==================
Original Command: "{original_command}"
Context-Resolved Command: "{resolved_command}"
Context Confidence: {context_data.get('confidence', 0)}%
Context Source: {context_data.get('context_source', 'unknown')}
Context Reasoning: {context_data.get('reasoning', 'No reasoning provided')}

LOGICAL VALIDATION RESULTS:
===========================
Makes Logical Sense: {logical_validation['makes_sense']}
Reason: {logical_validation['reason']}
Valid Actions for Subject: {logical_validation.get('valid_actions', [])}
Subject Category: {logical_validation.get('subject_category', 'unknown')}

ALTERNATIVE SUBJECTS FOUND:
===========================
{alternatives}

CONTROLLABLE PROPERTIES REFERENCE:
==================================
brightness: increase, decrease, set, adjust
volume: increase, decrease, set, turn up, turn down, mute
bluetooth: turn on, turn off, enable, disable, connect, disconnect
wifi: turn on, turn off, enable, disable, connect, disconnect
chrome: open, close, quit, restart, refresh
safari: open, close, quit, restart, refresh

ACTION-SUBJECT COMPATIBILITY RULES:
===================================
- "turn off" or "turn on" → bluetooth, wifi (system controls that can be toggled)
- "increase" or "decrease" → brightness, volume (numeric values that can be changed)
- "open" or "close" → chrome, safari, finder, terminal (applications)
- "set" → brightness, volume, bluetooth, wifi (any controllable property)

YOUR TASK:
==========
1. Analyze if the context resolution makes sense
2. If not, determine what the user ACTUALLY meant based on the ACTION
3. Look at the alternatives and find the most logical subject for the SPECIFIC ACTION
4. CRITICAL: Match the action type correctly (turn off ≠ increase)
5. Provide clear reasoning for your decision

EXAMPLE REASONING PROCESS:
=========================
- "turn chrome off" doesn't make sense → chrome can be "closed" not "turned off"
- User said "turn it off" after mentioning bluetooth and chrome
- "turn off" action is compatible with: bluetooth, wifi (system controls)
- "turn off" action is NOT compatible with: chrome (applications use "close")
- Looking at alternatives: bluetooth CAN be turned off
- Most likely user meant "turn bluetooth off"

CRITICAL: Do NOT suggest actions that don't match the user's intent:
- If user says "turn off" → suggest "turn X off", NOT "increase Y"
- If user says "increase" → suggest "increase X", NOT "turn Y off"
- If user says "close" → suggest "close X", NOT "turn Y off"

Respond in JSON format:
{{
    "valid": true/false,
    "confidence": 85,
    "final_command": "turn bluetooth off" or "NEEDS_CLARIFICATION",
    "reasoning": "Detailed explanation of why the original resolution was wrong and what user likely meant",
    "needs_clarification": true/false,
    "suggested_action": "specific command to execute that matches the original action intent",
    "clarification_question": "What would you like me to ask the user?",
    "context_analysis": "Analysis of why the context resolver made this mistake"
}}
"""
        
        try:
            response = call_gpt(prompt)
            
            # Clean and parse JSON
            response = response.strip()
            if response.startswith('```json'):
                response = response[7:]
            if response.endswith('```'):
                response = response[:-3]
            response = response.strip()
            
            # Extract JSON from any explanatory text
            if '{' in response and '}' in response:
                start = response.find('{')
                end = response.rfind('}') + 1
                response = response[start:end]
            
            result = json.loads(response)
            return result
            
        except Exception as e:
            print(f"❌ GPT context analysis failed: {e}")
            
            # Fallback analysis
            return self._fallback_analysis(original_command, alternatives, logical_validation)
    
    def _fallback_analysis(self, 
                          original_command: str, 
                          alternatives: List[str],
                          logical_validation: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback analysis when GPT fails - with proper action-subject matching"""
        
        # Extract action from original command
        words = original_command.lower().split()
        action = None
        
        action_words = ['increase', 'decrease', 'set', 'make', 'turn', 'open', 'close', 'start', 'stop']
        for word in words:
            if word in action_words:
                action = word
                break
        
        if not action:
            return {
                "valid": False,
                "confidence": 20,
                "final_command": "NEEDS_CLARIFICATION",
                "reasoning": "Could not identify the action in the command",
                "needs_clarification": True,
                "suggested_action": None,
                "clarification_question": "I'm not sure what you want me to do. Could you be more specific?",
                "context_analysis": "No clear action found in command"
            }
        
        # Find suitable alternatives based on action compatibility
        suitable_alternatives = []
        
        # Create action compatibility map
        action_compatibility = {
            'increase': ['brightness', 'volume'],
            'decrease': ['brightness', 'volume'],
            'set': ['brightness', 'volume', 'bluetooth', 'wifi'],
            'turn': ['bluetooth', 'wifi'],  # turn on/off
            'open': ['chrome', 'safari', 'finder', 'terminal'],
            'close': ['chrome', 'safari', 'finder', 'terminal'],
            'start': ['chrome', 'safari', 'finder', 'terminal'],
            'stop': ['chrome', 'safari', 'finder', 'terminal']
        }
        
        # Handle compound actions like "turn off", "turn on"
        if action == 'turn':
            if 'off' in words or 'disable' in words:
                action_type = 'turn off'
                compatible_subjects = ['bluetooth', 'wifi', 'chrome', 'safari', 'finder', 'terminal']
            elif 'on' in words or 'enable' in words:
                action_type = 'turn on'
                compatible_subjects = ['bluetooth', 'wifi', 'chrome', 'safari', 'finder', 'terminal']
            else:
                action_type = 'turn'
                compatible_subjects = ['bluetooth', 'wifi']
        else:
            action_type = action
            compatible_subjects = action_compatibility.get(action, [])
        
        # Find alternatives that are compatible with the action
        for alt in alternatives:
            if alt in compatible_subjects:
                suitable_alternatives.append(alt)
        
        # If no alternatives found in the list, check if any alternatives can work with the action
        if not suitable_alternatives:
            for alt in alternatives:
                if alt in self.controllable_properties:
                    valid_actions = self.controllable_properties[alt]
                    
                    # Check for direct action match
                    if action in valid_actions:
                        suitable_alternatives.append(alt)
                    # Check for semantic matches (turn off = disable, etc.)
                    elif action == 'turn' and ('turn on' in valid_actions or 'turn off' in valid_actions):
                        suitable_alternatives.append(alt)
                    elif action == 'turn' and ('enable' in valid_actions or 'disable' in valid_actions):
                        suitable_alternatives.append(alt)
        
        if suitable_alternatives:
            # Prioritize the most appropriate alternative
            best_alternative = suitable_alternatives[0]
            
            # For "turn off" commands, prioritize system controls over applications
            if action == 'turn' and 'off' in words:
                system_controls = ['bluetooth', 'wifi']
                for sys_ctrl in system_controls:
                    if sys_ctrl in suitable_alternatives:
                        best_alternative = sys_ctrl
                        break
            
            # Generate the corrected command
            if action == 'turn' and ('off' in words or 'on' in words):
                if 'off' in words:
                    final_command = f"turn {best_alternative} off"
                else:
                    final_command = f"turn {best_alternative} on"
            else:
                final_command = f"{action} {best_alternative}"
            
            return {
                "valid": False,
                "confidence": 75,
                "final_command": final_command,
                "reasoning": f"'{logical_validation['reason']}'. However, '{final_command}' would make logical sense based on the action '{action_type}'.",
                "needs_clarification": len(suitable_alternatives) > 1,
                "suggested_action": final_command,
                "clarification_question": f"Did you mean to {action_type} {' or '.join(suitable_alternatives)}?" if len(suitable_alternatives) > 1 else None,
                "context_analysis": f"Context resolver found incompatible subject, but '{best_alternative}' is compatible with action '{action_type}'"
            }
        
        return {
            "valid": False,
            "confidence": 30,
            "final_command": "NEEDS_CLARIFICATION",
            "reasoning": f"'{logical_validation['reason']}' and no suitable alternatives found that are compatible with action '{action}'.",
            "needs_clarification": True,
            "suggested_action": None,
            "clarification_question": f"I'm not sure what you want me to {action}. Could you be more specific?",
            "context_analysis": f"No alternatives found that are compatible with the action '{action}'"
        }

# Singleton instance
_validator = ContextValidator()

def validate_context_resolution(original_command: str,
                               resolved_command: str, 
                               context_data: Dict[str, Any],
                               alternatives: List[str]) -> Dict[str, Any]:
    """Main function to validate context resolution"""
    return _validator.validate_context_resolution(
        original_command, resolved_command, context_data, alternatives
    )

if __name__ == "__main__":
    # Test the context validator
    print("🔍 Testing Context Validator")
    print("=" * 40)
    
    test_cases = [
        {
            "original": "increase it",
            "resolved": "increase chrome",
            "context": {"confidence": 90, "context_source": "recent_interactions", "reasoning": "Chrome mentioned recently"},
            "alternatives": ["brightness", "volume", "bluetooth"]
        },
        {
            "original": "turn it off",
            "resolved": "turn bluetooth off",
            "context": {"confidence": 85, "context_source": "recent_interactions", "reasoning": "Bluetooth mentioned recently"},
            "alternatives": ["wifi", "chrome"]
        },
        {
            "original": "close it",
            "resolved": "close chrome",
            "context": {"confidence": 95, "context_source": "recent_interactions", "reasoning": "Chrome opened recently"},
            "alternatives": ["safari", "finder"]
        }
    ]
    
    validator = ContextValidator()
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n🧪 Test Case {i}:")
        print(f"   Original: '{case['original']}'")
        print(f"   Resolved: '{case['resolved']}'")
        
        result = validator.validate_context_resolution(
            case["original"],
            case["resolved"], 
            case["context"],
            case["alternatives"]
        )
        
        print(f"   Valid: {result['valid']}")
        print(f"   Final Command: '{result['final_command']}'")
        print(f"   Reasoning: {result['reasoning']}")
        
        if result['needs_clarification']:
            print(f"   Clarification: {result['clarification_question']}")
        
        print(f"   Context Analysis: {result.get('context_analysis', 'N/A')}")
