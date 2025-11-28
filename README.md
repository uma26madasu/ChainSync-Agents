# ChainSync Multi-Domain Enterprise Platform

> **Multi-Agent AI Orchestration with MuleSoft Integration**

ChainSync is a comprehensive enterprise integration platform that combines specialized AI agents with MuleSoft integration patterns to transform manual operational workflows into intelligent, automated, cross-domain coordination systems.

## 🤖 Specialized AI Agents

ChainSync includes 7 specialized AI agents, each designed for specific enterprise needs:

### 1. **Continuous Learning Agent**
Learns from interactions and improves system performance over time.

**Capabilities:**
- Stores and analyzes interaction patterns
- Identifies recurring issues and optimization opportunities
- Adapts responses based on historical feedback
- Provides data-driven suggestions for improvements

**Use Cases:**
- System optimization based on usage patterns
- Automated performance improvement
- Pattern recognition in user behavior
- Feedback-driven enhancement

### 2. **Root Cause Analysis Agent**
Identifies underlying causes of failures and provides remediation steps.

**Capabilities:**
- Analyzes error logs and stack traces
- Performs 5 Whys and Fishbone analysis
- Distinguishes between symptoms and root causes
- Generates actionable remediation recommendations

**Use Cases:**
- Incident response and troubleshooting
- Failure analysis and prevention
- System reliability improvement
- Post-mortem analysis

### 3. **Natural Language Query Agent**
Processes natural language questions and retrieves data intelligently.

**Capabilities:**
- Understands natural language queries
- Converts queries to structured API calls
- Retrieves and formats data from multiple sources
- Provides conversational responses

**Use Cases:**
- Business intelligence queries
- Data exploration without technical knowledge
- Report generation from natural language
- Conversational data access

### 4. **Compliance Autopilot Agent**
Automatically monitors and ensures regulatory compliance.

**Capabilities:**
- Monitors operations for compliance violations
- Checks against multiple frameworks (SOC2, GDPR, HIPAA, ISO27001, PCI-DSS)
- Generates compliance reports
- Provides automated remediation guidance

**Use Cases:**
- Continuous compliance monitoring
- Regulatory audit preparation
- Risk assessment and mitigation
- Automated compliance reporting

### 5. **Memory-Enabled Agent**
Maintains conversation history and provides context-aware interactions.

**Capabilities:**
- Persistent conversation memory
- User preference tracking
- Context-aware responses
- Long-term memory across sessions

**Use Cases:**
- Conversational AI interfaces
- Personalized user experiences
- Context-aware assistance
- Multi-turn problem solving

### 6. **Multi-Step Reasoning Agent**
Breaks down complex problems and reasons through them step-by-step.

**Capabilities:**
- Decomposes complex queries into sub-tasks
- Sequential reasoning with explanation
- Maintains reasoning chain for transparency
- Synthesizes comprehensive solutions

**Use Cases:**
- Complex problem solving
- Strategic planning
- Decision support
- Analytical tasks requiring multiple steps

### 7. **Meeting Context Agent (Slotify Integration)**
Provides context for meetings scheduled by Slotify based on ChainSync alerts.

**Capabilities:**
- Links Slotify meetings to ChainSync alerts
- Explains why meetings were automatically scheduled
- Generates recommended discussion points
- Provides pre-meeting summaries for attendees
- Calculates meeting urgency based on alert severity
- Suggests appropriate attendees based on alert type
- Generates post-meeting summaries with action items

**Use Cases:**
- Automated meeting context from system alerts
- Pre-meeting briefings for stakeholders
- Alert-driven meeting scheduling explanation
- Post-incident review meeting preparation
- Compliance violation review meetings

**Supported Alert Types:**
- Compliance Violations
- System Failures
- Performance Degradation
- Security Incidents
- Data Quality Issues
- Integration Failures
- Capacity Warnings

## 🎯 Multi-Agent Workflows

The agents work together in coordinated workflows:

### Intelligent Incident Response
**Agents:** Query + RCA + Compliance + Learning
- Processes incident descriptions
- Performs root cause analysis
- Checks for compliance violations
- Learns from incident patterns

### Compliance Monitoring with Auto-RCA
**Agents:** Compliance + RCA + Multi-Step Reasoning
- Monitors operations for compliance
- Analyzes root causes of violations
- Develops remediation plans automatically

### Conversational Problem Solving
**Agents:** Memory + Multi-Step Reasoning + Learning
- Maintains conversation context
- Reasons through complex problems
- Learns from solution effectiveness

