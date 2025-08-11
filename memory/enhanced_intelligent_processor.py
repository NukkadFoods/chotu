#!/usr/bin/env python3
"""
🎯 ENHANCED INTELLIGENT COMMAND PROCESSOR
==========================================
Complete command processing pipeline with:
1. Prompt completeness analysis
2. Iterative clarification 
3. Context-aware execution
4. Confidence-based decision making
"""

import sys
import os
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

# Add parent directory for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory.prompt_completeness_analyzer import PromptCompletenessAnalyzer
from memory.intelligent_context_resolver import resolve_ambiguous_command
from memory.context_validator import validate_context_resolution
from memory.context_manager import ContextManager

class EnhancedIntelligentProcessor:
    """Complete intelligent command processing with completeness analysis"""
    
    def __init__(self):
        self.completeness_analyzer = PromptCompletenessAnalyzer()
        self.context_manager = ContextManager()
        self.confidence_threshold = 75
        self.max_clarification_attempts = 3
        self.processing_history = []
    
    def process_command_with_completeness(self, user_input: str) -> Dict[str, Any]:
        """
        Complete command processing pipeline with completeness analysis
        
        Args:
            user_input: User's command/request
            
        Returns:
            Dict containing full processing results and actions
        """
        
        print(f"\n🎯 PROCESSING: '{user_input}'")
        print("="*60)
        
        # Step 1: Get current context (RAM, ROM, Chat History)
        context_data = self._gather_current_context()
        
        # Step 2: Analyze prompt completeness
        print("📊 STEP 1: Analyzing Prompt Completeness...")
        completeness_analysis = self.completeness_analyzer.analyze_prompt_completeness(
            user_input,
            context_data['ram_context'],
            context_data['rom_context'], 
            context_data['chat_history']
        )
        
        self._display_completeness_results(completeness_analysis)
        
        # Step 3: Decision based on completeness confidence
        if completeness_analysis['completeness_confidence'] >= self.confidence_threshold:
            # High confidence - proceed to execution
            return self._proceed_to_execution(user_input, completeness_analysis, context_data)
        else:
            # Low confidence - start clarification cycle
            return self._start_clarification_cycle(user_input, completeness_analysis, context_data)
    
    def _gather_current_context(self) -> Dict[str, Any]:
        """Gather current RAM, ROM, and chat history context"""
        
        # Get RAM context (recent interactions)
        ram_interactions = []
        if hasattr(self.context_manager, 'get_recent_interactions'):
            ram_interactions = self.context_manager.get_recent_interactions(limit=10)
        
        # Get ROM context (patterns and preferences)  
        rom_patterns = []
        if hasattr(self.context_manager, 'get_patterns'):
            rom_patterns = self.context_manager.get_patterns(limit=15)
        
        # Get chat history (last 9 turns)
        chat_history = []
        if hasattr(self.context_manager, 'get_chat_history'):
            chat_history = self.context_manager.get_chat_history(limit=9)
        
        return {
            'ram_context': ram_interactions,
            'rom_context': rom_patterns,
            'chat_history': chat_history,
            'context_timestamp': datetime.now().isoformat()
        }
    
    def _display_completeness_results(self, analysis: Dict[str, Any]) -> None:
        """Display completeness analysis results"""
        
        confidence = analysis['completeness_confidence']
        category = analysis['confidence_category']
        ready = analysis['execution_ready']
        
        print(f"   🎯 Confidence: {confidence}% ({category})")
        print(f"   🚦 Execution Ready: {'✅ YES' if ready else '❌ NO'}")
        
        # Show what's identified vs missing
        elements = analysis.get('analysis', {}).get('prompt_elements', {})
        print(f"   🔍 Analysis:")
        print(f"      Action: {'✅' if elements.get('action_identified') else '❌'}")
        print(f"      Subject: {'✅' if elements.get('subject_identified') else '❌'}")
        print(f"      Parameters: {'✅' if elements.get('parameters_clear') else '❌'}")
        print(f"      Context: {'✅' if elements.get('context_sufficient') else '❌'}")
        
        # Show missing context if any
        missing = analysis.get('analysis', {}).get('missing_context', [])
        if missing:
            print(f"   ❓ Missing: {', '.join(missing)}")
    
    def _proceed_to_execution(
        self, 
        user_input: str, 
        completeness_analysis: Dict[str, Any], 
        context_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Proceed with high-confidence command execution"""
        
        print(f"\n🚀 STEP 2: Proceeding to Execution (High Confidence)")
        
        # Use existing context resolution system
        print("   🧠 Resolving context...")
        context_result = resolve_ambiguous_command(user_input)
        
        print(f"   🎯 Resolved: '{context_result['resolved_command']}'")
        print(f"   🎲 Confidence: {context_result['confidence']}%")
        
        # Validate the resolution
        print("   🤖 Validating with GPT...")
        validation_result = validate_context_resolution(
            user_input,
            context_result['resolved_command'],
            context_result,
            context_result['alternatives']
        )
        
        print(f"   ✅ Valid: {'YES' if validation_result['valid'] else 'NO'}")
        
        # Final execution decision
        final_result = {
            'status': 'executed',
            'original_input': user_input,
            'completeness_analysis': completeness_analysis,
            'context_resolution': context_result,
            'validation_result': validation_result,
            'final_command': validation_result['final_command'],
            'execution_confidence': min(
                completeness_analysis['completeness_confidence'],
                context_result['confidence']
            ),
            'processing_path': 'direct_execution',
            'timestamp': datetime.now().isoformat()
        }
        
        if validation_result['valid']:
            print(f"   🎯 EXECUTING: '{validation_result['final_command']}'")
            final_result['chotu_response'] = f"I understand you want to {validation_result['final_command']}"
        else:
            print(f"   🤔 SUGGESTING: '{validation_result.get('suggested_action', 'clarification needed')}'")
            final_result['chotu_response'] = validation_result.get('clarification_question', 
                'I need more information to proceed')
        
        # Save to processing history
        self.processing_history.append(final_result)
        
        return final_result
    
    def _start_clarification_cycle(
        self, 
        user_input: str, 
        completeness_analysis: Dict[str, Any], 
        context_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Start iterative clarification cycle for low-confidence commands"""
        
        print(f"\n🤔 STEP 2: Starting Clarification Cycle (Low Confidence)")
        
        # Run iterative clarification
        clarification_result = self.completeness_analyzer.iterative_clarification_cycle(
            user_input,
            context_data['ram_context'],
            context_data['rom_context'],
            context_data['chat_history'],
            self.max_clarification_attempts
        )
        
        # Prepare clarification response
        clarification_question = clarification_result.get('clarification', {}).get('question', 
            'Could you provide more specific details about what you want me to do?')
        
        print(f"   ❓ ASKING: '{clarification_question}'")
        
        final_result = {
            'status': 'needs_clarification',
            'original_input': user_input,
            'completeness_analysis': completeness_analysis,
            'clarification_analysis': clarification_result,
            'clarification_question': clarification_question,
            'processing_path': 'clarification_cycle',
            'chotu_response': clarification_question,
            'timestamp': datetime.now().isoformat(),
            'next_steps': self._generate_next_steps(clarification_result)
        }
        
        # Save to processing history
        self.processing_history.append(final_result)
        
        return final_result
    
    def _generate_next_steps(self, clarification_result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate next steps based on clarification analysis"""
        
        missing_context = clarification_result.get('analysis', {}).get('missing_context', [])
        gap_analysis = clarification_result.get('gap_analysis', {})
        
        return {
            'user_should_provide': gap_analysis.get('user_input_needed', []),
            'system_should_check': gap_analysis.get('context_sources_needed', []),
            'critical_gaps': gap_analysis.get('critical_gaps', []),
            'follow_up_strategy': clarification_result.get('clarification', {}).get('follow_up_strategy', 'manual_analysis')
        }
    
    def handle_clarification_response(
        self, 
        original_request_id: str, 
        user_response: str
    ) -> Dict[str, Any]:
        """Handle user's response to clarification question"""
        
        print(f"\n🔄 HANDLING CLARIFICATION RESPONSE: '{user_response}'")
        
        # Find original request in history
        original_request = None
        for request in self.processing_history:
            if request.get('timestamp') == original_request_id:
                original_request = request
                break
        
        if not original_request:
            return {
                'status': 'error',
                'error': 'Original request not found in history',
                'chotu_response': 'Sorry, I lost track of your original request. Could you please start over?'
            }
        
        # Combine original input with clarification response
        combined_input = f"{original_request['original_input']} {user_response}"
        
        # Re-process with additional context
        return self.process_command_with_completeness(combined_input)
    
    def get_processing_summary(self) -> Dict[str, Any]:
        """Get summary of recent processing activities"""
        
        total_requests = len(self.processing_history)
        direct_executions = len([r for r in self.processing_history if r['processing_path'] == 'direct_execution'])
        clarifications = len([r for r in self.processing_history if r['processing_path'] == 'clarification_cycle'])
        
        return {
            'total_requests': total_requests,
            'direct_executions': direct_executions,
            'clarification_cycles': clarifications,
            'success_rate': (direct_executions / total_requests * 100) if total_requests > 0 else 0,
            'recent_requests': self.processing_history[-5:] if self.processing_history else []
        }

def test_enhanced_processor():
    """Test the enhanced intelligent processor"""
    
    print("🧪 TESTING ENHANCED INTELLIGENT PROCESSOR")
    print("="*60)
    
    processor = EnhancedIntelligentProcessor()
    
    # Test commands with different completeness levels
    test_commands = [
        ("set brightness to 75%", "Complete command"),
        ("increase it", "Ambiguous pronoun"),
        ("turn it off", "Ambiguous pronoun + action"),
        ("make it louder", "Ambiguous with context clue"),
        ("it", "Extremely ambiguous"),
        ("chrome", "Missing action"),
        ("turn up", "Missing subject")
    ]
    
    for command, description in test_commands:
        print(f"\n{'='*60}")
        print(f"TEST CASE: '{command}' ({description})")
        print('='*60)
        
        result = processor.process_command_with_completeness(command)
        
        print(f"\n📊 FINAL RESULT:")
        print(f"   Status: {result['status']}")
        print(f"   Path: {result['processing_path']}")
        print(f"   Response: '{result['chotu_response']}'")
        
        if result['status'] == 'executed':
            print(f"   Final Command: '{result['final_command']}'")
            print(f"   Execution Confidence: {result['execution_confidence']}%")
        elif result['status'] == 'needs_clarification':
            print(f"   Clarification: '{result['clarification_question']}'")
            next_steps = result.get('next_steps', {})
            if next_steps.get('user_should_provide'):
                print(f"   User Should Provide: {next_steps['user_should_provide']}")

    # Show processing summary
    print(f"\n📈 PROCESSING SUMMARY:")
    summary = processor.get_processing_summary()
    print(f"   Total Requests: {summary['total_requests']}")
    print(f"   Direct Executions: {summary['direct_executions']}")
    print(f"   Clarification Cycles: {summary['clarification_cycles']}")
    print(f"   Success Rate: {summary['success_rate']:.1f}%")

if __name__ == "__main__":
    test_enhanced_processor()
