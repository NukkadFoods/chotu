#!/usr/bin/env python3
"""
🚀 CHOTU ENHANCED WITH COMPLETENESS ANALYSIS
=============================================
Main Chotu system enhanced with prompt completeness evaluation,
iterative clarification, and confidence-based decision making
"""

import sys
import os
from typing import Dict, List, Any, Optional
from datetime import datetime

# Add parent directories for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory.enhanced_intelligent_processor import EnhancedIntelligentProcessor
from memory.context_manager import ContextManager
from utils.gpt_interface import call_gpt_system

class ChoutuEnhanced:
    """Enhanced Chotu with completeness analysis and iterative clarification"""
    
    def __init__(self):
        self.processor = EnhancedIntelligentProcessor()
        self.context_manager = ContextManager()
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.conversation_state = {
            'active_clarifications': {},
            'conversation_history': [],
            'user_preferences': {},
            'session_stats': {
                'total_commands': 0,
                'successful_executions': 0,
                'clarifications_needed': 0,
                'avg_confidence': 0
            }
        }
    
    def process_user_input(self, user_input: str) -> Dict[str, Any]:
        """
        Main entry point for processing user input with full completeness analysis
        
        Args:
            user_input: User's command or response
            
        Returns:
            Dict containing response and processing details
        """
        
        self.conversation_state['session_stats']['total_commands'] += 1
        
        print(f"\n🤖 CHOTU ENHANCED - Processing: '{user_input}'")
        print("="*70)
        
        # Check if this is a response to an active clarification
        clarification_response = self._check_for_clarification_response(user_input)
        if clarification_response:
            return clarification_response
        
        # Process new command with completeness analysis
        processing_result = self.processor.process_command_with_completeness(user_input)
        
        # Update conversation state
        self._update_conversation_state(user_input, processing_result)
        
        # Generate appropriate response
        response = self._generate_response(processing_result)
        
        # Add to conversation history
        self.conversation_state['conversation_history'].append({
            'user_input': user_input,
            'chotu_response': response['message'],
            'processing_result': processing_result,
            'timestamp': datetime.now().isoformat()
        })
        
        return response
    
    def _check_for_clarification_response(self, user_input: str) -> Optional[Dict[str, Any]]:
        """Check if user input is responding to an active clarification"""
        
        if not self.conversation_state['active_clarifications']:
            return None
        
        # Get the most recent clarification
        recent_clarification = list(self.conversation_state['active_clarifications'].values())[-1]
        
        print("🔄 HANDLING CLARIFICATION RESPONSE")
        
        # Process the clarification response
        response_result = self.processor.handle_clarification_response(
            recent_clarification['request_id'],
            user_input
        )
        
        # Remove from active clarifications
        self.conversation_state['active_clarifications'].clear()
        
        # Update stats
        if response_result['status'] == 'executed':
            self.conversation_state['session_stats']['successful_executions'] += 1
        
        return self._generate_response(response_result)
    
    def _update_conversation_state(self, user_input: str, processing_result: Dict[str, Any]) -> None:
        """Update conversation state based on processing results"""
        
        # Update session statistics
        if processing_result['status'] == 'executed':
            self.conversation_state['session_stats']['successful_executions'] += 1
        elif processing_result['status'] == 'needs_clarification':
            self.conversation_state['session_stats']['clarifications_needed'] += 1
            
            # Add to active clarifications
            clarification_id = f"clarify_{len(self.conversation_state['active_clarifications']) + 1}"
            self.conversation_state['active_clarifications'][clarification_id] = {
                'original_input': user_input,
                'clarification_question': processing_result['clarification_question'],
                'request_id': processing_result['timestamp'],
                'created_at': datetime.now().isoformat()
            }
        
        # Update average confidence
        if processing_result.get('execution_confidence'):
            current_avg = self.conversation_state['session_stats']['avg_confidence']
            total_commands = self.conversation_state['session_stats']['total_commands']
            new_confidence = processing_result['execution_confidence']
            
            self.conversation_state['session_stats']['avg_confidence'] = (
                (current_avg * (total_commands - 1) + new_confidence) / total_commands
            )
        
        # Learn user preferences from successful interactions
        if processing_result['status'] == 'executed':
            self._learn_user_preferences(user_input, processing_result)
    
    def _learn_user_preferences(self, user_input: str, processing_result: Dict[str, Any]) -> None:
        """Learn and store user preferences from successful interactions"""
        
        final_command = processing_result.get('final_command', '')
        
        # Extract patterns
        if 'brightness' in final_command.lower():
            self.conversation_state['user_preferences']['brightness_control'] = {
                'last_used': datetime.now().isoformat(),
                'frequency': self.conversation_state['user_preferences'].get('brightness_control', {}).get('frequency', 0) + 1
            }
        
        if 'volume' in final_command.lower():
            self.conversation_state['user_preferences']['volume_control'] = {
                'last_used': datetime.now().isoformat(),
                'frequency': self.conversation_state['user_preferences'].get('volume_control', {}).get('frequency', 0) + 1
            }
        
        # Add to context manager for future reference
        self.context_manager.add_interaction(user_input, processing_result['chotu_response'], True)
    
    def _generate_response(self, processing_result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate appropriate response based on processing results"""
        
        base_response = {
            'message': processing_result['chotu_response'],
            'status': processing_result['status'],
            'confidence': processing_result.get('execution_confidence', 0),
            'processing_path': processing_result.get('processing_path', 'unknown'),
            'timestamp': datetime.now().isoformat()
        }
        
        if processing_result['status'] == 'executed':
            base_response.update({
                'action_taken': processing_result.get('final_command', 'Unknown'),
                'execution_details': {
                    'original_input': processing_result['original_input'],
                    'resolved_command': processing_result.get('final_command'),
                    'confidence_score': processing_result.get('execution_confidence')
                }
            })
        
        elif processing_result['status'] == 'needs_clarification':
            base_response.update({
                'clarification_needed': True,
                'clarification_question': processing_result['clarification_question'],
                'suggested_responses': processing_result.get('next_steps', {}).get('user_should_provide', []),
                'help_text': self._generate_help_text(processing_result)
            })
        
        return base_response
    
    def _generate_help_text(self, processing_result: Dict[str, Any]) -> str:
        """Generate helpful guidance for user clarification"""
        
        next_steps = processing_result.get('next_steps', {})
        user_should_provide = next_steps.get('user_should_provide', [])
        
        if not user_should_provide:
            return "Please provide more specific details about what you want me to do."
        
        help_items = []
        for item in user_should_provide[:3]:  # Show max 3 items
            help_items.append(f"• {item}")
        
        return "To help me understand better, please tell me:\n" + "\n".join(help_items)
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get comprehensive session summary"""
        
        stats = self.conversation_state['session_stats']
        success_rate = (stats['successful_executions'] / stats['total_commands'] * 100) if stats['total_commands'] > 0 else 0
        
        return {
            'session_id': self.session_id,
            'session_duration': self._calculate_session_duration(),
            'statistics': {
                'total_commands': stats['total_commands'],
                'successful_executions': stats['successful_executions'],
                'clarifications_needed': stats['clarifications_needed'],
                'success_rate': round(success_rate, 1),
                'average_confidence': round(stats['avg_confidence'], 1)
            },
            'active_clarifications': len(self.conversation_state['active_clarifications']),
            'learned_preferences': self.conversation_state['user_preferences'],
            'recent_conversation': self.conversation_state['conversation_history'][-5:],
            'processor_summary': self.processor.get_processing_summary()
        }
    
    def _calculate_session_duration(self) -> str:
        """Calculate session duration"""
        session_start = datetime.strptime(self.session_id, "%Y%m%d_%H%M%S")
        duration = datetime.now() - session_start
        
        hours, remainder = divmod(duration.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def demonstrate_capabilities(self) -> None:
        """Demonstrate Chotu's enhanced capabilities"""
        
        print("🚀 CHOTU ENHANCED CAPABILITIES DEMONSTRATION")
        print("="*70)
        
        demo_commands = [
            ("set brightness to 80%", "Complete command - should execute directly"),
            ("increase it", "Ambiguous - should ask for clarification"),
            ("turn off the bluetooth", "Clear command - should execute"),
            ("make it louder", "Ambiguous subject - should clarify or resolve"),
            ("it", "Extremely vague - should ask for details"),
            ("chrome", "Missing action - should ask what to do with chrome")
        ]
        
        for i, (command, description) in enumerate(demo_commands, 1):
            print(f"\n{'='*70}")
            print(f"DEMO {i}/6: {description}")
            print('='*70)
            
            response = self.process_user_input(command)
            
            print(f"\n🤖 CHOTU SAYS: {response['message']}")
            print(f"📊 STATUS: {response['status'].upper()}")
            print(f"🎯 CONFIDENCE: {response['confidence']}%")
            print(f"🛤️  PATH: {response['processing_path']}")
            
            if response['status'] == 'needs_clarification':
                print(f"❓ HELP: {response.get('help_text', 'No additional help available')}")
        
        # Show session summary
        print(f"\n{'='*70}")
        print("📈 SESSION SUMMARY")
        print('='*70)
        
        summary = self.get_session_summary()
        stats = summary['statistics']
        
        print(f"Session ID: {summary['session_id']}")
        print(f"Duration: {summary['session_duration']}")
        print(f"Commands Processed: {stats['total_commands']}")
        print(f"Successful Executions: {stats['successful_executions']}")
        print(f"Clarifications Needed: {stats['clarifications_needed']}")
        print(f"Success Rate: {stats['success_rate']}%")
        print(f"Average Confidence: {stats['average_confidence']}%")

def main():
    """Main function to run Chotu Enhanced"""
    
    chotu = ChoutuEnhanced()
    
    print("🤖 Welcome to CHOTU ENHANCED!")
    print("Enhanced with prompt completeness analysis and iterative clarification")
    print("Type 'demo' to see capabilities demonstration")
    print("Type 'summary' to see session statistics")
    print("Type 'quit' to exit")
    print()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() == 'quit':
                print("👋 Goodbye!")
                break
            elif user_input.lower() == 'demo':
                chotu.demonstrate_capabilities()
                continue
            elif user_input.lower() == 'summary':
                summary = chotu.get_session_summary()
                print("\n📊 SESSION SUMMARY:")
                print(f"Commands: {summary['statistics']['total_commands']}")
                print(f"Success Rate: {summary['statistics']['success_rate']}%")
                print(f"Avg Confidence: {summary['statistics']['average_confidence']}%")
                continue
            
            if not user_input:
                continue
            
            response = chotu.process_user_input(user_input)
            print(f"Chotu: {response['message']}")
            
            if response.get('help_text'):
                print(f"💡 {response['help_text']}")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    # For testing, run demonstration
    chotu = ChoutuEnhanced()
    chotu.demonstrate_capabilities()