### Alert to Meeting (Slotify Integration)
**Agents:** RCA + Compliance + Meeting Context + Learning
- Processes ChainSync alerts automatically
- Performs root cause analysis on the alert
- Checks for compliance implications
- Creates Slotify meeting with full context explanation
- Generates discussion points and pre-meeting summary
- Learns from alert patterns for future improvements

---

## 🚨 Alert-Based Meeting Scheduler (Production Ready!)

**Automatically schedule meetings with the right authorities based on ChainSync alert severity and type.**

### ✨ Key Features

- ✅ **Automatic Meeting Scheduling** - Triggers Slotify meetings based on alert severity
- ✅ **Smart Authority Selection** - Invites the right stakeholders based on alert type
- ✅ **AI-Powered Context** - Generates meeting agendas, discussion points, and summaries
- ✅ **Escalation Logic** - Automatically escalates critical issues to management
- ✅ **Multi-Framework Compliance** - Tracks SOC2, GDPR, HIPAA, ISO27001, PCI-DSS violations
- ✅ **Full Database Tracking** - Maintains audit trail of all alerts and meetings

### 🎯 How It Works

```
ChainSync Alert → AI Analysis → Meeting Scheduled → Authorities Notified
```

When a ChainSync alert is received:
1. **Root Cause Analysis** - AI identifies the underlying issue
2. **Compliance Check** - Verifies regulatory implications
3. **Urgency Calculation** - Determines meeting priority (CRITICAL/HIGH/MEDIUM/LOW)
4. **Authority Selection** - Automatically invites appropriate stakeholders
5. **Context Generation** - Creates meeting agenda and discussion points
6. **Slotify Integration** - Schedules meeting and sends invitations

### 📋 Alert Types & Authorities

| Alert Type | Severity | Response Time | Key Attendees |
|-----------|----------|---------------|---------------|
| **Security Incident** | CRITICAL | < 1 hour | Security Team, CISO, Legal, Exec Sponsor |
| **System Failure** | CRITICAL | < 1 hour | DevOps, SRE, Engineering Lead, Management |
| **Compliance Violation** | HIGH | < 4 hours | Compliance Officer, Legal, Security, Exec |
| **Integration Failure** | HIGH | < 4 hours | Integration Team, API Team, MuleSoft Admin |
| **Performance Degradation** | MEDIUM | < 24 hours | Engineering, DevOps, Product |
| **Data Quality Issue** | MEDIUM | < 24 hours | Data Engineering, Analytics, QA |
| **Capacity Warning** | LOW | < 48 hours | Infrastructure, DevOps, FinOps |

### ⚡ Quick Start

**1. Send an Alert Webhook**
```bash
curl -X POST http://localhost:8000/webhooks/chainsync/alert \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-webhook-api-key" \
  -d '{
    "alert_id": "SEC-2025-001",
    "alert_type": "security_incident",
    "severity": "critical",
    "description": "Unauthorized access attempt detected",
    "affected_systems": ["prod-db-01", "auth-service"],
    "detected_at": "2025-11-28T10:00:00Z",
    "compliance_frameworks": ["SOC2", "ISO27001"]
  }'
```

**2. Meeting Automatically Scheduled** ✅
- Urgency: CRITICAL
- Response Time: < 1 hour
- Duration: 60 minutes
- Attendees: Security Team, CISO, Legal, Management, Executive Sponsor
- AI-generated agenda and discussion points included

### 🧪 Run the Demo

```bash
# Demo all alert types
python examples/alert_based_meeting_demo.py all

# Show authority mappings
python examples/alert_based_meeting_demo.py mappings

# Test specific alert type
python examples/alert_based_meeting_demo.py critical_security
```

### 📚 Documentation

- **[Complete Guide](docs/ALERT_BASED_MEETING_SCHEDULER.md)** - Full documentation with examples
- **[Quick Reference](docs/ALERT_AUTHORITIES_QUICK_REFERENCE.md)** - Cheat sheet for alert types
- **[Configuration](config/alert_authorities.yaml)** - Customize authority lists

### 🎨 Customization

Edit `config/alert_authorities.yaml` to customize:
- Authority lists for each alert type
- Escalation rules
- Meeting durations
- Notification settings
- Custom alert types

---

## 🏗️ Architecture Overview

### 🐍 Python AI Agent Layer
- **Agent Orchestrator** - Coordinates multiple specialized agents
- **OpenAI GPT-4 Integration** - Advanced AI capabilities
- **Async Architecture** - High-performance concurrent operations
- **Modular Design** - Easy to extend and customize

