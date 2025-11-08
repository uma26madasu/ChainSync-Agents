"""
ChainSync AI Agent - Main Application Entry Point

Demonstrates all specialized AI agents:
- Continuous Learning Agent
- Root Cause Analysis Agent
- Natural Language Query Agent
- Compliance Autopilot Agent
- Memory-Enabled Agent
- Multi-Step Reasoning Agent
"""
import asyncio
import logging
import json
from chainsync.config import Config
from chainsync.ai_agent import ChainSyncAIAgent
from chainsync.agent_orchestrator import AgentOrchestrator

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")


def print_result(label: str, data: dict):
    """Print a formatted result."""
    print(f"\n{label}:")
    print(json.dumps(data, indent=2, default=str)[:500] + "...")


async def demo_specialized_agents():
    """Demonstrate all specialized agents."""

    print_section("Specialized Agents Demo")

    # Initialize orchestrator (manages all agents)
    orchestrator = AgentOrchestrator()

    # List available agents
    print("\nAvailable Agents:")
    for name, description in orchestrator.list_agents().items():
        print(f"  • {name}: {description}")

    # Demo 1: Natural Language Query Agent
    print_section("1. Natural Language Query Agent")
    query_result = await orchestrator.route_request('query', {
        'query': 'What are the top 5 facilities with highest environmental risk scores?',
        'data_source': 'chainsync'
    })
    print_result("Query Result", query_result)

    # Demo 2: Root Cause Analysis Agent
    print_section("2. Root Cause Analysis Agent")
    rca_result = await orchestrator.route_request('failure_analysis', {
        'error_message': 'Database connection timeout after 30 seconds',
        'stack_trace': 'at DatabaseConnection.connect() line 145',
        'context': {
            'service': 'water-quality-monitoring',
            'timestamp': '2025-11-08T10:30:00Z',
            'impact': 'high'
        }
    })
    print_result("RCA Result", rca_result)

    # Demo 3: Compliance Autopilot Agent
    print_section("3. Compliance Autopilot Agent")
    compliance_result = await orchestrator.route_request('compliance', {
        'operation_type': 'data_processing',
        'data_types': ['personal_data', 'health_records'],
        'storage_location': 'us-east-1',
        'encryption': True,
        'frameworks': ['GDPR', 'HIPAA']
    })
    print_result("Compliance Check", compliance_result)

    # Demo 4: Memory-Enabled Agent
    print_section("4. Memory-Enabled Agent (Conversational)")

    # First message
    chat1 = await orchestrator.route_request('chat', {
        'message': 'I need help analyzing water quality trends for facility WQ-001',
        'conversation_id': 'conv-demo-1',
        'user_id': 'user-123'
    })
    print_result("Chat Response 1", chat1)

    # Follow-up message (agent remembers context)
    chat2 = await orchestrator.route_request('chat', {
        'message': 'What were the main concerns from last month?',
        'conversation_id': 'conv-demo-1',
        'user_id': 'user-123'
    })
    print_result("Chat Response 2", chat2)

    # Demo 5: Multi-Step Reasoning Agent
    print_section("5. Multi-Step Reasoning Agent")
    reasoning_result = await orchestrator.route_request('reasoning', {
        'problem': 'How can we reduce energy consumption across all facilities while maintaining operational efficiency?',
        'max_steps': 5
    })
    print_result("Reasoning Result", reasoning_result)

    # Demo 6: Continuous Learning Agent
    print_section("6. Continuous Learning Agent")
    learning_result = await orchestrator.route_request('learning', {
        'interaction': {
            'query': 'Compliance check for GDPR',
            'response': 'Compliant with recommendations',
            'context': {'domain': 'compliance'}
        },
        'feedback_score': 0.9
    })
    print_result("Learning Result", learning_result)

    return orchestrator


