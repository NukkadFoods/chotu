#!/usr/bin/env python3
"""
🧠 PROMPT COMPLETENESS ANALYZER
===============================
Evaluates if a prompt has enough context to be executed confidently
Uses RAM, ROM, and chat history to assess completeness and identify gaps
"""

import sys
import os
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.gpt_interface import call_gpt_context

class PromptCompletenessAnalyzer:
    """Analyzes prompt completeness and identifies missing context"""
    
    def __init__(self):
        self.confidence_threshold = 75  # Minimum confidence for direct execution
        self.clarification_history = []  # Track previous clarifications
    
    def analyze_prompt_completeness(
        self, 
        user_prompt: str, 
        ram_context: List[Dict], 
        rom_context: List[Dict], 
        chat_history: List[Dict],
        previous_clarifications: List[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze if a prompt has enough context for confident execution
        
        Args:
            user_prompt: The user's input command
            ram_context: Recent memory (last interactions)
            rom_context: Long-term memory (patterns, preferences)
            chat_history: Last 9 conversation turns
            previous_clarifications: Any previous clarification attempts
        
        Returns:
            Dict with completeness analysis and next steps
        """
        
        # Prepare context data for GPT analysis
        context_data = self._prepare_context_data(
            user_prompt, ram_context, rom_context, chat_history, previous_clarifications
        )
        
        # Get GPT analysis of prompt completeness
        completeness_result = self._get_gpt_completeness_analysis(context_data)
        
        # Process the analysis results
        analysis = self._process_completeness_analysis(completeness_result, user_prompt)
        
        return analysis
    
    def _prepare_context_data(
        self, 
        user_prompt: str, 
        ram_context: List[Dict], 
        rom_context: List[Dict], 
        chat_history: List[Dict],
        previous_clarifications: List[str] = None
    ) -> Dict[str, Any]:
        """Prepare structured context data for GPT analysis"""
        
        return {
            "user_prompt": user_prompt,
            "analysis_timestamp": datetime.now().isoformat(),
            "context_sources": {
                "ram_memory": {
                    "description": "Recent interactions and immediate context",
                    "entries": ram_context[-10:] if ram_context else [],  # Last 10 RAM entries
                    "count": len(ram_context) if ram_context else 0
                },
                "rom_memory": {
                    "description": "Long-term patterns, preferences, and learned behaviors",
                    "entries": rom_context[-15:] if rom_context else [],  # Last 15 ROM entries
                    "count": len(rom_context) if rom_context else 0
                },
                "chat_history": {
                    "description": "Last 9 conversation turns for immediate context",
                    "entries": chat_history[-9:] if chat_history else [],
                    "count": len(chat_history) if chat_history else 0
                }
            },
            "clarification_context": {
                "previous_attempts": previous_clarifications if previous_clarifications else [],
                "attempt_count": len(previous_clarifications) if previous_clarifications else 0
            },
            "system_capabilities": {
                "controllable_properties": [
                    "brightness", "volume", "bluetooth", "wifi", "applications"
                ],
                "valid_actions": [
                    "set", "increase", "decrease", "turn on", "turn off", "open", "close"
                ],
                "common_subjects": [
                    "screen brightness", "audio volume", "bluetooth connectivity", 
                    "wifi connection", "chrome browser", "terminal app"
                ]
            }
        }
    
    def _get_gpt_completeness_analysis(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Use GPT to analyze prompt completeness with full context"""
        
        # Pre-analyze context for intelligent pattern detection
        context_intelligence = self._analyze_context_intelligence(context_data)
        
        prompt = f"""
TASK: Analyze prompt completeness and determine if enough context exists for confident execution

USER PROMPT: "{context_data['user_prompt']}"

CONTEXT INTELLIGENCE PRE-ANALYSIS:
=================================
{context_intelligence}

AVAILABLE CONTEXT:
=================

RAM MEMORY (Recent interactions - {context_data['context_sources']['ram_memory']['count']} entries):
{self._format_memory_entries(context_data['context_sources']['ram_memory']['entries'])}

ROM MEMORY (Long-term patterns - {context_data['context_sources']['rom_memory']['count']} entries):
{self._format_memory_entries(context_data['context_sources']['rom_memory']['entries'])}

CHAT HISTORY (Last 9 turns - {context_data['context_sources']['chat_history']['count']} entries):
{self._format_chat_history(context_data['context_sources']['chat_history']['entries'])}

PREVIOUS CLARIFICATIONS ({context_data['clarification_context']['attempt_count']} attempts):
{self._format_clarifications(context_data['clarification_context']['previous_attempts'])}

SYSTEM CAPABILITIES:
- Controllable: {', '.join(context_data['system_capabilities']['controllable_properties'])}
- Actions: {', '.join(context_data['system_capabilities']['valid_actions'])}
- Subjects: {', '.join(context_data['system_capabilities']['common_subjects'])}

INTELLIGENT CONTEXT ANALYSIS RULES:
====================================

CRITICAL: Before asking for clarification, you MUST analyze the available context intelligently:

1. PATTERN RECOGNITION:
   - If user says "chrome" and ROM shows frequent "open chrome" commands → likely wants to OPEN chrome
   - If user says "chrome" and RAM shows "chrome opened" recently → likely wants to CLOSE chrome
   - If user says "it" and last action was brightness → likely refers to brightness
   - If user says "turn it off" and bluetooth was recently mentioned → likely bluetooth

2. STATE AWARENESS:
   - Check current system state from recent interactions
   - If Chrome is open (from RAM) and user says "chrome" → probably wants to close it
   - If Chrome is closed and user says "chrome" → probably wants to open it
   - Consider safety implications (closing apps may lose data)

3. CONTEXT INTELLIGENCE SCORING:
   - HIGH INTELLIGENCE (80-100%): Clear patterns, recent context, obvious intent
   - MEDIUM INTELLIGENCE (50-79%): Some patterns, partial context, educated guess possible
   - LOW INTELLIGENCE (0-49%): No clear patterns, need clarification

4. INTELLIGENT SUGGESTIONS:
   - Instead of generic "what do you want?", provide SPECIFIC suggestions based on context
   - Example: "Chrome is currently open. Do you want to: 1) Close Chrome 2) Open new tab 3) Something else?"
   - Include safety warnings when appropriate

5. SAFETY CONSIDERATIONS:
   - Warn about potential data loss (closing browser with unsaved content)
   - Confirm destructive actions
   - Suggest safer alternatives

ANALYSIS REQUIREMENTS:
======================

1. COMPLETENESS CONFIDENCE (0-100%):
   - 90-100%: Crystal clear, can execute immediately
   - 75-89%: Good understanding, minor assumptions acceptable  
   - 50-74%: Partial understanding, but can make educated guess with confirmation
   - 25-49%: Significant gaps, need specific clarification with intelligent suggestions
   - 0-24%: Insufficient context, need comprehensive clarification

2. CONTEXT INTELLIGENCE USAGE:
   - MUST use the pre-analysis intelligence data provided above
   - Factor in patterns, current state, and user behavior
   - Make intelligent inferences before asking for clarification

3. SMART CLARIFICATION:
   - Never ask generic questions like "what do you want?"
   - Always provide specific options based on context analysis
   - Include current state information in questions
   - Suggest most likely actions based on patterns

ANALYSIS RULES:
===============
- Consider ambiguous pronouns (it, this, that) as requiring context
- Look for missing subjects when actions are clear
- Look for missing actions when subjects are clear
- Factor in recent context patterns from RAM/ROM
- Consider user's typical interaction style from history
- Account for previous clarification attempts (don't repeat)
- Evaluate if system capabilities can fulfill the request

Return structured JSON analysis:
{{
    "completeness_confidence": <0-100 integer>,
    "execution_ready": <true/false>,
    "confidence_category": "<crystal_clear|good_understanding|partial_understanding|significant_gaps|insufficient_context>",
    "analysis": {{
        "prompt_elements": {{
            "action_identified": <true/false>,
            "subject_identified": <true/false>,
            "parameters_clear": <true/false>,
            "context_sufficient": <true/false>
        }},
        "missing_context": [
            "specific missing information item 1",
            "specific missing information item 2"
        ],
        "context_sources_used": {{
            "ram_helpful": <true/false>,
            "rom_helpful": <true/false>,
            "chat_helpful": <true/false>
        }},
        "assumptions_required": [
            "assumption 1 if executed without clarification",
            "assumption 2 if executed without clarification"
        ]
    }},
    "execution_plan": {{
        "recommended_action": "<execute_directly|request_clarification|gather_more_context>",
        "risk_level": "<low|medium|high>",
        "potential_command": "<likely command if executed>",
        "alternative_interpretations": [
            "possible interpretation 1",
            "possible interpretation 2"
        ]
    }},
    "clarification": {{
        "needed": <true/false>,
        "question": "<INTELLIGENT clarification question based on context analysis above>",
        "options": [
            "Most likely option based on patterns",
            "Second most likely option", 
            "Alternative option"
        ],
        "safety_warning": "<any safety considerations to mention>",
        "follow_up_strategy": "<how to handle response>",
        "context_to_gather": ["specific context item 1", "specific context item 2"]
    }},
    "reasoning": "<detailed explanation of analysis process, including how context intelligence was used>"
}}

Analyze now:"""
        
        try:
            response = call_gpt_context(prompt)
            
            # Clean and parse the JSON response
            response = response.strip()
            if response.startswith('```json'):
                response = response[7:]
            if response.endswith('```'):
                response = response[:-3]
            
            import json
            analysis = json.loads(response.strip())
            return analysis
            
        except Exception as e:
            print(f"❌ GPT completeness analysis failed: {e}")
            return self._fallback_analysis(context_data['user_prompt'])
    
    def _analyze_context_intelligence(self, context_data: Dict[str, Any]) -> str:
        """Pre-analyze context to provide intelligent insights for GPT"""
        
        user_prompt = context_data['user_prompt'].lower()
        ram_entries = context_data['context_sources']['ram_memory']['entries']
        rom_entries = context_data['context_sources']['rom_memory']['entries']
        chat_entries = context_data['context_sources']['chat_history']['entries']
        
        intelligence = []
        
        # Analyze for specific applications/subjects
        if 'chrome' in user_prompt:
            chrome_analysis = self._analyze_application_context('chrome', ram_entries, rom_entries)
            intelligence.append(f"CHROME ANALYSIS: {chrome_analysis}")
        
        if 'bluetooth' in user_prompt:
            bluetooth_analysis = self._analyze_system_feature_context('bluetooth', ram_entries, rom_entries)
            intelligence.append(f"BLUETOOTH ANALYSIS: {bluetooth_analysis}")
        
        if 'brightness' in user_prompt:
            brightness_analysis = self._analyze_system_feature_context('brightness', ram_entries, rom_entries)
            intelligence.append(f"BRIGHTNESS ANALYSIS: {brightness_analysis}")
        
        # Analyze pronouns with context
        if user_prompt.strip() in ['it', 'this', 'that']:
            pronoun_analysis = self._analyze_pronoun_context(ram_entries, chat_entries)
            intelligence.append(f"PRONOUN ANALYSIS: {pronoun_analysis}")
        
        # Analyze action patterns
        action_analysis = self._analyze_action_patterns(user_prompt, rom_entries)
        intelligence.append(f"ACTION PATTERNS: {action_analysis}")
        
        # Analyze current system state
        state_analysis = self._analyze_current_state(ram_entries)
        intelligence.append(f"CURRENT STATE: {state_analysis}")
        
        # Safety considerations
        safety_analysis = self._analyze_safety_implications(user_prompt, ram_entries)
        if safety_analysis:
            intelligence.append(f"SAFETY CONSIDERATIONS: {safety_analysis}")
        
        return "\n".join(intelligence) if intelligence else "No specific intelligence patterns detected."
    
    def _analyze_application_context(self, app_name: str, ram_entries: List[Dict], rom_entries: List[Dict]) -> str:
        """Analyze context for specific applications like Chrome"""
        
        # Check recent state from RAM
        recent_app_interactions = []
        for entry in ram_entries[-5:]:  # Last 5 interactions
            user_input = entry.get('user_input', '').lower()
            response = entry.get('response', '').lower()
            if app_name in user_input or app_name in response:
                recent_app_interactions.append({
                    'input': user_input,
                    'response': response,
                    'timestamp': entry.get('timestamp', 'unknown')
                })
        
        # Check patterns from ROM
        app_patterns = []
        for entry in rom_entries:
            pattern = entry.get('pattern', '').lower()
            if app_name in pattern:
                app_patterns.append({
                    'pattern': pattern,
                    'frequency': entry.get('frequency', 0)
                })
        
        # Determine current state and likely intent
        is_open = any('opened' in interaction['response'] for interaction in recent_app_interactions)
        is_closed = any('closed' in interaction['response'] for interaction in recent_app_interactions)
        
        common_actions = [p['pattern'] for p in sorted(app_patterns, key=lambda x: x['frequency'], reverse=True)[:3]]
        
        analysis = f"Recent: {len(recent_app_interactions)} interactions. "
        
        if is_open and not is_closed:
            analysis += f"{app_name.title()} appears to be OPEN. User likely wants to CLOSE it or perform action within it. "
        elif is_closed or not recent_app_interactions:
            analysis += f"{app_name.title()} appears to be CLOSED. User likely wants to OPEN it. "
        
        if common_actions:
            analysis += f"Common actions: {', '.join(common_actions[:2])}. "
        
        return analysis
    
    def _analyze_system_feature_context(self, feature: str, ram_entries: List[Dict], rom_entries: List[Dict]) -> str:
        """Analyze context for system features like bluetooth, brightness"""
        
        recent_values = []
        for entry in ram_entries[-3:]:
            user_input = entry.get('user_input', '').lower()
            if feature in user_input:
                recent_values.append(user_input)
        
        feature_patterns = [entry.get('pattern', '') for entry in rom_entries if feature in entry.get('pattern', '').lower()]
        
        analysis = f"Recent {feature} interactions: {len(recent_values)}. "
        
        if recent_values:
            latest_interaction = recent_values[-1]
            if 'set' in latest_interaction or 'increase' in latest_interaction or 'decrease' in latest_interaction:
                analysis += f"Last action: '{latest_interaction}'. User may want to adjust further. "
        
        if feature_patterns:
            analysis += f"User frequently controls {feature}. "
        
        return analysis
    
    def _analyze_pronoun_context(self, ram_entries: List[Dict], chat_entries: List[Dict]) -> str:
        """Analyze what pronouns like 'it', 'this', 'that' might refer to"""
        
        # Look at the most recent interactions for subjects
        recent_subjects = []
        
        # Check RAM for recent subjects
        for entry in ram_entries[-3:]:
            user_input = entry.get('user_input', '').lower()
            for subject in ['brightness', 'volume', 'chrome', 'bluetooth', 'wifi']:
                if subject in user_input:
                    recent_subjects.append(subject)
        
        # Check chat history
        for entry in chat_entries[-3:]:
            content = entry.get('content', '').lower()
            for subject in ['brightness', 'volume', 'chrome', 'bluetooth', 'wifi']:
                if subject in content:
                    recent_subjects.append(subject)
        
        if recent_subjects:
            most_recent = recent_subjects[-1]
            return f"Most likely refers to '{most_recent}' (mentioned in recent context). Other possibilities: {list(set(recent_subjects))}."
        
        return "No clear referent found in recent context. Need clarification."
    
    def _analyze_action_patterns(self, user_prompt: str, rom_entries: List[Dict]) -> str:
        """Analyze user's typical action patterns"""
        
        # Extract potential action from prompt
        actions = ['open', 'close', 'set', 'increase', 'decrease', 'turn on', 'turn off', 'enable', 'disable']
        detected_actions = [action for action in actions if action in user_prompt.lower()]
        
        if not detected_actions:
            # Look for partial actions
            if user_prompt.strip().lower() in ['chrome', 'bluetooth', 'brightness', 'volume']:
                # Single word - look at ROM patterns
                word = user_prompt.strip().lower()
                related_patterns = []
                for entry in rom_entries:
                    pattern = entry.get('pattern', '').lower()
                    if word in pattern:
                        related_patterns.append({
                            'pattern': pattern,
                            'frequency': entry.get('frequency', 0)
                        })
                
                if related_patterns:
                    most_common = sorted(related_patterns, key=lambda x: x['frequency'], reverse=True)[0]
                    return f"Single word '{word}' detected. Most common pattern: '{most_common['pattern']}' (used {most_common['frequency']} times)."
        
        return f"Detected actions: {detected_actions}" if detected_actions else "No clear action detected."
    
    def _analyze_current_state(self, ram_entries: List[Dict]) -> str:
        """Analyze current system state from recent interactions"""
        
        state_indicators = {
            'chrome': 'unknown',
            'bluetooth': 'unknown', 
            'wifi': 'unknown',
            'brightness': 'unknown',
            'volume': 'unknown'
        }
        
        for entry in ram_entries[-5:]:
            response = entry.get('response', '').lower()
            
            if 'chrome opened' in response:
                state_indicators['chrome'] = 'open'
            elif 'chrome closed' in response:
                state_indicators['chrome'] = 'closed'
                
            if 'bluetooth enabled' in response:
                state_indicators['bluetooth'] = 'on'
            elif 'bluetooth disabled' in response:
                state_indicators['bluetooth'] = 'off'
                
            if 'brightness set' in response:
                # Try to extract value
                import re
                match = re.search(r'brightness set to (\d+)', response)
                if match:
                    state_indicators['brightness'] = f"{match.group(1)}%"
        
        known_states = {k: v for k, v in state_indicators.items() if v != 'unknown'}
        
        if known_states:
            return f"Known states: {known_states}"
        
        return "No clear current state information available."
    
    def _analyze_safety_implications(self, user_prompt: str, ram_entries: List[Dict]) -> str:
        """Analyze potential safety implications of the command"""
        
        safety_concerns = []
        
        # Check for potentially destructive actions
        if 'close' in user_prompt.lower() and 'chrome' in user_prompt.lower():
            safety_concerns.append("Closing Chrome may result in loss of unsaved work or open tabs.")
        
        if 'turn off' in user_prompt.lower():
            if 'wifi' in user_prompt.lower():
                safety_concerns.append("Turning off WiFi will disconnect from internet.")
            elif 'bluetooth' in user_prompt.lower():
                safety_concerns.append("Turning off Bluetooth will disconnect connected devices.")
        
        # Check if there are recent unsaved actions
        recent_commands = [entry.get('user_input', '') for entry in ram_entries[-3:]]
        if any('open' in cmd for cmd in recent_commands) and 'close' in user_prompt.lower():
            safety_concerns.append("Recently opened applications may have unsaved content.")
        
        return ". ".join(safety_concerns) if safety_concerns else ""

    def _format_memory_entries(self, entries: List[Dict]) -> str:
        """Format memory entries for GPT prompt"""
        if not entries:
            return "No entries available"
        
        formatted = []
        for i, entry in enumerate(entries[-10:], 1):  # Show last 10
            user_input = entry.get('user_input', 'Unknown')
            response = entry.get('response', 'Unknown')
            timestamp = entry.get('timestamp', 'Unknown')
            formatted.append(f"   {i}. [{timestamp}] User: '{user_input}' → Response: '{response[:50]}...'")
        
        return "\n".join(formatted)
    
    def _format_chat_history(self, entries: List[Dict]) -> str:
        """Format chat history for GPT prompt"""
        if not entries:
            return "No chat history available"
        
        formatted = []
        for i, entry in enumerate(entries, 1):
            role = entry.get('role', 'unknown')
            content = entry.get('content', 'Unknown')
            formatted.append(f"   {i}. {role.title()}: '{content[:60]}...'")
        
        return "\n".join(formatted)
    
    def _format_clarifications(self, clarifications: List[str]) -> str:
        """Format previous clarifications for GPT prompt"""
        if not clarifications:
            return "No previous clarifications"
        
        formatted = []
        for i, clarification in enumerate(clarifications, 1):
            formatted.append(f"   {i}. '{clarification}'")
        
        return "\n".join(formatted)
    
    def _process_completeness_analysis(self, gpt_analysis: Dict[str, Any], user_prompt: str) -> Dict[str, Any]:
        """Process GPT analysis and add additional metadata"""
        
        # Add processing metadata
        gpt_analysis['processing_metadata'] = {
            'analyzer_version': '1.0',
            'analysis_timestamp': datetime.now().isoformat(),
            'original_prompt': user_prompt,
            'confidence_threshold': self.confidence_threshold
        }
        
        # Determine next action based on confidence
        confidence = gpt_analysis.get('completeness_confidence', 0)
        
        if confidence >= self.confidence_threshold:
            gpt_analysis['next_action'] = 'proceed_to_execution'
            gpt_analysis['action_reason'] = f"Confidence {confidence}% meets threshold {self.confidence_threshold}%"
        else:
            gpt_analysis['next_action'] = 'request_clarification'
            gpt_analysis['action_reason'] = f"Confidence {confidence}% below threshold {self.confidence_threshold}%"
        
        # Add gap analysis
        gpt_analysis['gap_analysis'] = self._analyze_context_gaps(gpt_analysis)
        
        return gpt_analysis
    
    def _analyze_context_gaps(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze what specific context gaps exist"""
        
        gaps = {
            'critical_gaps': [],
            'minor_gaps': [],
            'context_sources_needed': [],
            'user_input_needed': []
        }
        
        # Analyze missing elements
        elements = analysis.get('analysis', {}).get('prompt_elements', {})
        
        if not elements.get('action_identified', False):
            gaps['critical_gaps'].append('Action/verb not clearly identified')
            gaps['user_input_needed'].append('What action do you want to perform?')
        
        if not elements.get('subject_identified', False):
            gaps['critical_gaps'].append('Subject/target not clearly identified')
            gaps['context_sources_needed'].append('RAM/ROM context for subject resolution')
            gaps['user_input_needed'].append('What device/setting do you want to control?')
        
        if not elements.get('parameters_clear', False):
            gaps['minor_gaps'].append('Parameters or values not specified')
            gaps['user_input_needed'].append('What specific value or level?')
        
        return gaps
    
    def _fallback_analysis(self, user_prompt: str) -> Dict[str, Any]:
        """Fallback analysis when GPT fails"""
        return {
            'completeness_confidence': 25,
            'execution_ready': False,
            'confidence_category': 'significant_gaps',
            'analysis': {
                'prompt_elements': {
                    'action_identified': False,
                    'subject_identified': False,
                    'parameters_clear': False,
                    'context_sufficient': False
                },
                'missing_context': ['GPT analysis failed - manual review needed'],
                'assumptions_required': ['Cannot determine without proper analysis']
            },
            'execution_plan': {
                'recommended_action': 'request_clarification',
                'risk_level': 'high',
                'potential_command': 'UNKNOWN',
                'alternative_interpretations': []
            },
            'clarification': {
                'needed': True,
                'question': 'Could you please provide more specific details about what you want me to do?',
                'follow_up_strategy': 'manual_analysis',
                'context_to_gather': ['action', 'subject', 'parameters']
            },
            'reasoning': 'Fallback analysis due to GPT processing failure',
            'processing_metadata': {
                'analyzer_version': '1.0',
                'analysis_timestamp': datetime.now().isoformat(),
                'original_prompt': user_prompt,
                'error': 'GPT analysis failed'
            },
            'next_action': 'request_clarification',
            'action_reason': 'Analysis system error - requiring manual clarification'
        }
    
    def iterative_clarification_cycle(
        self,
        initial_prompt: str,
        ram_context: List[Dict],
        rom_context: List[Dict], 
        chat_history: List[Dict],
        max_iterations: int = 3
    ) -> Dict[str, Any]:
        """
        Run iterative clarification cycle until confidence threshold is met
        
        Args:
            initial_prompt: The original user prompt
            ram_context: RAM memory
            rom_context: ROM memory  
            chat_history: Recent chat history
            max_iterations: Maximum clarification attempts
            
        Returns:
            Final analysis with all clarification attempts
        """
        
        clarification_attempts = []
        current_prompt = initial_prompt
        
        for iteration in range(max_iterations):
            print(f"\n🔄 ITERATION {iteration + 1}/{max_iterations}")
            
            # Analyze current prompt completeness
            analysis = self.analyze_prompt_completeness(
                current_prompt,
                ram_context,
                rom_context,
                chat_history,
                clarification_attempts
            )
            
            confidence = analysis.get('completeness_confidence', 0)
            print(f"   Confidence: {confidence}%")
            
            # Check if we have enough confidence to proceed
            if confidence >= self.confidence_threshold:
                print(f"   ✅ Confidence threshold met! Ready to execute.")
                analysis['clarification_cycle'] = {
                    'iterations': iteration + 1,
                    'final_confidence': confidence,
                    'clarification_history': clarification_attempts,
                    'status': 'completed_successfully'
                }
                return analysis
            
            # Get clarification question
            clarification_question = analysis.get('clarification', {}).get('question', 
                'Could you provide more details?')
            
            print(f"   🤔 Need clarification: {clarification_question}")
            clarification_attempts.append(clarification_question)
            
            # In a real system, this would wait for user response
            # For testing, we'll simulate or break
            print(f"   ⏸️  Waiting for user clarification...")
            break
        
        # Max iterations reached without sufficient confidence
        analysis['clarification_cycle'] = {
            'iterations': max_iterations,
            'final_confidence': analysis.get('completeness_confidence', 0),
            'clarification_history': clarification_attempts,
            'status': 'max_iterations_reached'
        }
        
        return analysis

def test_completeness_analyzer():
    """Test the prompt completeness analyzer"""
    
    print("🧪 TESTING PROMPT COMPLETENESS ANALYZER")
    print("="*50)
    
    analyzer = PromptCompletenessAnalyzer()
    
    # Sample context data
    ram_context = [
        {"user_input": "set brightness to 80%", "response": "Brightness set to 80%", "timestamp": "2025-08-12T10:00:00"},
        {"user_input": "open chrome", "response": "Chrome opened", "timestamp": "2025-08-12T10:01:00"},
        {"user_input": "turn on bluetooth", "response": "Bluetooth enabled", "timestamp": "2025-08-12T10:02:00"}
    ]
    
    rom_context = [
        {"pattern": "user prefers brightness adjustments", "frequency": 15, "last_used": "2025-08-12"},
        {"pattern": "chrome is frequently opened", "frequency": 25, "last_used": "2025-08-12"}
    ]
    
    chat_history = [
        {"role": "user", "content": "set brightness to 80%"},
        {"role": "assistant", "content": "I'll set the brightness to 80%"},
        {"role": "user", "content": "open chrome browser"},
        {"role": "assistant", "content": "Opening Chrome browser"}
    ]
    
    # Test cases with different completeness levels
    test_prompts = [
        ("set brightness to 50%", "Complete command"),
        ("increase it", "Ambiguous pronoun"),
        ("turn it off", "Ambiguous pronoun + action"),
        ("make it brighter", "Ambiguous with context clue"),
        ("it", "Extremely ambiguous"),
        ("open", "Missing subject"),
        ("chrome", "Missing action")
    ]
    
    for prompt, description in test_prompts:
        print(f"\n📝 TESTING: '{prompt}' ({description})")
        print("-" * 40)
        
        analysis = analyzer.analyze_prompt_completeness(
            prompt, ram_context, rom_context, chat_history
        )
        
        print(f"Confidence: {analysis['completeness_confidence']}%")
        print(f"Category: {analysis['confidence_category']}")
        print(f"Ready: {analysis['execution_ready']}")
        print(f"Action: {analysis['next_action']}")
        
        if analysis['clarification']['needed']:
            print(f"Question: {analysis['clarification']['question']}")

if __name__ == "__main__":
    test_completeness_analyzer()
