"""
Agent Orchestrator for ChainSync Multi-Domain Enterprise Platform

This module provides coordination and orchestration of multiple specialized agents.
"""

import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime
from .specialized_agents import (
    ContinuousLearningAgent,
    RootCauseAnalysisAgent,
    NaturalLanguageQueryAgent,
    ComplianceAutopilotAgent,
    MemoryEnabledAgent,
    MultiStepReasoningAgent,
    MeetingContextAgent
)


class AgentOrchestrator:
    """
    Orchestrates multiple specialized agents to work together.

    Capabilities:
    - Manages all specialized agents
    - Routes requests to appropriate agents
    - Coordinates multi-agent workflows
    - Provides unified interface for agent interactions
    """

    def __init__(self):
        """Initialize orchestrator with all specialized agents."""
        self.agents = {
            'continuous_learning': ContinuousLearningAgent(),
            'root_cause_analysis': RootCauseAnalysisAgent(),
            'natural_language_query': NaturalLanguageQueryAgent(),
            'compliance_autopilot': ComplianceAutopilotAgent(),
            'memory_enabled': MemoryEnabledAgent(),
            'multi_step_reasoning': MultiStepReasoningAgent(),
            'meeting_context': MeetingContextAgent()
        }

        self.orchestration_history = []
        self.created_at = datetime.now()

        print(f"[AgentOrchestrator] Initialized with {len(self.agents)} specialized agents")

    def get_agent(self, agent_name: str) -> Optional[Any]:
        """
        Get a specific agent by name.

        Args:
            agent_name: Name of the agent to retrieve

        Returns:
            Agent instance or None
        """
        return self.agents.get(agent_name)

    def list_agents(self) -> Dict[str, str]:
        """
        List all available agents with descriptions.

        Returns:
            Dict mapping agent names to descriptions
        """
        return {
            'continuous_learning': 'Learns from interactions and improves over time',
            'root_cause_analysis': 'Analyzes failures and identifies root causes',
            'natural_language_query': 'Processes natural language queries against data',
            'compliance_autopilot': 'Monitors and ensures regulatory compliance',
            'memory_enabled': 'Maintains conversation history and context',
            'multi_step_reasoning': 'Breaks down complex problems into steps',
            'meeting_context': 'Provides context for Slotify meetings based on ChainSync alerts'
        }

    async def route_request(self, request_type: str, request_data: Dict[str, Any]) -> Dict:
        """
        Route a request to the appropriate agent.

        Args:
            request_type: Type of request (query, analysis, compliance_check, etc.)
            request_data: Data for the request

        Returns:
            Dict with agent response
        """
        print(f"[AgentOrchestrator] Routing request type: {request_type}")

        routing_map = {
            'query': 'natural_language_query',
            'nl_query': 'natural_language_query',
            'failure_analysis': 'root_cause_analysis',
            'rca': 'root_cause_analysis',
            'compliance_check': 'compliance_autopilot',
            'compliance': 'compliance_autopilot',
            'chat': 'memory_enabled',
            'conversation': 'memory_enabled',
            'problem_solving': 'multi_step_reasoning',
            'reasoning': 'multi_step_reasoning',
            'learning': 'continuous_learning',
            'meeting': 'meeting_context',
            'meeting_context': 'meeting_context',
            'slotify': 'meeting_context'
        }

        agent_name = routing_map.get(request_type.lower())

        if not agent_name:
            return {
                'error': f'Unknown request type: {request_type}',
                'available_types': list(routing_map.keys())
            }

        agent = self.get_agent(agent_name)
        result = await self._execute_agent_request(agent, agent_name, request_data)

        # Learn from this interaction
        await self._learn_from_interaction(request_type, request_data, result)

        return result

    async def _execute_agent_request(self, agent: Any, agent_name: str, request_data: Dict) -> Dict:
        """Execute request on specific agent."""
        try:
            if agent_name == 'natural_language_query':
                return await agent.process_query(
                    request_data.get('query', ''),
                    request_data.get('data_source', 'chainsync')
                )

            elif agent_name == 'root_cause_analysis':
                return await agent.analyze_failure(request_data)

            elif agent_name == 'compliance_autopilot':
                return await agent.check_compliance(
                    request_data,
                    request_data.get('frameworks')
                )

            elif agent_name == 'memory_enabled':
                return await agent.chat(
                    request_data.get('message', ''),
                    request_data.get('conversation_id', 'default'),
                    request_data.get('user_id')
                )

            elif agent_name == 'multi_step_reasoning':
                return await agent.solve_problem(
                    request_data.get('problem', ''),
                    request_data.get('max_steps', 10)
                )

            elif agent_name == 'continuous_learning':
                return await agent.learn_from_interaction(
                    request_data.get('interaction', {}),
                    request_data.get('feedback_score')
                )

            elif agent_name == 'meeting_context':
                return await agent.process_slotify_meeting(
                    request_data.get('meeting_data', {}),
                    request_data.get('alert_data', {})
                )

        except Exception as e:
            return {
                'error': f'Agent execution failed: {str(e)}',
                'agent': agent_name
            }

    async def _learn_from_interaction(self, request_type: str, request_data: Dict, result: Dict):
        """Have continuous learning agent learn from this interaction."""
        learning_agent = self.agents['continuous_learning']

        interaction = {
            'query': f"{request_type}: {str(request_data)[:100]}",
            'response': str(result)[:100],
            'context': {'request_type': request_type}
        }

        # Don't wait for learning to complete
        asyncio.create_task(learning_agent.learn_from_interaction(interaction))

    async def multi_agent_workflow(self, workflow_name: str, workflow_data: Dict[str, Any]) -> Dict:
        """
        Execute a workflow involving multiple agents.

        Args:
            workflow_name: Name of the workflow
            workflow_data: Data for the workflow

        Returns:
            Dict with workflow results
        """
        print(f"[AgentOrchestrator] Executing workflow: {workflow_name}")

        workflows = {
            'intelligent_incident_response': self._intelligent_incident_response,
            'compliance_with_rca': self._compliance_with_rca,
            'conversational_problem_solving': self._conversational_problem_solving,
            'alert_to_meeting': self._alert_to_meeting_workflow
        }

        workflow_func = workflows.get(workflow_name)

        if not workflow_func:
            return {
                'error': f'Unknown workflow: {workflow_name}',
                'available_workflows': list(workflows.keys())
            }

        result = await workflow_func(workflow_data)

        # Record orchestration
        self.orchestration_history.append({
            'timestamp': datetime.now().isoformat(),
            'workflow': workflow_name,
            'result': result
        })

        return result

    async def _intelligent_incident_response(self, data: Dict) -> Dict:
        """
        Workflow: Intelligent incident response using multiple agents.

        Steps:
        1. Query agent processes incident description
        2. RCA agent performs root cause analysis
        3. Compliance agent checks if incident caused compliance violations
        4. Learning agent records incident for future improvement
        """
        print("[Workflow] Intelligent Incident Response")

        # Step 1: Process incident query
        query_agent = self.agents['natural_language_query']
        query_result = await query_agent.process_query(
            data.get('incident_description', ''),
            'chainsync'
        )

        # Step 2: Root cause analysis
        rca_agent = self.agents['root_cause_analysis']
        rca_result = await rca_agent.analyze_failure({
            'error_message': data.get('error_message', ''),
            'stack_trace': data.get('stack_trace', ''),
            'context': query_result
        })

        # Step 3: Compliance check
        compliance_agent = self.agents['compliance_autopilot']
        compliance_result = await compliance_agent.check_compliance({
            'operation_type': 'incident_response',
            'incident_data': data,
            'root_cause': rca_result.get('root_cause')
        })

        # Step 4: Learn from incident
        learning_agent = self.agents['continuous_learning']
        await learning_agent.learn_from_interaction({
            'query': data.get('incident_description'),
            'response': rca_result,
            'context': {'incident': True}
        })

        return {
            'workflow': 'intelligent_incident_response',
            'query_analysis': query_result,
            'root_cause_analysis': rca_result,
            'compliance_check': compliance_result,
            'timestamp': datetime.now().isoformat()
        }

    async def _compliance_with_rca(self, data: Dict) -> Dict:
        """
        Workflow: Compliance monitoring with automatic RCA for violations.

        Steps:
        1. Compliance agent checks operation
        2. If violations found, RCA agent analyzes why
        3. Multi-step reasoning agent develops remediation plan
        """
        print("[Workflow] Compliance with RCA")

        # Step 1: Check compliance
        compliance_agent = self.agents['compliance_autopilot']
        compliance_result = await compliance_agent.check_compliance(
            data,
            data.get('frameworks')
        )

        workflow_result = {
            'workflow': 'compliance_with_rca',
            'compliance_check': compliance_result
        }

        # Step 2: If violations, perform RCA
        if compliance_result.get('violations'):
            rca_agent = self.agents['root_cause_analysis']
            rca_result = await rca_agent.analyze_failure({
                'error_message': 'Compliance violations detected',
                'context': {
                    'violations': compliance_result['violations'],
                    'operation': data
                }
            })

            workflow_result['root_cause_analysis'] = rca_result

            # Step 3: Develop remediation plan
            reasoning_agent = self.agents['multi_step_reasoning']
            remediation_result = await reasoning_agent.solve_problem(
                f"Develop remediation plan for compliance violations: {compliance_result['violations']}"
            )

            workflow_result['remediation_plan'] = remediation_result

        return workflow_result

    async def _conversational_problem_solving(self, data: Dict) -> Dict:
        """
        Workflow: Conversational problem solving with memory and reasoning.

        Steps:
        1. Memory agent maintains conversation context
        2. Multi-step reasoning agent solves the problem
        3. Learning agent improves from feedback
        """
        print("[Workflow] Conversational Problem Solving")

        conversation_id = data.get('conversation_id', 'default')
        problem = data.get('problem', '')

        # Step 1: Chat with memory
        memory_agent = self.agents['memory_enabled']
        chat_result = await memory_agent.chat(
            problem,
            conversation_id,
            data.get('user_id')
        )

        # Step 2: Solve problem with reasoning
        reasoning_agent = self.agents['multi_step_reasoning']
        solution_result = await reasoning_agent.solve_problem(problem)

        # Step 3: Send solution back through memory agent
        solution_chat = await memory_agent.chat(
            f"Here's the solution: {solution_result['final_answer']}",
            conversation_id
        )

        return {
            'workflow': 'conversational_problem_solving',
            'conversation_id': conversation_id,
            'initial_chat': chat_result,
            'problem_solution': solution_result,
            'solution_delivery': solution_chat,
            'timestamp': datetime.now().isoformat()
        }

    async def _alert_to_meeting_workflow(self, data: Dict) -> Dict:
        """
        Workflow: Process ChainSync alert and create Slotify meeting with full context.

        Steps:
        1. RCA agent analyzes the alert to understand root cause
        2. Compliance agent checks for any compliance implications
        3. Meeting Context agent creates meeting with full context explanation
        4. Learning agent records the alert pattern

        Args:
            data: Dict containing:
                - alert_data: ChainSync alert information
                - meeting_data: Slotify meeting details (optional, can be auto-generated)

        Returns:
            Dict with complete workflow results including meeting context
        """
        print("[Workflow] Alert to Meeting")

        alert_data = data.get('alert_data', {})
        meeting_data = data.get('meeting_data', {})

        # Auto-generate meeting data if not provided
        if not meeting_data.get('meeting_id'):
            meeting_data['meeting_id'] = f"slotify_meeting_{datetime.now().timestamp()}"
        if not meeting_data.get('title'):
            alert_type = alert_data.get('alert_type', 'Unknown')
            severity = alert_data.get('severity', 'medium')
            meeting_data['title'] = f"[{severity.upper()}] {alert_type.replace('_', ' ').title()} Review"
        if not meeting_data.get('scheduled_time'):
            meeting_data['scheduled_time'] = datetime.now().isoformat()

        # Step 1: Root cause analysis on the alert
        rca_agent = self.agents['root_cause_analysis']
        rca_result = await rca_agent.analyze_failure({
            'error_message': alert_data.get('description', ''),
            'error_type': alert_data.get('alert_type', 'unknown'),
            'context': alert_data.get('context', {}),
            'impact': alert_data.get('severity', 'medium')
        })

        # Enrich alert data with RCA results
        enriched_alert = {
            **alert_data,
            'root_cause_analysis': rca_result.get('root_cause'),
            'recommendations': rca_result.get('recommendations', [])
        }

        # Step 2: Check for compliance implications
        compliance_agent = self.agents['compliance_autopilot']
        compliance_result = await compliance_agent.check_compliance({
            'operation_type': alert_data.get('alert_type', 'system_alert'),
            'alert_data': alert_data,
            'root_cause': rca_result.get('root_cause')
        }, alert_data.get('compliance_frameworks'))

        # Add compliance info to enriched alert
        enriched_alert['compliance_implications'] = compliance_result

        # Step 3: Create meeting context with MeetingContextAgent
        meeting_agent = self.agents['meeting_context']
        meeting_context = await meeting_agent.process_slotify_meeting(
            meeting_data,
            enriched_alert
        )

        # Step 4: Learn from this alert pattern
        learning_agent = self.agents['continuous_learning']
        await learning_agent.learn_from_interaction({
            'query': f"Alert: {alert_data.get('alert_type')} - {alert_data.get('description', '')}",
            'response': meeting_context,
            'context': {'alert_to_meeting': True, 'severity': alert_data.get('severity')}
        })

        return {
            'workflow': 'alert_to_meeting',
            'alert_id': alert_data.get('alert_id'),
            'meeting_id': meeting_data.get('meeting_id'),
            'root_cause_analysis': rca_result,
            'compliance_check': compliance_result,
            'meeting_context': meeting_context,
            'meeting_explanation': await meeting_agent.explain_meeting(meeting_data.get('meeting_id')),
            'timestamp': datetime.now().isoformat()
        }

    async def get_system_status(self) -> Dict:
        """
        Get overall system status and agent health.

        Returns:
            Dict with system status
        """
        return {
            'orchestrator': {
                'status': 'operational',
                'uptime': str(datetime.now() - self.created_at),
                'total_orchestrations': len(self.orchestration_history)
            },
            'agents': {
                name: {
                    'status': 'operational',
                    'type': agent.__class__.__name__
                }
                for name, agent in self.agents.items()
            },
            'capabilities': self.list_agents()
        }

    async def execute_parallel_agents(self, agent_tasks: List[Dict]) -> List[Dict]:
        """
        Execute multiple agent tasks in parallel.

        Args:
            agent_tasks: List of dicts with 'agent_name' and 'request_data'

        Returns:
            List of results from all agents
        """
        print(f"[AgentOrchestrator] Executing {len(agent_tasks)} agents in parallel")

        tasks = []
        for task in agent_tasks:
            agent_name = task.get('agent_name')
            request_data = task.get('request_data', {})
            agent = self.get_agent(agent_name)

            if agent:
                tasks.append(self._execute_agent_request(agent, agent_name, request_data))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        return [
            result if not isinstance(result, Exception) else {'error': str(result)}
            for result in results
        ]