### 🔗 MuleSoft Integration Layer (Ready for Integration)
- **API-Led Connectivity** - 15+ external data sources
- **DataWeave Transformations** - Enterprise-grade data processing
- **Webhook Processing** - Real-time event handling
- **CloudHub Deployment** - Production-ready infrastructure

## 🚀 Quick Start

### 1. Environment Setup
```bash
# Clone repository
git clone https://github.com/uma26madasu/ChainSync-Agents.git
cd ChainSync-Agents

# Create virtual environment
python -m venv chainsync_env
source chainsync_env/bin/activate  # Linux/Mac
# or
chainsync_env\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=your_api_key_here
```

### 3. Run Demo
```bash
python main.py
```

This will demonstrate:
- All 7 specialized agents (including Meeting Context Agent for Slotify)
- Multi-agent workflows
- Parallel agent execution
- System status and capabilities

### 4. Start Webhook Server (For ChainSync & Slotify Integration)
```bash
# Start webhook server on default port 8000
python main.py --webhook

# Start on custom port
python main.py --webhook --port 8080
```

The webhook server provides real-time integration with:
- **ChainSync** - Receives alert notifications
- **Slotify** - Receives meeting scheduling notifications

## 🔗 Webhook Integration

### Overview

The webhook server enables real-time integration between ChainSync alerts and Slotify meetings through AI-powered automation.

**Flow:**
```
ChainSync Alert → Webhook → AI Agents → Meeting Context → Slotify
```

### Webhook Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/webhooks/chainsync/alert` | POST | Receive ChainSync alerts |
| `/webhooks/slotify/meeting` | POST | Receive Slotify meeting notifications |
| `/webhooks/chainsync/alert-batch` | POST | Batch process multiple alerts |
| `/health` | GET | Health check |
| `/status` | GET | System status |
| `/agents/list` | GET | List all agents |
| `/workflows/list` | GET | List all workflows |

### ChainSync Alert Webhook

**Endpoint:** `POST /webhooks/chainsync/alert`

**Payload Example:**
```json
{
  "alert_id": "chainsync-alert-12345",
  "alert_type": "system_failure",
  "severity": "critical",
  "description": "Database connection pool exhausted",
  "affected_systems": ["API Gateway", "User Service", "Database"],
  "detected_at": "2025-11-26T10:30:00Z",
  "context": {
    "connection_count": 100,
    "max_connections": 100,
    "error_rate": 0.45
  },
  "compliance_frameworks": ["SOC2", "ISO27001"]
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Alert chainsync-alert-12345 processed successfully",
  "data": {
    "alert_id": "chainsync-alert-12345",
    "meeting_id": "slotify_meeting_1732617000.123",
    "urgency": {
      "level": "CRITICAL",
      "score": 1.0,
      "recommended_response_time": "< 1 hour"
    },
    "workflow_result": {
      "root_cause_analysis": {...},
      "compliance_check": {...},
      "meeting_context": {...}
    }
  },
  "timestamp": "2025-11-26T10:30:15Z"
}
```

**What Happens:**
1. Alert is received and validated
2. RCA Agent analyzes root cause
3. Compliance Agent checks for violations
4. Meeting Context Agent generates meeting briefing
5. Learning Agent records pattern
6. Returns meeting context with explanation

### Slotify Meeting Webhook

**Endpoint:** `POST /webhooks/slotify/meeting`

**Payload Example:**
```json
{
  "meeting_id": "slotify-meeting-789",
  "title": "Critical System Review",
  "scheduled_time": "2025-11-26T15:00:00Z",
  "attendees": [
    "devops@company.com",
    "sre@company.com",
    "cto@company.com"
  ],
  "alert_reference": "chainsync-alert-12345",
  "organizer": "slotify@company.com",
  "duration_minutes": 60
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Meeting slotify-meeting-789 context generated",
  "data": {
    "meeting_id": "slotify-meeting-789",
    "meeting_context": {
      "why_scheduled": "This meeting was scheduled because...",
      "discussion_points": [
        "1. Review database connection pool configuration",
        "2. Implement connection pooling best practices",
        "3. Set up monitoring for connection exhaustion"
      ],
      "urgency": "CRITICAL",
      "recommended_duration": "60 minutes"
    },
    "explanation": "📅 Meeting: Critical System Review\n..."
  },
  "timestamp": "2025-11-26T10:31:00Z"
}
```

### Setting Up Webhooks

#### In ChainSync (MuleSoft)

Configure ChainSync to send alerts to your webhook endpoint:

```xml
<!-- MuleSoft Flow Example -->
<flow name="send-alert-to-ai-agents">
  <http:request method="POST"
                url="http://your-server:8000/webhooks/chainsync/alert">
    <http:body><![CDATA[#[payload]]]></http:body>
    <http:headers>
      <http:header key="Content-Type" value="application/json"/>
    </http:headers>
  </http:request>
</flow>
```

