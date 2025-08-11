#!/usr/bin/env python3
"""
🧠 CODE ANALYZER
==============
Maps existing capabilities, identifies gaps, and analyzes code semantically
"""

import ast
import inspect
import importlib
import json
import os
import sys
from typing import Dict, List, Any

# Import specialized GPT interface
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from utils.gpt_interface import call_gpt_learning, call_gpt_context

class CodeAnalyzer:
    """Advanced code analysis for self-learning capabilities"""
    
    def __init__(self):
        self.known_tools = {}
        self.capability_map = {}
        self.function_signatures = {}
        self.semantic_patterns = {}
        self._load_tool_signatures()
        self._build_capability_map()
    
    def _load_tool_signatures(self):
        """Load function signatures from all existing tools"""
        tools_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tools")
        
        for file in os.listdir(tools_dir):
            if file.endswith('.py') and not file.startswith('__'):
                module_name = file[:-3]
                
                # Skip test files and backup files to avoid import errors
                if any(skip in module_name for skip in ['test_', '_test', '_backup', '.backup']):
                    continue
                
                try:
                    spec = importlib.util.spec_from_file_location(
                        module_name, os.path.join(tools_dir, file)
                    )
                    if spec is None or spec.loader is None:
                        continue
                        
                    module = importlib.util.module_from_spec(spec)
                    
                    # Add the tools directory to sys.path temporarily for relative imports
                    import sys
                    original_path = sys.path.copy()
                    sys.path.insert(0, tools_dir)
                    
                    try:
                        spec.loader.exec_module(module)
                    finally:
                        sys.path = original_path
                    
                    signatures = {}
                    for name, obj in inspect.getmembers(module):
                        if inspect.isfunction(obj) and not name.startswith('_'):
                            try:
                                signatures[name] = {
                                    'params': str(inspect.signature(obj)),
                                    'doc': inspect.getdoc(obj) or "",
                                    'source': inspect.getsource(obj) if hasattr(obj, '__code__') else ""
                                }
                            except (OSError, TypeError):
                                signatures[name] = {
                                    'params': 'unknown',
                                    'doc': inspect.getdoc(obj) or "",
                                    'source': ""
                                }
                    
                    self.known_tools[module_name] = signatures
                    
                except ImportError as e:
                    # Skip modules with missing dependencies but don't show warning
                    if "No module named" in str(e):
                        continue
                    print(f"⚠️ Failed to analyze {module_name}: {e}")
                except Exception as e:
                    # Only show warnings for actual errors, not dependency issues
                    if not any(err in str(e) for err in ["No module named", "cannot import", "ModuleNotFoundError"]):
                        print(f"⚠️ Failed to analyze {module_name}: {e}")
        
        print(f"✅ Analyzed {len(self.known_tools)} tool modules")
    
    def _build_capability_map(self):
        """Build semantic capability map from existing tools"""
        for module_name, functions in self.known_tools.items():
            module_capabilities = []
            
            for func_name, details in functions.items():
                # Extract capabilities from function names and docs
                capabilities = self._extract_capabilities(func_name, details['doc'])
                module_capabilities.extend(capabilities)
            
            self.capability_map[module_name] = module_capabilities
    
    def _extract_capabilities(self, func_name: str, doc: str) -> List[str]:
        """Extract semantic capabilities from function name and documentation"""
        capabilities = []
        
        # Function name analysis
        name_parts = func_name.lower().replace('_', ' ').split()
        capabilities.extend(name_parts)
        
        # Documentation analysis
        if doc:
            # Extract key action words from documentation
            doc_lower = doc.lower()
            action_words = ['create', 'open', 'close', 'set', 'get', 'enable', 'disable', 
                          'increase', 'decrease', 'toggle', 'send', 'take', 'play', 'stop']
            
            for word in action_words:
                if word in doc_lower:
                    capabilities.append(word)
        
        return list(set(capabilities))  # Remove duplicates
    
    def analyze_intent(self, intent: str, existing_capabilities: Dict) -> Dict[str, Any]:
        """Analyze user intent against existing capabilities"""
        
        prompt = f"""
You are an expert system analyzer for an AI assistant. Analyze this user intent against existing capabilities.

USER INTENT: "{intent}"

EXISTING CAPABILITIES:
{json.dumps(existing_capabilities, indent=2)}

CAPABILITY MAP:
{json.dumps(self.capability_map, indent=2)}

Perform deep semantic analysis:
1. What is the user trying to accomplish?
2. Do we have any similar/related capabilities?
3. What specific functionality is missing?
4. Can we extend an existing tool or need a new one?
5. What are the technical requirements?

Return detailed JSON analysis:
{{
    "intent_category": "system_control|app_management|file_operations|communication|media|web|productivity",
    "user_goal": "clear description of what user wants to achieve",
    "missing_capability": "specific functionality that's missing",
    "gap_analysis": {{
        "similar_existing": ["list of similar existing functions"],
        "capability_gap": "what specific gap needs to be filled",
        "complexity_level": "simple|medium|complex|expert"
    }},
    "technical_requirements": {{
        "requires_external_tools": ["list of external tools/commands needed"],
        "requires_permissions": ["list of permissions needed"],
        "requires_apis": ["list of APIs or services needed"],
        "platform_specific": "macOS specific considerations"
    }},
    "implementation_strategy": {{
        "approach": "extend_existing|create_new|hybrid",
        "target_module": "which module to extend (if applicable)",
        "new_function_name": "suggested function name",
        "integration_points": ["how it connects with existing tools"]
    }},
    "safety_considerations": ["list of safety/security concerns"],
    "test_scenarios": ["list of test cases to validate the implementation"]
}}
"""
        
        try:
            response = call_gpt_learning(prompt)
            
            # Clean and parse JSON response
            response = response.strip()
            if response.startswith('```json'):
                response = response[7:]
            if response.endswith('```'):
                response = response[:-3]
            
            analysis = json.loads(response.strip())
            
            # Add confidence score based on gap analysis
            analysis['confidence_score'] = self._calculate_capability_confidence(analysis)
            
            return analysis
            
        except Exception as e:
            print(f"❌ Intent analysis failed: {e}")
            return {
                "intent_category": "unknown",
                "user_goal": intent,
                "missing_capability": "analysis failed",
                "confidence_score": 0
            }
    
    def _calculate_capability_confidence(self, analysis: Dict) -> int:
        """Calculate confidence score for capability implementation"""
        score = 0
        
        # Base score from complexity
        complexity = analysis.get('gap_analysis', {}).get('complexity_level', 'complex')
        if complexity == 'simple':
            score += 40
        elif complexity == 'medium':
            score += 25
        elif complexity == 'complex':
            score += 10
        
        # Boost for similar existing capabilities
        similar_existing = analysis.get('gap_analysis', {}).get('similar_existing', [])
        if similar_existing:
            score += min(len(similar_existing) * 15, 30)
        
        # Reduce for external dependencies
        external_tools = analysis.get('technical_requirements', {}).get('requires_external_tools', [])
        score -= len(external_tools) * 5
        
        # Boost for clear implementation strategy
        if analysis.get('implementation_strategy', {}).get('approach') == 'extend_existing':
            score += 20
        
        return max(0, min(100, score))
    
    def find_similar_implementations(self, intent: str) -> List[Dict]:
        """Find similar implementations that could be used as templates"""
        similar_functions = []
        
        intent_words = set(intent.lower().split())
        
        for module_name, functions in self.known_tools.items():
            for func_name, details in functions.items():
                # Calculate similarity score
                func_words = set(func_name.lower().replace('_', ' ').split())
                doc_words = set(details['doc'].lower().split()) if details['doc'] else set()
                
                all_func_words = func_words.union(doc_words)
                overlap = len(intent_words.intersection(all_func_words))
                
                if overlap > 0:
                    similarity_score = overlap / len(intent_words.union(all_func_words))
                    
                    similar_functions.append({
                        'module': module_name,
                        'function': func_name,
                        'similarity_score': similarity_score,
                        'signature': details['params'],
                        'documentation': details['doc'],
                        'source_code': details['source'][:500] + '...' if len(details['source']) > 500 else details['source']
                    })
        
        # Sort by similarity score
        similar_functions.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        return similar_functions[:5]  # Return top 5 similar functions
    
    def validate_capability_gap(self, intent: str, analysis: Dict) -> bool:
        """Validate that there's actually a capability gap using precise semantic matching"""
        
        # Extract the core functionality from the intent
        missing_capability = analysis.get('missing_capability', '').lower()
        user_goal = analysis.get('user_goal', '').lower()
        
        # Special case: If GPT says the capability already exists, trust it
        # But be more precise about the matching - look for positive confirmations
        if any(phrase in missing_capability for phrase in [
            'capability can fulfill', 'already available', 'already exists',
            'can fulfill this', 'currently has', 'include a function', 'includes a',
            'capabilities already include', 'existing tools can handle'
        ]):
            print(f"🔍 GPT analysis indicates existing capability: {missing_capability}")
            return False  # No gap - GPT says we already have this
        
        # If GPT explicitly says we DON'T have the capability, that's a gap
        if any(phrase in missing_capability for phrase in [
            'do not include', 'does not include', 'capabilities do not', 'currently does not',
            'not currently have', 'missing the capability', 'lacks the ability'
        ]):
            print(f"🔍 GPT analysis confirms capability gap: {missing_capability}")
            return True  # Confirmed gap - GPT says we DON'T have this
        
        # Check for direct function name matches first
        intent_lower = intent.lower()
        for module_name, functions in self.known_tools.items():
            for func_name, details in functions.items():
                # Check for exact function name matches
                func_words = func_name.lower().replace('_', ' ')
                if self._direct_function_match(intent_lower, func_words):
                    print(f"🔍 Found direct function match: {module_name}.{func_name}")
                    return False  # No gap - direct match found
        
        # Check for EXACT functional matches (not just word overlap)
        for module_name, functions in self.known_tools.items():
            for func_name, details in functions.items():
                # Look for functions that perform the SAME core task
                func_purpose = self._extract_function_purpose(func_name, details['doc'])
                
                # Check for semantic equivalence
                if self._is_functionally_equivalent(missing_capability, func_purpose):
                    print(f"🔍 Found functionally equivalent capability: {module_name}.{func_name}")
                    print(f"    Purpose: {func_purpose}")
                    return False  # No gap - we already have this exact capability
                
                # Check if the function directly addresses the user goal
                if self._addresses_user_goal(user_goal, func_purpose):
                    print(f"🔍 Found function that addresses user goal: {module_name}.{func_name}")
                    print(f"    Goal: {user_goal}")
                    print(f"    Function: {func_purpose}")
                    return False  # No gap - existing function solves the problem
        
        # Check similar implementations with MUCH higher threshold
        similar = self.find_similar_implementations(intent)
        if similar and similar[0]['similarity_score'] > 0.95:  # Much stricter threshold
            print(f"🔍 Found near-identical implementation: {similar[0]['function']} (score: {similar[0]['similarity_score']:.2f})")
            return False  # No significant gap
        
        print(f"✅ Confirmed capability gap for: {missing_capability}")
        return True  # Confirmed capability gap
    
    def _direct_function_match(self, intent: str, func_name: str) -> bool:
        """Check for direct function name matches"""
        # Normalize strings
        intent_words = set(intent.split())
        func_words = set(func_name.split())
        
        # Define direct matches
        direct_matches = {
            'play music': 'play music',
            'send email': 'send email',
            'get weather': 'get weather',
            'open file': 'open file',
            'battery': 'battery',
            'network': 'network'
        }
        
        for intent_pattern, func_pattern in direct_matches.items():
            if intent_pattern in intent and func_pattern in func_name:
                return True
                
        return False
    
    def generate_enhancement_plan(self, analysis: Dict) -> Dict:
        """Generate a plan for implementing the missing capability"""
        
        plan = {
            "implementation_type": analysis['implementation_strategy']['approach'],
            "priority_level": self._calculate_priority(analysis),
            "estimated_effort": self._estimate_effort(analysis),
            "dependencies": self._identify_dependencies(analysis),
            "risks": self._assess_risks(analysis),
            "success_criteria": analysis.get('test_scenarios', [])
        }
        
        return plan
    
    def _calculate_priority(self, analysis: Dict) -> str:
        """Calculate implementation priority based on analysis"""
        confidence = analysis.get('confidence_score', 0)
        complexity = analysis.get('gap_analysis', {}).get('complexity_level', 'complex')
        
        if confidence >= 70 and complexity in ['simple', 'medium']:
            return 'high'
        elif confidence >= 50:
            return 'medium'
        else:
            return 'low'
    
    def _estimate_effort(self, analysis: Dict) -> str:
        """Estimate development effort"""
        complexity = analysis.get('gap_analysis', {}).get('complexity_level', 'complex')
        external_deps = len(analysis.get('technical_requirements', {}).get('requires_external_tools', []))
        
        if complexity == 'simple' and external_deps == 0:
            return 'low'
        elif complexity == 'medium' or external_deps <= 2:
            return 'medium'
        else:
            return 'high'
    
    def _identify_dependencies(self, analysis: Dict) -> List[str]:
        """Identify all dependencies for implementation"""
        deps = []
        
        tech_reqs = analysis.get('technical_requirements', {})
        deps.extend(tech_reqs.get('requires_external_tools', []))
        deps.extend(tech_reqs.get('requires_apis', []))
        
        if tech_reqs.get('requires_permissions'):
            deps.extend([f"permission:{p}" for p in tech_reqs['requires_permissions']])
        
        return deps
    
    def _assess_risks(self, analysis: Dict) -> List[str]:
        """Assess potential risks for implementing this capability"""
        risks = []
        
        # Get complexity level
        complexity = analysis.get('gap_analysis', {}).get('complexity_level', 'unknown')
        if complexity in ['complex', 'expert']:
            risks.append(f"High complexity implementation ({complexity} level)")
        
        # Check technical requirements
        tech_reqs = analysis.get('technical_requirements', {})
        
        if tech_reqs.get('requires_external_tools'):
            risks.append("Dependency on external tools/libraries")
        
        if tech_reqs.get('requires_permissions'):
            for perm in tech_reqs['requires_permissions']:
                if 'system' in perm.lower() or 'admin' in perm.lower():
                    risks.append(f"Requires elevated permissions: {perm}")
                elif 'file' in perm.lower():
                    risks.append("File system access required")
        
        if tech_reqs.get('requires_apis'):
            risks.append("Dependency on external APIs")
        
        # Check safety considerations
        safety_items = analysis.get('safety_considerations', [])
        for item in safety_items:
            if any(keyword in item.lower() for keyword in ['security', 'unauthorized', 'data loss']):
                risks.append(f"Security concern: {item}")
        
        # Check category-specific risks
        category = analysis.get('intent_category', '')
        if 'system_control' in category:
            risks.append("System control operations can affect stability")
        if 'file_operations' in category:
            risks.append("File operations can cause data loss if not handled properly")
        if 'web' in category:
            risks.append("Web operations depend on external connectivity")
        
        # Default risk if none identified
        if not risks:
            risks.append("Standard implementation risks apply")
        
        return risks
    
    def analyze_tool_failure(self, tool_name: str, error_message: str, user_intent: str) -> Dict[str, Any]:
        """
        Analyze why an existing tool failed and what improvements are needed
        Enhanced failure analysis for better autonomous learning
        """
        
        prompt = f"""
You are an expert system analyzer for autonomous learning. A tool failed and you need to analyze why and how to fix it.

TOOL FAILURE ANALYSIS:
- Tool Name: {tool_name}
- Error Message: {error_message}
- User Intent: {user_intent}

EXISTING TOOL CAPABILITIES:
{json.dumps(self.known_tools.get(tool_name, {}), indent=2)}

Perform deep failure analysis:

1. ROOT CAUSE ANALYSIS:
   - What exactly caused the failure?
   - Is it a configuration issue, missing dependency, or fundamental limitation?
   - Can the existing tool be fixed or does it need replacement?

2. TECHNICAL REQUIREMENTS FOR FIX:
   - What specific technical knowledge is needed?
   - What external services, APIs, or protocols are required?
   - What authentication or configuration is needed?

3. IMPROVEMENT STRATEGY:
   - Should we modify existing tool or create new one?
   - What's the minimum viable fix vs comprehensive solution?
   - What are the implementation steps?

4. LEARNING OPPORTUNITY:
   - What domain knowledge should the system learn from this failure?
   - How can we prevent similar failures in the future?
   - What patterns can be extracted for future tool generation?

Return detailed JSON analysis:
{{
    "failure_analysis": {{
        "root_cause": "specific technical reason for failure",
        "failure_category": "configuration|dependency|fundamental_limitation|authentication|network",
        "fixable": true/false,
        "complexity_level": "simple|medium|complex|expert"
    }},
    "technical_requirements": {{
        "protocols_needed": ["list of required protocols/services"],
        "dependencies": ["required python modules, system tools"],
        "authentication": "description of auth requirements",
        "configuration": "what configuration is needed"
    }},
    "improvement_strategy": {{
        "approach": "fix_existing|replace_tool|hybrid_solution",
        "implementation_priority": "high|medium|low",
        "estimated_effort": "small|medium|large",
        "success_probability": 85
    }},
    "domain_knowledge": {{
        "concepts_to_learn": ["key concepts the system should understand"],
        "common_patterns": ["reusable patterns for similar problems"],
        "best_practices": ["best practices for this domain"]
    }},
    "specific_solution": {{
        "tool_name": "suggested new tool name",
        "key_functions": ["list of functions the improved tool should have"],
        "implementation_notes": "specific guidance for implementation"
    }}
}}
"""
        
        try:
            response = call_gpt_learning(prompt)
            
            # Clean and parse JSON response
            response = response.strip()
            if response.startswith('```json'):
                response = response[7:]
            if response.endswith('```'):
                response = response[:-3]
            
            analysis = json.loads(response.strip())
            
            print(f"🔍 Failure Analysis Complete:")
            print(f"   Root Cause: {analysis.get('failure_analysis', {}).get('root_cause', 'unknown')}")
            print(f"   Approach: {analysis.get('improvement_strategy', {}).get('approach', 'unknown')}")
            print(f"   Success Probability: {analysis.get('improvement_strategy', {}).get('success_probability', 0)}%")
            
            return analysis
            
        except Exception as e:
            print(f"❌ Failure analysis failed: {e}")
            return {
                "failure_analysis": {
                    "root_cause": f"Analysis failed: {e}",
                    "failure_category": "analysis_error",
                    "fixable": False,
                    "complexity_level": "unknown"
                }
            }
    
    def _extract_function_purpose(self, func_name: str, doc: str) -> str:
        """Extract the core purpose/functionality of a function"""
        # Normalize function name
        name_parts = func_name.lower().replace('_', ' ')
        
        # Extract key purpose from documentation
        if doc:
            # Look for purpose indicators in first line or sentences
            lines = doc.split('\n')
            for line in lines:
                line = line.strip().lower()
                if line and not line.startswith('args') and not line.startswith('returns'):
                    # This is likely the purpose description
                    return f"{name_parts}: {line}"
        
        return name_parts
    
    def _is_functionally_equivalent(self, missing_capability: str, existing_purpose: str) -> bool:
        """Check if two capabilities are functionally equivalent"""
        # Normalize both strings
        missing = missing_capability.lower().strip()
        existing = existing_purpose.lower().strip()
        
        # Define semantic equivalences for common functions
        equivalences = {
            'battery': ['battery status monitoring', 'battery percentage', 'battery level', 'power level', 'charge level', 'battery monitoring', 'monitor battery'],
            'network': ['network connectivity monitoring', 'network latency', 'check connectivity', 'internet connectivity', 'network monitoring', 'connectivity check'],
            'music': ['play music', 'music playback', 'audio playback', 'sound playback', 'play audio'],
            'email': ['send email', 'email sending', 'send message', 'email functionality', 'email communication'],
            'weather': ['weather information', 'weather data', 'weather forecast', 'get weather', 'weather details'],
            'file': ['file operations', 'open file', 'file access', 'file handling', 'file management'],
            'app': ['application control', 'launch app', 'open application', 'start program', 'run application'],
            'system': ['system control', 'system information', 'system status', 'system monitoring']
        }
        
        # Check for direct semantic matches
        for category, variations in equivalences.items():
            missing_matches = sum(1 for variant in variations if self._contains_semantic_match(missing, variant))
            existing_matches = sum(1 for variant in variations if self._contains_semantic_match(existing, variant))
            
            # If both have matches in the same category, they're equivalent
            if missing_matches >= 1 and existing_matches >= 1:
                return True
        
        return False
    
    def _contains_semantic_match(self, text: str, pattern: str) -> bool:
        """Check if text contains a semantic match for the pattern"""
        # Normalize both strings
        text = text.lower().strip()
        pattern = pattern.lower().strip()
        
        # Split into key words
        text_words = set(text.split())
        pattern_words = set(pattern.split())
        
        # Remove common words
        common_words = {'get', 'set', 'the', 'a', 'an', 'and', 'or', 'with', 'for', 'to', 'of', 'in', 'on', 'at', 'is', 'are', 'have', 'has'}
        text_words -= common_words
        pattern_words -= common_words
        
        # Check for significant overlap
        if len(pattern_words) == 0:
            return False
        
        overlap = len(text_words.intersection(pattern_words))
        # Require at least 70% of pattern words to be present
        match_threshold = max(1, len(pattern_words) * 0.7)
        
        return overlap >= match_threshold
    
    def _addresses_user_goal(self, user_goal: str, function_purpose: str) -> bool:
        """Check if a function directly addresses the user's goal with high precision"""
        goal = user_goal.lower().strip()
        purpose = function_purpose.lower().strip()
        
        # First check: Do they involve the same domain/technology?
        # Only match if they're working with the same type of resource
        goal_domains = set()
        purpose_domains = set()
        
        domain_keywords = {
            'database': ['database', 'db', 'sqlite', 'mysql', 'postgresql', 'sql'],
            'file': ['file', 'document', 'txt', 'pdf', 'csv'],
            'folder': ['folder', 'directory', 'dir'],
            'web': ['web', 'browser', 'website', 'url', 'http'],
            'email': ['email', 'mail', 'message'],
            'system': ['system', 'process', 'service', 'application'],
            'media': ['video', 'audio', 'music', 'sound', 'image']
        }
        
        for domain, keywords in domain_keywords.items():
            if any(keyword in goal for keyword in keywords):
                goal_domains.add(domain)
            if any(keyword in purpose for keyword in keywords):
                purpose_domains.add(domain)
        
        # If they don't share any domain, they can't address the same goal
        if goal_domains and purpose_domains and not goal_domains.intersection(purpose_domains):
            return False
        
        # If goal has specific domains but purpose doesn't, they're not related
        if goal_domains and not purpose_domains:
            return False
        
        # Extract action verbs from user goal
        action_verbs = {
            'monitor', 'check', 'get', 'show', 'display', 'track', 'watch',
            'create', 'make', 'generate', 'build', 'add',
            'open', 'launch', 'start', 'run', 'execute',
            'close', 'stop', 'end', 'terminate', 'quit',
            'send', 'email', 'message', 'notify', 'alert',
            'play', 'pause', 'volume', 'music', 'sound',
            'search', 'find', 'locate', 'lookup'
        }
        
        goal_actions = [word for word in goal.split() if word in action_verbs]
        purpose_actions = [word for word in purpose.split() if word in action_verbs]
        
        # If they have the same primary action AND same domain, check similarity
        if goal_actions and purpose_actions:
            if goal_actions[0] == purpose_actions[0]:
                # Same action - check if target is similar
                goal_targets = [word for word in goal.split() if word not in action_verbs]
                purpose_targets = [word for word in purpose.split() if word not in action_verbs]
                
                # Remove articles and common words
                common_words = {'the', 'a', 'an', 'my', 'your', 'this', 'that'}
                goal_targets = [word for word in goal_targets if word not in common_words]
                purpose_targets = [word for word in purpose_targets if word not in common_words]
                
                # Check for target overlap
                if goal_targets and purpose_targets:
                    target_overlap = len(set(goal_targets).intersection(set(purpose_targets)))
                    return target_overlap >= 1
        
        return False
