"""
Specialized AI Agents for ChainSync Multi-Domain Enterprise Platform

This module contains specialized agents for different operational needs:
- Continuous Learning Agent
- Root Cause Analysis Agent
- Natural Language Query Agent
- Compliance Autopilot Agent
- Memory-Enabled Agent
- Multi-Step Reasoning Agent
"""

import json
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional
from .config import Config


class BaseAgent:
    """Base class for all specialized agents with common functionality."""

    def __init__(self, agent_name: str):
        """Initialize base agent with name and configuration."""
        self.agent_name = agent_name
        self.config = Config()
        self.created_at = datetime.now()

    def _get_openai_client(self):
        """Get OpenAI client instance."""
        try:
            import openai
            openai.api_key = self.config.get_openai_api_key()
            return openai
        except ImportError:
            raise ImportError("OpenAI package not installed. Run: pip install openai")

    async def _call_openai(self, messages: List[Dict], model: str = "gpt-4", temperature: float = 0.7) -> str:
        """Make async call to OpenAI API."""
        try:
            client = self._get_openai_client()
            response = await asyncio.to_thread(
                client.chat.completions.create,
                model=model,
                messages=messages,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error calling OpenAI: {str(e)}"

    def log(self, message: str):
        """Log agent activity."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{self.agent_name}] {message}")


class ContinuousLearningAgent(BaseAgent):
    """
    Agent that learns from interactions and improves over time.

    Capabilities:
    - Stores interaction patterns
    - Identifies recurring issues
    - Suggests optimizations based on historical data
    - Adapts responses based on feedback
    """

    def __init__(self):
        super().__init__("ContinuousLearningAgent")
        self.learning_history = []
        self.feedback_scores = []
        self.optimization_suggestions = []

    async def learn_from_interaction(self, interaction: Dict[str, Any], feedback_score: Optional[float] = None) -> Dict:
        """
        Learn from a user interaction and store insights.

        Args:
            interaction: Dict containing query, response, context
            feedback_score: Optional feedback score (0-1)

        Returns:
            Dict with learning insights
        """
        self.log(f"Learning from interaction: {interaction.get('query', 'N/A')[:50]}...")

        # Store interaction
        learning_entry = {
            'timestamp': datetime.now().isoformat(),
            'interaction': interaction,
            'feedback_score': feedback_score
        }
        self.learning_history.append(learning_entry)

        if feedback_score is not None:
            self.feedback_scores.append(feedback_score)

        # Analyze patterns if we have enough history
        if len(self.learning_history) >= 5:
            patterns = await self._identify_patterns()
            return {
                'learned': True,
                'total_interactions': len(self.learning_history),
                'average_feedback': sum(self.feedback_scores) / len(self.feedback_scores) if self.feedback_scores else None,
                'patterns': patterns,
                'agent': self.agent_name
            }

        return {
            'learned': True,
            'total_interactions': len(self.learning_history),
            'message': 'Collecting more data for pattern analysis',
            'agent': self.agent_name
        }

    async def _identify_patterns(self) -> List[str]:
        """Identify patterns from learning history using AI."""
        recent_interactions = self.learning_history[-10:]

        messages = [
            {"role": "system", "content": "You are an AI that identifies patterns in user interactions to improve future responses."},
            {"role": "user", "content": f"Analyze these interactions and identify key patterns:\n{json.dumps(recent_interactions, indent=2)}"}
        ]

        analysis = await self._call_openai(messages, temperature=0.3)
        return [analysis]

    async def suggest_optimization(self, current_query: str) -> Dict:
        """Suggest optimizations based on learning history."""
        if not self.learning_history:
            return {'suggestion': 'No learning history available yet', 'agent': self.agent_name}

        messages = [
            {"role": "system", "content": "You are an AI optimization assistant that suggests improvements based on historical data."},
            {"role": "user", "content": f"Based on this learning history:\n{json.dumps(self.learning_history[-5:], indent=2)}\n\nSuggest optimizations for this query: {current_query}"}
        ]

        suggestion = await self._call_openai(messages, temperature=0.5)

        return {
            'query': current_query,
            'optimization_suggestion': suggestion,
            'based_on_interactions': len(self.learning_history),
            'agent': self.agent_name
        }


class RootCauseAnalysisAgent(BaseAgent):
    """
    Agent specialized in identifying root causes of failures and issues.

    Capabilities:
    - Analyzes error logs and stack traces
    - Identifies underlying causes vs symptoms
    - Provides remediation recommendations
    - Uses 5 Whys and Fishbone analysis techniques
    """

    def __init__(self):
        super().__init__("RootCauseAnalysisAgent")
        self.analysis_history = []

    async def analyze_failure(self, failure_data: Dict[str, Any]) -> Dict:
        """
        Perform root cause analysis on a failure.

        Args:
            failure_data: Dict containing error, context, logs, etc.

        Returns:
            Dict with root cause analysis results
        """
        self.log(f"Analyzing failure: {failure_data.get('error_type', 'Unknown')}...")

        # Extract key information
        error_message = failure_data.get('error_message', '')
        stack_trace = failure_data.get('stack_trace', '')
        context = failure_data.get('context', {})

        # Perform 5 Whys analysis
        five_whys = await self._perform_five_whys(error_message, context)

        # Identify root cause
        root_cause = await self._identify_root_cause(failure_data)

        # Generate recommendations
        recommendations = await self._generate_recommendations(root_cause, failure_data)

        analysis_result = {
            'timestamp': datetime.now().isoformat(),
            'error_message': error_message,
            'five_whys_analysis': five_whys,
            'root_cause': root_cause,
            'recommendations': recommendations,
            'severity': self._assess_severity(failure_data),
            'agent': self.agent_name
        }

        self.analysis_history.append(analysis_result)
        return analysis_result

    async def _perform_five_whys(self, error: str, context: Dict) -> List[str]:
        """Perform 5 Whys analysis technique."""
        messages = [
            {"role": "system", "content": "You are a root cause analysis expert. Use the 5 Whys technique to identify underlying causes."},
            {"role": "user", "content": f"Error: {error}\nContext: {json.dumps(context)}\n\nPerform 5 Whys analysis. Ask 'Why?' five times to get to the root cause."}
        ]

        analysis = await self._call_openai(messages, temperature=0.3)
        return analysis.split('\n')

    async def _identify_root_cause(self, failure_data: Dict) -> str:
        """Identify the root cause from failure data."""
        messages = [
            {"role": "system", "content": "You are a root cause analysis expert. Identify the underlying root cause, not just symptoms."},
            {"role": "user", "content": f"Analyze this failure data and identify the root cause:\n{json.dumps(failure_data, indent=2)}"}
        ]

        return await self._call_openai(messages, temperature=0.2)

    async def _generate_recommendations(self, root_cause: str, failure_data: Dict) -> List[str]:
        """Generate remediation recommendations."""
        messages = [
            {"role": "system", "content": "You are a solutions architect. Provide actionable remediation steps."},
            {"role": "user", "content": f"Root Cause: {root_cause}\n\nProvide 3-5 specific remediation steps to prevent this issue."}
        ]

        recommendations = await self._call_openai(messages, temperature=0.4)
        return recommendations.split('\n')

    def _assess_severity(self, failure_data: Dict) -> str:
        """Assess failure severity."""
        impact = failure_data.get('impact', 'unknown')
        if impact in ['critical', 'high']:
            return 'HIGH'
        elif impact == 'medium':
            return 'MEDIUM'
        return 'LOW'


class NaturalLanguageQueryAgent(BaseAgent):
    """
    Agent that processes natural language queries and converts them to structured operations.

    Capabilities:
    - Understands natural language questions
    - Converts queries to API calls or database queries
    - Retrieves and formats data
    - Provides natural language responses
    """

    def __init__(self):
        super().__init__("NaturalLanguageQueryAgent")
        self.query_history = []

    async def process_query(self, user_query: str, data_source: str = "chainsync") -> Dict:
        """
        Process a natural language query and return results.

        Args:
            user_query: Natural language question from user
            data_source: Data source to query (chainsync, database, etc.)

        Returns:
            Dict with query results and natural language response
        """
        self.log(f"Processing query: {user_query[:50]}...")

        # Parse intent and extract parameters
        intent = await self._parse_intent(user_query)

        # Convert to structured query
        structured_query = await self._convert_to_structured_query(user_query, data_source)

        # Execute query (mock for now)
        results = await self._execute_query(structured_query, data_source)

        # Generate natural language response
        nl_response = await self._generate_nl_response(user_query, results)

        query_result = {
            'timestamp': datetime.now().isoformat(),
            'original_query': user_query,
            'intent': intent,
            'structured_query': structured_query,
            'results': results,
            'natural_language_response': nl_response,
            'agent': self.agent_name
        }

        self.query_history.append(query_result)
        return query_result

    async def _parse_intent(self, query: str) -> Dict:
        """Parse user intent from natural language."""
        messages = [
            {"role": "system", "content": "You are an intent parser. Extract the intent and key entities from user queries. Return JSON format."},
            {"role": "user", "content": f"Parse this query: '{query}'\n\nReturn JSON with: intent, entities, query_type"}
        ]

        intent_str = await self._call_openai(messages, temperature=0.2)

        try:
            return json.loads(intent_str)
        except:
            return {'intent': 'unknown', 'entities': [], 'query_type': 'general'}

    async def _convert_to_structured_query(self, nl_query: str, data_source: str) -> Dict:
        """Convert natural language to structured query."""
        messages = [
            {"role": "system", "content": f"Convert natural language queries to structured {data_source} API calls. Return JSON."},
            {"role": "user", "content": f"Convert to structured query: '{nl_query}'"}
        ]

        structured_str = await self._call_openai(messages, temperature=0.1)

        try:
            return json.loads(structured_str)
        except:
            return {'type': 'search', 'query': nl_query}

    async def _execute_query(self, structured_query: Dict, data_source: str) -> Any:
        """Execute the structured query against data source."""
        # Mock implementation - in production, this would call actual APIs
        self.log(f"Executing query on {data_source}: {structured_query}")

        return {
            'status': 'success',
            'data': [
                {'id': 1, 'name': 'Sample Result 1', 'value': 100},
                {'id': 2, 'name': 'Sample Result 2', 'value': 200}
            ],
            'count': 2
        }

    async def _generate_nl_response(self, original_query: str, results: Any) -> str:
        """Generate natural language response from results."""
        messages = [
            {"role": "system", "content": "Convert data results into clear, natural language responses."},
            {"role": "user", "content": f"Query: {original_query}\n\nResults: {json.dumps(results, indent=2)}\n\nProvide a clear natural language answer."}
        ]

        return await self._call_openai(messages, temperature=0.5)


class ComplianceAutopilotAgent(BaseAgent):
    """
    Agent that automatically monitors and ensures compliance with regulations.

    Capabilities:
    - Monitors operations for compliance violations
    - Checks against regulatory frameworks (SOC2, GDPR, HIPAA, etc.)
    - Generates compliance reports
    - Alerts on violations and provides remediation steps
    """

    def __init__(self):
        super().__init__("ComplianceAutopilotAgent")
        self.compliance_frameworks = ['SOC2', 'GDPR', 'HIPAA', 'ISO27001', 'PCI-DSS']
        self.violations = []
        self.compliance_checks = []

    async def check_compliance(self, operation_data: Dict[str, Any], frameworks: Optional[List[str]] = None) -> Dict:
        """
        Check operation for compliance with specified frameworks.

        Args:
            operation_data: Data about the operation to check
            frameworks: List of compliance frameworks to check against

        Returns:
            Dict with compliance results
        """
        if frameworks is None:
            frameworks = self.compliance_frameworks

        self.log(f"Checking compliance against: {', '.join(frameworks)}...")

        results = {}
        for framework in frameworks:
            framework_result = await self._check_framework_compliance(operation_data, framework)
            results[framework] = framework_result

        # Identify violations
        violations = self._extract_violations(results)

        compliance_result = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation_data.get('operation_type', 'unknown'),
            'frameworks_checked': frameworks,
            'results': results,
            'violations': violations,
            'overall_status': 'COMPLIANT' if not violations else 'NON_COMPLIANT',
            'risk_level': self._assess_compliance_risk(violations),
            'agent': self.agent_name
        }

        self.compliance_checks.append(compliance_result)

        if violations:
            self.violations.extend(violations)

        return compliance_result

    async def _check_framework_compliance(self, operation_data: Dict, framework: str) -> Dict:
        """Check compliance against a specific framework."""
        messages = [
            {"role": "system", "content": f"You are a {framework} compliance expert. Analyze operations for compliance violations."},
            {"role": "user", "content": f"Check this operation for {framework} compliance:\n{json.dumps(operation_data, indent=2)}\n\nProvide: status (compliant/non-compliant), issues found, and recommendations."}
        ]

        analysis = await self._call_openai(messages, temperature=0.2)

        return {
            'framework': framework,
            'analysis': analysis,
            'checked_at': datetime.now().isoformat()
        }

    def _extract_violations(self, results: Dict) -> List[Dict]:
        """Extract violations from compliance check results."""
        violations = []

        for framework, result in results.items():
            analysis = result.get('analysis', '')
            if 'non-compliant' in analysis.lower() or 'violation' in analysis.lower():
                violations.append({
                    'framework': framework,
                    'details': analysis,
                    'severity': 'high'
                })

        return violations

    def _assess_compliance_risk(self, violations: List[Dict]) -> str:
        """Assess overall compliance risk level."""
        if not violations:
            return 'LOW'
        if len(violations) >= 3:
            return 'HIGH'
        return 'MEDIUM'

    async def generate_compliance_report(self, time_period: str = "last_30_days") -> Dict:
        """Generate comprehensive compliance report."""
        self.log(f"Generating compliance report for {time_period}...")

        messages = [
            {"role": "system", "content": "Generate a comprehensive compliance report based on check history."},
            {"role": "user", "content": f"Generate report for:\nTotal Checks: {len(self.compliance_checks)}\nViolations: {len(self.violations)}\n\nProvide executive summary and key findings."}
        ]

        report_summary = await self._call_openai(messages, temperature=0.3)

        return {
            'period': time_period,
            'total_checks': len(self.compliance_checks),
            'total_violations': len(self.violations),
            'frameworks_monitored': self.compliance_frameworks,
            'executive_summary': report_summary,
            'recent_violations': self.violations[-5:],
            'agent': self.agent_name
        }


class MemoryEnabledAgent(BaseAgent):
    """
    Agent with persistent memory across conversations.

    Capabilities:
    - Maintains conversation history
    - Remembers user preferences and context
    - Recalls past interactions
    - Provides context-aware responses
    """

    def __init__(self):
        super().__init__("MemoryEnabledAgent")
        self.conversations = {}
        self.user_preferences = {}
        self.long_term_memory = []

    async def chat(self, user_message: str, conversation_id: str, user_id: Optional[str] = None) -> Dict:
        """
        Chat with memory of past conversations.

        Args:
            user_message: User's message
            conversation_id: ID of the conversation thread
            user_id: Optional user identifier

        Returns:
            Dict with response and conversation context
        """
        self.log(f"Chat in conversation {conversation_id}: {user_message[:50]}...")

        # Initialize conversation if new
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = {
                'id': conversation_id,
                'user_id': user_id,
                'started_at': datetime.now().isoformat(),
                'messages': [],
                'context': {}
            }

        conversation = self.conversations[conversation_id]

        # Add user message to history
        conversation['messages'].append({
            'role': 'user',
            'content': user_message,
            'timestamp': datetime.now().isoformat()
        })

        # Get relevant context from memory
        relevant_context = await self._recall_relevant_context(user_message, conversation_id)

        # Generate response with full conversation history
        response = await self._generate_contextual_response(
            user_message,
            conversation['messages'],
            relevant_context
        )

        # Add assistant response to history
        conversation['messages'].append({
            'role': 'assistant',
            'content': response,
            'timestamp': datetime.now().isoformat()
        })

        # Update long-term memory
        await self._update_long_term_memory(user_message, response, conversation_id)

        return {
            'conversation_id': conversation_id,
            'response': response,
            'message_count': len(conversation['messages']),
            'context_used': relevant_context,
            'agent': self.agent_name
        }

    async def _recall_relevant_context(self, message: str, conversation_id: str) -> Dict:
        """Recall relevant context from memory."""
        conversation = self.conversations.get(conversation_id, {})

        return {
            'conversation_history_length': len(conversation.get('messages', [])),
            'user_preferences': self.user_preferences.get(conversation.get('user_id'), {}),
            'related_memories': [m for m in self.long_term_memory[-5:]]
        }

    async def _generate_contextual_response(self, user_message: str, message_history: List[Dict], context: Dict) -> str:
        """Generate response with full conversation context."""
        # Build messages for OpenAI including history
        messages = [
            {"role": "system", "content": "You are a helpful assistant with memory of past conversations. Use context to provide personalized, relevant responses."}
        ]

        # Add recent conversation history (last 10 messages)
        for msg in message_history[-10:]:
            messages.append({
                "role": msg['role'],
                "content": msg['content']
            })

        # Add current message context
        messages.append({
            "role": "system",
            "content": f"Context from memory: {json.dumps(context)}"
        })

        return await self._call_openai(messages, temperature=0.7)

    async def _update_long_term_memory(self, user_message: str, response: str, conversation_id: str):
        """Update long-term memory with important information."""
        # Store significant interactions in long-term memory
        memory_entry = {
            'timestamp': datetime.now().isoformat(),
            'conversation_id': conversation_id,
            'user_message': user_message,
            'response': response
        }

        self.long_term_memory.append(memory_entry)

        # Keep only last 100 entries
        if len(self.long_term_memory) > 100:
            self.long_term_memory = self.long_term_memory[-100:]

    def set_user_preference(self, user_id: str, preference_key: str, preference_value: Any):
        """Set a user preference."""
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = {}

        self.user_preferences[user_id][preference_key] = preference_value
        self.log(f"Set preference for {user_id}: {preference_key} = {preference_value}")

    def get_conversation_summary(self, conversation_id: str) -> Dict:
        """Get summary of a conversation."""
        conversation = self.conversations.get(conversation_id)

        if not conversation:
            return {'error': 'Conversation not found'}

        return {
            'conversation_id': conversation_id,
            'started_at': conversation['started_at'],
            'message_count': len(conversation['messages']),
            'user_id': conversation.get('user_id'),
            'agent': self.agent_name
        }


class MultiStepReasoningAgent(BaseAgent):
    """
    Agent that breaks down complex problems into steps and reasons through them.

    Capabilities:
    - Decomposes complex queries into sub-tasks
    - Executes steps sequentially with reasoning
    - Maintains reasoning chain
    - Provides step-by-step explanations
    """

    def __init__(self):
        super().__init__("MultiStepReasoningAgent")
        self.reasoning_history = []

    async def solve_problem(self, problem: str, max_steps: int = 10) -> Dict:
        """
        Solve a complex problem using multi-step reasoning.

        Args:
            problem: Complex problem to solve
            max_steps: Maximum number of reasoning steps

        Returns:
            Dict with reasoning chain and solution
        """
        self.log(f"Solving problem: {problem[:50]}...")

        # Break down into steps
        steps = await self._decompose_problem(problem)

        # Execute each step
        reasoning_chain = []
        for i, step in enumerate(steps[:max_steps], 1):
            step_result = await self._execute_step(step, i, reasoning_chain)
            reasoning_chain.append(step_result)

        # Synthesize final answer
        final_answer = await self._synthesize_answer(problem, reasoning_chain)

        result = {
            'timestamp': datetime.now().isoformat(),
            'problem': problem,
            'total_steps': len(reasoning_chain),
            'reasoning_chain': reasoning_chain,
            'final_answer': final_answer,
            'agent': self.agent_name
        }

        self.reasoning_history.append(result)
        return result

    async def _decompose_problem(self, problem: str) -> List[str]:
        """Decompose complex problem into steps."""
        messages = [
            {"role": "system", "content": "You are an expert at breaking down complex problems into clear, sequential steps."},
            {"role": "user", "content": f"Break down this problem into 3-7 logical steps:\n{problem}\n\nReturn only the steps, numbered."}
        ]

        steps_text = await self._call_openai(messages, temperature=0.3)

        # Parse steps
        steps = [line.strip() for line in steps_text.split('\n') if line.strip() and any(c.isdigit() for c in line[:3])]
        return steps

    async def _execute_step(self, step: str, step_number: int, previous_steps: List[Dict]) -> Dict:
        """Execute a reasoning step."""
        self.log(f"Executing step {step_number}: {step[:50]}...")

        # Build context from previous steps
        context = "\n".join([f"Step {i+1}: {s['step']} -> {s['reasoning']}" for i, s in enumerate(previous_steps)])

        messages = [
            {"role": "system", "content": "You are reasoning through a problem step by step. Provide clear reasoning for this step."},
            {"role": "user", "content": f"Previous steps:\n{context}\n\nCurrent step: {step}\n\nProvide your reasoning and conclusions for this step."}
        ]

        reasoning = await self._call_openai(messages, temperature=0.5)

        return {
            'step_number': step_number,
            'step': step,
            'reasoning': reasoning,
            'timestamp': datetime.now().isoformat()
        }

    async def _synthesize_answer(self, problem: str, reasoning_chain: List[Dict]) -> str:
        """Synthesize final answer from reasoning chain."""
        chain_summary = "\n".join([
            f"Step {s['step_number']}: {s['step']}\nReasoning: {s['reasoning']}\n"
            for s in reasoning_chain
        ])

        messages = [
            {"role": "system", "content": "Synthesize a final answer based on the step-by-step reasoning."},
            {"role": "user", "content": f"Problem: {problem}\n\nReasoning Chain:\n{chain_summary}\n\nProvide a clear, comprehensive final answer."}
        ]

        return await self._call_openai(messages, temperature=0.4)

    async def explain_reasoning(self, problem: str) -> str:
        """Explain the reasoning process for a problem."""
        # Find most recent solution for this problem
        for result in reversed(self.reasoning_history):
            if result['problem'] == problem:
                explanation = f"Problem: {problem}\n\n"
                explanation += f"I solved this in {result['total_steps']} steps:\n\n"

                for step in result['reasoning_chain']:
                    explanation += f"{step['step']}\n"
                    explanation += f"Reasoning: {step['reasoning']}\n\n"

                explanation += f"Final Answer: {result['final_answer']}"
                return explanation

        return "No reasoning history found for this problem."
