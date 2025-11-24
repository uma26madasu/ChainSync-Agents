"""
Tests for MeetingContextAgent - Slotify Integration

This module tests the MeetingContextAgent functionality for:
- Processing Slotify meetings with ChainSync alerts
- Generating meeting context explanations
- Calculating urgency and suggesting attendees
- Post-meeting summary generation
"""

import unittest
import asyncio
from datetime import datetime
from chainsync.specialized_agents import MeetingContextAgent
from chainsync.agent_orchestrator import AgentOrchestrator


class TestMeetingContextAgent(unittest.TestCase):
    """Test cases for MeetingContextAgent."""

    def setUp(self):
        """Set up test fixtures."""
        self.agent = MeetingContextAgent()
        self.sample_meeting_data = {
            'meeting_id': 'test-meeting-001',
            'title': 'Critical System Review',
            'scheduled_time': '2025-11-25T10:00:00Z',
            'attendees': ['devops@company.com', 'sre@company.com']
        }
        self.sample_alert_data = {
            'alert_id': 'test-alert-001',
            'alert_type': 'system_failure',
            'severity': 'critical',
            'description': 'Database connection pool exhausted',
            'affected_systems': ['API Gateway', 'User Service'],
            'detected_at': '2025-11-24T15:30:00Z',
            'context': {
                'connection_count': 100,
                'max_connections': 100
            }
        }

    def test_agent_initialization(self):
        """Test that MeetingContextAgent initializes correctly."""
        self.assertIsNotNone(self.agent)
        self.assertEqual(self.agent.agent_name, "MeetingContextAgent")
        self.assertIsInstance(self.agent.alert_meeting_map, dict)
        self.assertIsInstance(self.agent.meeting_history, list)
        self.assertIsInstance(self.agent.alert_types, dict)

    def test_alert_types_defined(self):
        """Test that all expected alert types are defined."""
        expected_types = [
            'compliance_violation',
            'system_failure',
            'performance_degradation',
            'security_incident',
            'data_quality_issue',
            'integration_failure',
            'capacity_warning'
        ]
        for alert_type in expected_types:
            self.assertIn(alert_type, self.agent.alert_types)
            self.assertIn('severity_weight', self.agent.alert_types[alert_type])
            self.assertIn('category', self.agent.alert_types[alert_type])
            self.assertIn('typical_attendees', self.agent.alert_types[alert_type])

    def test_calculate_urgency_critical(self):
        """Test urgency calculation for critical alerts."""
        alert_data = {'severity': 'critical', 'alert_type': 'system_failure'}
        urgency = self.agent._calculate_urgency(alert_data)

        self.assertEqual(urgency['level'], 'CRITICAL')
        self.assertGreaterEqual(urgency['score'], 0.8)
        self.assertIn('< 1 hour', urgency['recommended_response_time'])

    def test_calculate_urgency_high(self):
        """Test urgency calculation for high severity alerts."""
        alert_data = {'severity': 'high', 'alert_type': 'compliance_violation'}
        urgency = self.agent._calculate_urgency(alert_data)

        self.assertIn(urgency['level'], ['CRITICAL', 'HIGH'])
        self.assertGreaterEqual(urgency['score'], 0.6)

    def test_calculate_urgency_medium(self):
        """Test urgency calculation for medium severity alerts."""
        alert_data = {'severity': 'medium', 'alert_type': 'data_quality_issue'}
        urgency = self.agent._calculate_urgency(alert_data)

        self.assertIn(urgency['level'], ['MEDIUM', 'LOW'])
        self.assertLess(urgency['score'], 0.6)

    def test_calculate_urgency_low(self):
        """Test urgency calculation for low severity alerts."""
        alert_data = {'severity': 'low', 'alert_type': 'capacity_warning'}
        urgency = self.agent._calculate_urgency(alert_data)

        self.assertEqual(urgency['level'], 'LOW')
        self.assertLess(urgency['score'], 0.4)

    def test_recommend_duration_critical(self):
        """Test meeting duration recommendation for critical alerts."""
        alert_data = {'severity': 'critical', 'affected_systems': ['A', 'B', 'C', 'D']}
        duration = self.agent._recommend_duration(alert_data)
        self.assertEqual(duration, '60 minutes')

    def test_recommend_duration_high(self):
        """Test meeting duration recommendation for high severity alerts."""
        alert_data = {'severity': 'high', 'affected_systems': ['A', 'B']}
        duration = self.agent._recommend_duration(alert_data)
        self.assertEqual(duration, '45 minutes')

    def test_recommend_duration_medium(self):
        """Test meeting duration recommendation for medium severity alerts."""
        alert_data = {'severity': 'medium', 'affected_systems': ['A']}
        duration = self.agent._recommend_duration(alert_data)
        self.assertEqual(duration, '30 minutes')

    def test_recommend_duration_low(self):
        """Test meeting duration recommendation for low severity alerts."""
        alert_data = {'severity': 'low', 'affected_systems': []}
        duration = self.agent._recommend_duration(alert_data)
        self.assertEqual(duration, '15 minutes')

    def test_suggest_attendees_system_failure(self):
        """Test attendee suggestions for system failure alerts."""
        alert_data = {'alert_type': 'system_failure', 'severity': 'critical'}
        attendees = self.agent._suggest_attendees(alert_data)

        self.assertIn('DevOps', attendees)
        self.assertIn('Management', attendees)

    def test_suggest_attendees_compliance_violation(self):
        """Test attendee suggestions for compliance violation alerts."""
        alert_data = {'alert_type': 'compliance_violation', 'severity': 'high'}
        attendees = self.agent._suggest_attendees(alert_data)

        self.assertIn('Compliance Officer', attendees)
        self.assertIn('Legal', attendees)
        self.assertIn('Management', attendees)

    def test_suggest_attendees_security_incident(self):
        """Test attendee suggestions for security incident alerts."""
        alert_data = {'alert_type': 'security_incident', 'severity': 'critical'}
        attendees = self.agent._suggest_attendees(alert_data)

        self.assertIn('Security Team', attendees)
        self.assertIn('CISO', attendees)
        self.assertIn('Executive Sponsor', attendees)

    def test_process_slotify_meeting_method_exists(self):
        """Test that process_slotify_meeting method exists."""
        self.assertTrue(hasattr(self.agent, 'process_slotify_meeting'))
        self.assertTrue(asyncio.iscoroutinefunction(self.agent.process_slotify_meeting))

    def test_explain_meeting_method_exists(self):
        """Test that explain_meeting method exists."""
        self.assertTrue(hasattr(self.agent, 'explain_meeting'))
        self.assertTrue(asyncio.iscoroutinefunction(self.agent.explain_meeting))

    def test_generate_post_meeting_summary_method_exists(self):
        """Test that generate_post_meeting_summary method exists."""
        self.assertTrue(hasattr(self.agent, 'generate_post_meeting_summary'))
        self.assertTrue(asyncio.iscoroutinefunction(self.agent.generate_post_meeting_summary))

    def test_get_meeting_context_by_alert_method_exists(self):
        """Test that get_meeting_context_by_alert method exists."""
        self.assertTrue(hasattr(self.agent, 'get_meeting_context_by_alert'))
        self.assertTrue(asyncio.iscoroutinefunction(self.agent.get_meeting_context_by_alert))

    def test_get_meeting_context_by_meeting_id_method_exists(self):
        """Test that get_meeting_context_by_meeting_id method exists."""
        self.assertTrue(hasattr(self.agent, 'get_meeting_context_by_meeting_id'))
        self.assertTrue(asyncio.iscoroutinefunction(self.agent.get_meeting_context_by_meeting_id))