async def demo_multi_agent_workflows():
    """Demonstrate multi-agent workflows."""

    print_section("Multi-Agent Workflows")

    orchestrator = AgentOrchestrator()

    # Workflow 1: Intelligent Incident Response
    print_section("Workflow 1: Intelligent Incident Response")
    print("Uses: Query + RCA + Compliance + Learning Agents")

    incident_result = await orchestrator.multi_agent_workflow(
        'intelligent_incident_response',
        {
            'incident_description': 'Multiple API failures reported in water quality monitoring service',
            'error_message': 'Service unavailable - connection pool exhausted',
            'stack_trace': 'ConnectionPoolError at api_handler.py:89'
        }
    )
    print_result("Incident Response", incident_result)

    # Workflow 2: Compliance with RCA
    print_section("Workflow 2: Compliance Monitoring with Auto-RCA")
    print("Uses: Compliance + RCA + Multi-Step Reasoning Agents")

    compliance_workflow = await orchestrator.multi_agent_workflow(
        'compliance_with_rca',
        {
            'operation_type': 'data_transfer',
            'data_classification': 'sensitive',
            'source': 'eu-west-1',
            'destination': 'us-east-1',
            'encryption': False,  # This will likely trigger violations
            'frameworks': ['GDPR', 'SOC2']
        }
    )
    print_result("Compliance Workflow", compliance_workflow)

    # Workflow 3: Conversational Problem Solving
    print_section("Workflow 3: Conversational Problem Solving")
    print("Uses: Memory + Multi-Step Reasoning + Learning Agents")

    problem_solving = await orchestrator.multi_agent_workflow(
        'conversational_problem_solving',
        {
            'problem': 'Design a strategy to improve response times across all monitoring services',
            'conversation_id': 'problem-solving-demo',
            'user_id': 'engineer-456'
        }
    )
    print_result("Problem Solving", problem_solving)

    return orchestrator


async def demo_parallel_agents():
    """Demonstrate parallel agent execution."""

    print_section("Parallel Agent Execution")
    print("Running multiple agents simultaneously for efficiency")

    orchestrator = AgentOrchestrator()

    # Execute multiple agents in parallel
    parallel_tasks = [
        {
            'agent_name': 'natural_language_query',
            'request_data': {'query': 'List all facilities in California'}
        },
        {
            'agent_name': 'compliance_autopilot',
            'request_data': {
                'operation_type': 'data_audit',
                'frameworks': ['SOC2']
            }
        },
        {
            'agent_name': 'root_cause_analysis',
            'request_data': {
                'error_message': 'High latency detected',
                'context': {'service': 'monitoring'}
            }
        }
    ]

    results = await orchestrator.execute_parallel_agents(parallel_tasks)

    print(f"\nExecuted {len(results)} agents in parallel:")
    for i, result in enumerate(results, 1):
        print(f"\n  Agent {i} Result:")
        print(f"  {json.dumps(result, indent=4, default=str)[:300]}...")

    return orchestrator


async def main():
    """Main application entry point."""

    print("\n")
    print("╔" + "═"*68 + "╗")
    print("║" + " "*15 + "ChainSync Unified AI Agent v2.0" + " "*22 + "║")
    print("║" + " "*11 + "Multi-Agent Orchestration Platform" + " "*22 + "║")
    print("╚" + "═"*68 + "╝")

    # Validate configuration
    if not Config.validate():
        print("\n⚠️  Configuration validation failed")
        print("    Note: Some demos will work without OpenAI API key (using mock data)")
        print("    Set OPENAI_API_KEY in .env for full functionality\n")

    try:
        # Demo 1: Individual Specialized Agents
        orchestrator = await demo_specialized_agents()

        # Demo 2: Multi-Agent Workflows
        await demo_multi_agent_workflows()

        # Demo 3: Parallel Execution
        await demo_parallel_agents()

        # System Status
        print_section("System Status")
        status = await orchestrator.get_system_status()
        print_result("Agent Orchestrator Status", status)

        print("\n" + "="*70)
        print("✅ All demonstrations completed successfully!")
        print("="*70)
        print("\n📊 Agent Summary:")
        print(f"   • 6 Specialized Agents initialized")
        print(f"   • 3 Multi-Agent Workflows demonstrated")
        print(f"   • Parallel execution capability verified")
        print(f"   • System Status: {status['orchestrator']['status'].upper()}")

        print("\n🚀 Ready for:")
        print("   • MuleSoft integration layer")
        print("   • CloudHub deployment")
        print("   • Production workloads")
        print("   • Enterprise-scale operations")

        print("\n💡 Next Steps:")
        print("   1. Configure OpenAI API key in .env")
        print("   2. Set up ChainSync API connection")
        print("   3. Deploy to CloudHub environment")
        print("   4. Integrate with MuleSoft flows")

    except Exception as e:
        logger.error(f"Error during demo: {str(e)}", exc_info=True)
        print(f"\n❌ Error: {str(e)}")
        print("   Check logs for details")


if __name__ == "__main__":
    asyncio.run(main())