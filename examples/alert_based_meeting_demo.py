"""
Alert-Based Meeting Scheduler Demo

This script demonstrates how ChainSync alerts automatically trigger
meeting scheduling in Slotify with concerned authorities.

Features Demonstrated:
1. Alert severity-based urgency calculation
2. Automatic attendee selection based on alert type
3. AI-generated meeting context and discussion points
4. Integration with ChainSync and Slotify APIs
"""

import asyncio
import json
from datetime import datetime, timedelta
from chainsync.webhook_server import app
from chainsync.api_clients import SlotifyAPIClient, ChainSyncAPIClient
from chainsync.agent_orchestrator import AgentOrchestrator
from chainsync.database import init_database, get_db, MeetingRepository, AlertRepository


# Example Alerts with Different Severity Levels
EXAMPLE_ALERTS = {
    "critical_security": {
        "alert_id": "SEC-2025-001",
        "alert_type": "security_incident",
        "severity": "critical",
        "description": "Unauthorized access attempt detected on production database. Multiple failed authentication attempts from unknown IP addresses.",
        "affected_systems": ["prod-db-01", "prod-db-02", "auth-service"],
        "detected_at": datetime.now().isoformat(),
        "context": {
            "ip_addresses": ["192.168.1.100", "10.0.0.50"],
            "failed_attempts": 150,
            "time_window": "15 minutes"
        },
        "compliance_frameworks": ["SOC2", "ISO27001", "GDPR"]
    },

    "high_compliance": {
        "alert_id": "COMP-2025-042",
        "alert_type": "compliance_violation",
        "severity": "high",
        "description": "PCI-DSS compliance violation detected: unencrypted payment data found in log files.",
        "affected_systems": ["payment-gateway", "logging-service"],
        "detected_at": datetime.now().isoformat(),
        "context": {
            "violation_type": "data_exposure",
            "affected_records": 247,
            "framework": "PCI-DSS"
        },
        "compliance_frameworks": ["PCI-DSS"]
    },

    "medium_performance": {
        "alert_id": "PERF-2025-123",
        "alert_type": "performance_degradation",
        "severity": "medium",
        "description": "API response time increased by 300% over the last 2 hours. Users experiencing slowness.",
        "affected_systems": ["api-gateway", "microservice-cluster"],
        "detected_at": datetime.now().isoformat(),
        "context": {
            "baseline_latency": "150ms",
            "current_latency": "450ms",
            "affected_endpoints": ["/api/users", "/api/transactions"]
        }
    },

    "low_capacity": {
        "alert_id": "INFRA-2025-089",
        "alert_type": "capacity_warning",
        "severity": "low",
        "description": "Database storage capacity approaching 70% threshold. Proactive scaling recommended.",
        "affected_systems": ["prod-db-01"],
        "detected_at": datetime.now().isoformat(),
        "context": {
            "current_usage": "68%",
            "threshold": "70%",
            "estimated_time_to_full": "45 days"
        }
    }
}


async def simulate_alert_webhook(alert_data: dict):
    """
    Simulate receiving an alert webhook from ChainSync.

    This demonstrates the full flow:
    1. Alert received via webhook
    2. AI agents analyze the alert
    3. Meeting is automatically created in Slotify
    4. Concerned authorities are notified
    5. Meeting context is generated
    """
    print(f"\n{'='*80}")
    print(f"🚨 SIMULATING ALERT: {alert_data['alert_id']}")
    print(f"{'='*80}")
    print(f"Type: {alert_data['alert_type']}")
    print(f"Severity: {alert_data['severity'].upper()}")
    print(f"Description: {alert_data['description']}")
    print(f"Affected Systems: {', '.join(alert_data['affected_systems'])}")
    print(f"\n{'─'*80}")

    # Initialize orchestrator
    orchestrator = AgentOrchestrator()
    slotify_client = SlotifyAPIClient()
    chainsync_client = ChainSyncAPIClient()

    # Step 1: Run AI agent workflow
    print("\n🤖 Running AI Agent Analysis...")
    workflow_result = await orchestrator.multi_agent_workflow(
        'alert_to_meeting',
        {
            'alert_data': alert_data,
            'meeting_data': {}
        }
    )

    meeting_context = workflow_result.get('meeting_context', {})

    print(f"\n✓ Root Cause Analysis Complete")
    print(f"  Root Cause: {workflow_result.get('root_cause_analysis', {}).get('root_cause', 'Unknown')}")

    print(f"\n✓ Compliance Check Complete")
    print(f"  Status: {workflow_result.get('compliance_check', {}).get('overall_status', 'Unknown')}")

    # Step 2: Display meeting details
    print(f"\n📅 MEETING SCHEDULED IN SLOTIFY")
    print(f"{'─'*80}")
    print(f"Title: {meeting_context.get('meeting_title')}")
    print(f"Urgency: {meeting_context.get('urgency', {}).get('level')} (Score: {meeting_context.get('urgency', {}).get('score')})")
    print(f"Response Time: {meeting_context.get('urgency', {}).get('recommended_response_time')}")
    print(f"Duration: {meeting_context.get('recommended_duration')}")

    # Step 3: Display concerned authorities
    print(f"\n👥 CONCERNED AUTHORITIES INVITED:")
    print(f"{'─'*80}")
    for attendee in meeting_context.get('suggested_attendees', []):
        print(f"  • {attendee}")

    # Step 4: Display why meeting was scheduled
    print(f"\n💡 WHY THIS MEETING WAS SCHEDULED:")
    print(f"{'─'*80}")
    print(f"{meeting_context.get('why_scheduled', 'No explanation provided')}")

    # Step 5: Display discussion points
    print(f"\n📋 DISCUSSION POINTS:")
    print(f"{'─'*80}")
    for i, point in enumerate(meeting_context.get('discussion_points', []), 1):
        print(f"{i}. {point}")

    # Step 6: Display pre-meeting summary
    print(f"\n📄 PRE-MEETING SUMMARY:")
    print(f"{'─'*80}")
    print(f"{meeting_context.get('pre_meeting_summary', 'No summary available')}")

    print(f"\n{'='*80}")
    print(f"✅ Meeting successfully scheduled!")
    print(f"{'='*80}\n")

    return meeting_context