#### In Slotify

Configure Slotify webhook URL in settings:
```
Webhook URL: http://your-server:8000/webhooks/slotify/meeting
Method: POST
Content-Type: application/json
```

### Testing Webhooks

#### Test ChainSync Alert
```bash
curl -X POST http://localhost:8000/webhooks/chainsync/alert \
  -H "Content-Type: application/json" \
  -d '{
    "alert_id": "test-alert-001",
    "alert_type": "system_failure",
    "severity": "high",
    "description": "Test alert for webhook integration",
    "affected_systems": ["Test Service"],
    "detected_at": "2025-11-26T10:00:00Z",
    "context": {}
  }'
```

#### Test Slotify Meeting
```bash
curl -X POST http://localhost:8000/webhooks/slotify/meeting \
  -H "Content-Type: application/json" \
  -d '{
    "meeting_id": "test-meeting-001",
    "title": "Test Meeting",
    "scheduled_time": "2025-11-26T15:00:00Z",
    "attendees": ["test@company.com"],
    "alert_reference": "test-alert-001"
  }'
```

### API Documentation

Once the webhook server is running, access interactive API documentation:

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

## 💻 Usage Examples

### Using Individual Agents

```python
from chainsync.agent_orchestrator import AgentOrchestrator

# Initialize orchestrator
orchestrator = AgentOrchestrator()

# Natural Language Query
result = await orchestrator.route_request('query', {
    'query': 'What are the top 5 facilities with highest risk?',
    'data_source': 'chainsync'
})

# Root Cause Analysis
rca = await orchestrator.route_request('failure_analysis', {
    'error_message': 'Database connection timeout',
    'stack_trace': '...',
    'context': {'service': 'monitoring'}
})

# Compliance Check
compliance = await orchestrator.route_request('compliance', {
    'operation_type': 'data_processing',
    'frameworks': ['GDPR', 'HIPAA']
})

# Memory-Enabled Chat
chat = await orchestrator.route_request('chat', {
    'message': 'Help me analyze water quality trends',
    'conversation_id': 'conv-123',
    'user_id': 'user-456'
})

# Multi-Step Reasoning
solution = await orchestrator.route_request('reasoning', {
    'problem': 'How to reduce energy consumption?',
    'max_steps': 5
})

# Meeting Context (Slotify Integration)
meeting_context = await orchestrator.route_request('meeting', {
    'meeting_data': {
        'meeting_id': 'slotify-123',
        'title': 'Critical System Review',
        'scheduled_time': '2025-11-25T10:00:00Z',
        'attendees': ['devops@company.com', 'sre@company.com']
    },
    'alert_data': {
        'alert_id': 'alert-456',
        'alert_type': 'system_failure',
        'severity': 'critical',
        'description': 'Database connection pool exhausted',
        'affected_systems': ['API Gateway', 'User Service'],
        'detected_at': '2025-11-24T15:30:00Z'
    }
})
```

### Using Multi-Agent Workflows

```python
# Intelligent Incident Response
incident = await orchestrator.multi_agent_workflow(
    'intelligent_incident_response',
    {
        'incident_description': 'API failures in monitoring service',
        'error_message': 'Connection pool exhausted',
        'stack_trace': '...'
    }
)

# Compliance with Auto-RCA
compliance_workflow = await orchestrator.multi_agent_workflow(
    'compliance_with_rca',
    {
        'operation_type': 'data_transfer',
        'frameworks': ['GDPR', 'SOC2']
    }
)

# Alert to Meeting (Slotify Integration)
alert_meeting = await orchestrator.multi_agent_workflow(
    'alert_to_meeting',
    {
        'alert_data': {
            'alert_id': 'chainsync-alert-789',
            'alert_type': 'compliance_violation',
            'severity': 'high',
            'description': 'GDPR data retention policy exceeded for customer records',
            'affected_systems': ['Customer Database', 'Backup Systems'],
            'context': {
                'violation_type': 'data_retention',
                'records_affected': 15000,
                'days_exceeded': 30
            }
        },
        'meeting_data': {
            'meeting_id': 'slotify-meeting-001',
            'attendees': ['compliance@company.com', 'legal@company.com']
        }
    }
)
# Returns: meeting context, RCA results, compliance check, and full explanation
print(alert_meeting['meeting_explanation'])
```

### Direct Agent Access

```python
# Get specific agent
rca_agent = orchestrator.get_agent('root_cause_analysis')

# Use agent directly
result = await rca_agent.analyze_failure({
    'error_message': 'High latency detected',
    'context': {...}
})
```