class TestAgentOrchestratorMeetingContext(unittest.TestCase):
    """Test cases for MeetingContextAgent integration in AgentOrchestrator."""

    def setUp(self):
        """Set up test fixtures."""
        self.orchestrator = AgentOrchestrator()

    def test_meeting_context_agent_registered(self):
        """Test that MeetingContextAgent is registered in orchestrator."""
        self.assertIn('meeting_context', self.orchestrator.agents)
        self.assertIsInstance(
            self.orchestrator.agents['meeting_context'],
            MeetingContextAgent
        )

    def test_meeting_context_agent_listed(self):
        """Test that MeetingContextAgent is listed in agent descriptions."""
        agents = self.orchestrator.list_agents()
        self.assertIn('meeting_context', agents)
        self.assertIn('Slotify', agents['meeting_context'])

    def test_meeting_routing_available(self):
        """Test that meeting-related request types are routable."""
        # We can't easily test the routing without making actual requests
        # but we can verify the orchestrator has the method
        self.assertTrue(hasattr(self.orchestrator, 'route_request'))
        self.assertTrue(asyncio.iscoroutinefunction(self.orchestrator.route_request))

    def test_alert_to_meeting_workflow_available(self):
        """Test that alert_to_meeting workflow is available."""
        self.assertTrue(hasattr(self.orchestrator, 'multi_agent_workflow'))
        self.assertTrue(asyncio.iscoroutinefunction(self.orchestrator.multi_agent_workflow))

    def test_get_meeting_context_agent(self):
        """Test getting meeting context agent directly."""
        agent = self.orchestrator.get_agent('meeting_context')
        self.assertIsNotNone(agent)
        self.assertIsInstance(agent, MeetingContextAgent)


class TestMeetingContextAgentAsync(unittest.TestCase):
    """Async test cases for MeetingContextAgent."""

    def setUp(self):
        """Set up test fixtures."""
        self.agent = MeetingContextAgent()
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        """Clean up after tests."""
        self.loop.close()

    def test_get_meeting_context_by_alert_not_found(self):
        """Test getting meeting context for non-existent alert."""
        async def run_test():
            result = await self.agent.get_meeting_context_by_alert('non-existent-alert')
            self.assertIsNone(result)

        self.loop.run_until_complete(run_test())

    def test_get_meeting_context_by_meeting_id_not_found(self):
        """Test getting meeting context for non-existent meeting."""
        async def run_test():
            result = await self.agent.get_meeting_context_by_meeting_id('non-existent-meeting')
            self.assertIsNone(result)

        self.loop.run_until_complete(run_test())

    def test_explain_meeting_not_found(self):
        """Test explaining non-existent meeting."""
        async def run_test():
            result = await self.agent.explain_meeting('non-existent-meeting')
            self.assertIn('No context found', result)

        self.loop.run_until_complete(run_test())


if __name__ == "__main__":
    unittest.main()