async def demo_all_alert_types():
    """Run demo for all alert types to show different meeting configurations."""
    print("\n" + "="*80)
    print("ALERT-BASED MEETING SCHEDULER DEMONSTRATION")
    print("="*80)
    print("\nThis demo shows how different alert types and severities")
    print("automatically schedule meetings with appropriate authorities.\n")

    # Initialize database
    init_database()

    for alert_name, alert_data in EXAMPLE_ALERTS.items():
        await simulate_alert_webhook(alert_data)
        await asyncio.sleep(1)  # Brief pause between demos

    print("\n" + "="*80)
    print("DEMO COMPLETE")
    print("="*80)
    print("\n📊 SUMMARY:")
    print(f"  • {len(EXAMPLE_ALERTS)} alerts processed")
    print(f"  • {len(EXAMPLE_ALERTS)} meetings automatically scheduled")
    print(f"  • All concerned authorities notified")
    print("\n💡 Key Features Demonstrated:")
    print("  ✓ Severity-based urgency calculation")
    print("  ✓ Automatic attendee selection")
    print("  ✓ AI-generated meeting context")
    print("  ✓ Compliance framework integration")
    print("  ✓ Root cause analysis")
    print("  ✓ Discussion point generation")
    print("\n")


async def demo_single_alert(alert_type: str = "critical_security"):
    """Demo a single alert type."""
    init_database()

    if alert_type not in EXAMPLE_ALERTS:
        print(f"❌ Unknown alert type: {alert_type}")
        print(f"Available types: {', '.join(EXAMPLE_ALERTS.keys())}")
        return

    alert_data = EXAMPLE_ALERTS[alert_type]
    await simulate_alert_webhook(alert_data)


async def show_authority_mappings():
    """Display the authority mappings for all alert types."""
    orchestrator = AgentOrchestrator()
    meeting_agent = orchestrator.get_agent('meeting_context')

    print("\n" + "="*80)
    print("CONCERNED AUTHORITIES MAPPING")
    print("="*80)
    print("\nThis shows which authorities are automatically invited for each alert type.\n")

    for alert_type, info in meeting_agent.alert_types.items():
        print(f"📌 {alert_type.upper().replace('_', ' ')}")
        print(f"   Category: {info['category']}")
        print(f"   Severity Weight: {info['severity_weight']}")
        print(f"   Base Attendees:")
        for attendee in info['typical_attendees']:
            print(f"      • {attendee}")
        print()

    print("📝 ESCALATION RULES:")
    print("   • Critical/High severity → +Management")
    print("   • Critical/High compliance/security → +Executive Sponsor")
    print("\n" + "="*80 + "\n")


# CLI Interface
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "all":
            asyncio.run(demo_all_alert_types())
        elif command == "mappings":
            asyncio.run(show_authority_mappings())
        elif command in EXAMPLE_ALERTS:
            asyncio.run(demo_single_alert(command))
        else:
            print(f"Unknown command: {command}")
            print("\nUsage:")
            print("  python alert_based_meeting_demo.py all              # Demo all alert types")
            print("  python alert_based_meeting_demo.py mappings         # Show authority mappings")
            print("  python alert_based_meeting_demo.py critical_security # Demo specific alert")
            print("\nAvailable alert types:")
            for alert_type in EXAMPLE_ALERTS.keys():
                print(f"  - {alert_type}")
    else:
        # Default: run all demos
        asyncio.run(demo_all_alert_types())