## 📊 System Requirements

### Python Environment
- Python 3.8+
- OpenAI API key (for full functionality)
- 4GB+ RAM recommended
- Internet connection for OpenAI API

### Dependencies
All dependencies are listed in `requirements.txt`:
- openai==1.54.0
- fastapi==0.108.0
- uvicorn==0.25.0
- pandas==2.2.0
- numpy==1.26.0
- httpx==0.27.0
- pydantic==2.5.0
- python-dotenv==1.0.0
- pytest==7.4.0 (development)

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_ai_agent.py

# Run with coverage
python -m pytest --cov=chainsync tests/
```

## 📁 Project Structure

```
ChainSync-Agents/
├── main.py                                    # Application entry point with demos
├── requirements.txt                           # Python dependencies
├── .env.example                               # Environment configuration template
├── chainsync/                                 # Core application package
│   ├── __init__.py                           # Package initialization
│   ├── config.py                             # Configuration management
│   ├── ai_agent.py                           # Legacy AI agent (deprecated)
│   ├── domain_manager.py                     # Domain-specific logic handler
│   ├── specialized_agents.py                 # 7 specialized AI agents
│   ├── agent_orchestrator.py                 # Multi-agent coordination
│   ├── webhook_server.py                     # Webhook endpoints for ChainSync/Slotify
│   ├── api_clients.py                        # SlotifyAPI & ChainSync API clients
│   ├── database.py                           # Database models and repositories
│   └── security.py                           # Authentication and security
├── config/                                    # Configuration files
│   └── alert_authorities.yaml                # Alert-based meeting scheduler config
├── examples/                                  # Example scripts
│   └── alert_based_meeting_demo.py           # Alert-to-meeting demo script
├── docs/                                      # Documentation
│   ├── architecture.md                       # Architecture design
│   ├── api_documentation.md                  # API specifications
│   ├── deployment_guide.md                   # Deployment instructions
│   ├── ALERT_BASED_MEETING_SCHEDULER.md      # Alert scheduler complete guide
│   ├── ALERT_AUTHORITIES_QUICK_REFERENCE.md  # Quick reference cheat sheet
│   └── INTEGRATION_GUIDE.md                  # Integration guide
└── tests/                                     # Test suite
    ├── test_ai_agent.py                      # AI agent tests
    ├── test_integration.py                   # Integration tests
    ├── test_meeting_context_agent.py         # Meeting context agent tests
    └── test_webhook_server.py                # Webhook server tests
```

## 🔧 Configuration Options

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | OpenAI API key for GPT-4 | - | Yes* |
| `CHAINSYNC_API_URL` | ChainSync API endpoint | http://localhost:8081/api | No |
| `CHAINSYNC_TIMEOUT` | API timeout (seconds) | 10 | No |
| `PYTHON_AGENT_PORT` | Agent server port | 8000 | No |
| `DEBUG` | Enable debug mode | False | No |
| `LOG_LEVEL` | Logging level | INFO | No |

\* Required for full functionality. Some features work with mock data without API key.

## 🚀 Deployment

### Local Development
```bash
python main.py
```

### Production Deployment

1. **Set up environment variables** in your production environment
2. **Configure OpenAI API key** securely
3. **Deploy to CloudHub** or your preferred platform
4. **Integrate with MuleSoft flows** for enterprise connectivity

See `docs/deployment_guide.md` for detailed deployment instructions.

## 🔐 Security Considerations

- Store API keys securely (use environment variables, never commit to git)
- Implement authentication for production deployments
- Use HTTPS for all external communications
- Follow compliance framework requirements (GDPR, HIPAA, etc.)
- Regularly update dependencies for security patches

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Author

**Uma Maheswararao Madasu**

## 🙏 Acknowledgments

- OpenAI for GPT-4 capabilities
- MuleSoft for enterprise integration patterns
- Python community for excellent async libraries

## 📞 Support

For issues, questions, or contributions, please open an issue on GitHub.

## 🗺️ Roadmap

- [ ] FastAPI REST endpoints for agent access
- [ ] Web UI for agent management
- [ ] Enhanced learning algorithms for Continuous Learning Agent
- [ ] Additional compliance frameworks
- [ ] Vector database integration for better memory
- [ ] Advanced multi-agent coordination patterns
- [ ] Real-time monitoring dashboard
- [ ] Integration with more data sources

---

**Version:** 2.0.0
**Last Updated:** November 2025
**Status:** Production Ready (Python AI Layer) | Integration Ready (MuleSoft Layer)
