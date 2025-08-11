#!/usr/bin/env python3
"""
🔄 CONTEXT INTEGRATION LAYER
============================
Seamlessly integrate enhanced context with existing Chotu system
"""

import json
from typing import Dict, Any, Optional
from memory.enhanced_context_manager import get_enhanced_context_manager

def enhance_existing_confidence_calculation(user_input: str, base_confidence: float) -> Dict[str, Any]:
    """
    Enhance existing confidence calculation with contextual insights
    
    This BUILDS ON your existing system, doesn't replace it
    """
    
    enhanced_context = get_enhanced_context_manager()
    
    # Get enhanced context analysis
    context_data = enhanced_context.get_enhanced_context(user_input, base_confidence)
    
    # Start with your existing confidence
    enhanced_confidence = base_confidence
    
    # Add contextual confidence boosts (build on existing +20, +15 boosts)
    if context_data.get('semantic_context'):
        semantic_boost = _calculate_semantic_confidence_boost(context_data['semantic_context'])
        enhanced_confidence += semantic_boost
    
    # Penalty for detected ambiguity
    ambiguity_data = context_data['textual_context']['ambiguity_resolution']
    if ambiguity_data['ambiguous_terms_found']:
        if ambiguity_data['confidence_in_resolution'] > 0.7:
            enhanced_confidence += 5  # We can resolve the ambiguity
        else:
            enhanced_confidence -= 10  # Unresolvable ambiguity
    
    # Cap at 100 (same as existing system)
    enhanced_confidence = min(enhanced_confidence, 100)
    
    return {
        'enhanced_confidence': enhanced_confidence,
        'confidence_boost': enhanced_confidence - base_confidence,
        'context_data': context_data,
        'recommendations': _get_improvement_recommendations(context_data)
    }

def _calculate_semantic_confidence_boost(semantic_context: Dict) -> float:
    """Calculate confidence boost from semantic similarity"""
    if not semantic_context or not semantic_context.get('most_similar'):
        return 0
    
    # Check if we have highly similar successful interactions
    successful_similar = [
        item for item in semantic_context['most_similar'] 
        if item['interaction'].get('success', False) and item['similarity'] > 0.8
    ]
    
    if successful_similar:
        return min(len(successful_similar) * 5, 15)  # Up to +15 boost
    
    return 0

def _get_improvement_recommendations(context_data: Dict) -> Dict[str, Any]:
    """Get actionable recommendations for improving user commands"""
    
    recommendations = {
        'immediate_suggestions': [],
        'clarifying_questions': context_data['suggested_questions'],
        'confidence_gaps': context_data['confidence_analysis']
    }
    
    # Add specific suggestions based on analysis
    gaps = context_data['confidence_analysis']
    
    if gaps['ambiguous_terms']:
        recommendations['immediate_suggestions'].append({
            'issue': f"Ambiguous terms detected: {', '.join(gaps['ambiguous_terms'])}",
            'suggestion': "Try being more specific about what you're referring to"
        })
    
    if gaps['clarity_issues']:
        recommendations['immediate_suggestions'].append({
            'issue': "Command clarity can be improved",
            'suggestion': "Add more descriptive words to your request"
        })
    
    return recommendations

def integrate_with_existing_medium_confidence_handler(ram: Dict, confidence: float, nlp_context: Dict) -> Dict[str, Any]:
    """
    Integration point for existing medium confidence handler
    
    This enhances your existing GPT prompt with better context
    """
    
    enhanced_context = get_enhanced_context_manager()
    context_data = enhanced_context.get_enhanced_context(ram['raw_input'], confidence)
    
    # Enhance the existing memory context with semantic data
    enhanced_memory_context = ram.get('memory_context', '')
    
    if context_data.get('semantic_context'):
        semantic_patterns = context_data['semantic_context'].get('semantic_patterns', {})
        if semantic_patterns.get('successful_patterns'):
            enhanced_memory_context += " | Semantically similar successful interactions: "
            for pattern in semantic_patterns['successful_patterns'][:2]:
                enhanced_memory_context += f"'{pattern['input']}' (similarity: {pattern['similarity']:.2f}), "
    
    # Add ambiguity resolution context
    ambiguity = context_data['textual_context']['ambiguity_resolution']
    if ambiguity['possible_references']:
        enhanced_memory_context += f" | Likely referring to: {ambiguity['possible_references']['most_likely']}"
    
    # Return enhanced context for existing GPT prompt
    return {
        'enhanced_memory_context': enhanced_memory_context,
        'clarifying_questions': context_data['suggested_questions'][:2],
        'confidence_recommendations': context_data['confidence_analysis'],
        'should_ask_for_clarification': context_data['clarification_needed']
    }

def generate_enhanced_gpt_prompt(ram: Dict, confidence: float, nlp_context: Dict) -> str:
    """
    Generate enhanced GPT prompt building on your existing system
    """
    
    # Get enhanced context integration
    enhanced_data = integrate_with_existing_medium_confidence_handler(ram, confidence, nlp_context)
    
    # Build on your existing prompt structure
    base_prompt = f"""
You are Chotu, an advanced AI assistant like J.A.R.V.I.S. with enhanced contextual understanding.

Current User Command: '{ram['raw_input']}'
NLP Analysis: {nlp_context}
Enhanced Context: {enhanced_data['enhanced_memory_context']}
Confidence Level: {confidence}%
"""
    
    # Add clarification guidance if needed
    if enhanced_data['should_ask_for_clarification']:
        base_prompt += f"""
CLARIFICATION NEEDED: The user's request has ambiguities. Consider asking:
{enhanced_data['clarifying_questions']}

Before providing a response, consider if clarification would be more helpful than attempting execution.
"""
    
    # Add your existing response format requirements
    base_prompt += """
With access to enhanced context analysis, respond in JSON format:
{
    "understood_intent": "specific action to take (be very specific)",
    "confidence": 90,
    "context_reasoning": "Based on enhanced context analysis and conversation history",
    "tools_needed": ["specific.tool.names"],
    "parameters": {"key": "value"},
    "response_tone": "professional",
    "clarification_needed": false,
    "clarifying_question": "Only if clarification is essential"
}
"""
    
    return base_prompt

def create_enhanced_integration_summary() -> Dict[str, Any]:
    """Create a summary of how the enhancement integrates with existing system"""
    
    return {
        'integration_approach': 'additive_enhancement',
        'existing_features_preserved': [
            'RAM/ROM memory system',
            'Three-stage confidence calculation',
            'NLP processor functionality', 
            '9-interaction conversation tracking',
            'Ambiguity resolution for "it", "that", "this"',
            'MCP server integration'
        ],
        'new_features_added': [
            'Semantic similarity search using sentence embeddings',
            'Enhanced confidence gap analysis',
            'Contextual clarifying question generation',
            'Improved ambiguity resolution with confidence scoring',
            'Semantic pattern recognition in conversation history'
        ],
        'integration_points': [
            'Existing confidence calculation (+0 to +15 boost)',
            'Enhanced memory context for GPT prompts',
            'Improved medium confidence handler',
            'Optional semantic embeddings (graceful fallback)'
        ],
        'backwards_compatibility': True,
        'performance_impact': 'minimal (optional semantic processing)',
        'deployment_strategy': 'gradual_activation'
    }
