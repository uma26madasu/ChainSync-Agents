# Complete Integration Guide: ChainSync + AI Agents + Slotify

## Overview

This guide provides complete instructions for integrating ChainSync alerts with AI agents and Slotify meeting scheduling through webhooks, with full security, persistence, and MuleSoft integration.

## Architecture

```
┌──────────────┐         ┌─────────────────┐         ┌──────────────┐
│   ChainSync  │────────▶│   AI Agents     │────────▶│   Slotify    │
│  (MuleSoft)  │  Alert  │  (Webhook API)  │ Meeting │  (Meetings)  │
└──────────────┘         └─────────────────┘         └──────────────┘
                                 │
                                 ▼
                         ┌───────────────┐
                         │   Database    │
                         │  (SQLAlchemy) │
                         └───────────────┘
```

## Features Implemented

### ✅ Priority 1: Complete Slotify Integration
- **Slotify API Client**: Full CRUD operations for meetings
- **Auto-create meetings**: AI agents automatically create Slotify meetings for alerts
- **Meeting URLs**: URLs returned to ChainSync for tracking

### ✅ Priority 2: Webhook Security
- **API Key Authentication**: X-API-Key header validation
- **HMAC Signature Verification**: HMAC-SHA256 request signing
- **Rate Limiting**: In-memory rate limiter (100 requests/minute per IP)
- **Timestamp Validation**: Prevents replay attacks (5-minute window)

### ✅ Priority 3: Persistence Layer
- **Database Models**: SQLAlchemy models for meetings, alerts, learning data
- **Meeting History**: Complete audit trail of all meetings
- **Alert Processing**: Track all processed alerts with RCA results
- **Learning Data**: Store agent learning patterns for continuous improvement
- **Webhook Logs**: Full request/response logging

### ✅ Priority 4: MuleSoft Flows
- **Alert to Webhook**: Send ChainSync alerts to AI agents
- **Response Handler**: Process AI agent responses
- **Retry Logic**: Exponential backoff for failed requests
- **Batch Processing**: Handle multiple alerts efficiently

## Quick Start

### 1. Environment Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Configure API keys in .env
vi .env
```

### 2. Required Configuration

```bash
# .env file
OPENAI_API_KEY=sk-your-openai-key
CHAINSYNC_API_KEY=your-chainsync-key
SLOTIFY_API_KEY=your-slotify-key
WEBHOOK_API_KEY=your-secure-webhook-key
WEBHOOK_SECRET_KEY=your-hmac-secret-key
DATABASE_URL=sqlite:///./chainsync_agents.db
```

### 3. Start Webhook Server

```bash
python main.py --webhook --port 8000
```

Server will start at: `http://localhost:8000`

## API Endpoints

### Webhook Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/webhooks/chainsync/alert` | POST | Required | Receive ChainSync alerts |
| `/webhooks/slotify/meeting` | POST | Required | Receive Slotify meetings |
| `/health` | GET | None | Health check |
| `/status` | GET | None | System status |
| `/agents/list` | GET | None | List all agents |
| `/meetings/recent` | GET | None | Recent meetings |
| `/alerts/recent` | GET | None | Recent alerts |

### Security Headers

All POST requests must include:

```
X-API-Key: your-webhook-api-key
X-Webhook-Signature: hmac-sha256-signature
X-Webhook-Timestamp: unix-timestamp
```

## Complete Flow Example

### 1. ChainSync Detects Alert

ChainSync MuleSoft flow sends alert to webhook:

```http
POST http://your-server:8000/webhooks/chainsync/alert
X-API-Key: your-webhook-api-key
X-Webhook-Signature: generated-hmac-signature
X-Webhook-Timestamp: 1732617000
Content-Type: application/json

{
  "alert_id": "chainsync-alert-12345",
  "alert_type": "system_failure",
  "severity": "critical",
  "description": "Database connection pool exhausted",
  "affected_systems": ["API Gateway", "User Service"],
  "detected_at": "2025-11-26T10:30:00Z",
  "context": {
    "connection_count": 100,
    "max_connections": 100
  }
}
```

### 2. AI Agents Process Alert

Webhook server triggers workflow:
1. **RCA Agent**: Analyzes root cause
2. **Compliance Agent**: Checks for violations
3. **Meeting Context Agent**: Generates meeting briefing
4. **Learning Agent**: Records pattern

### 3. Slotify Meeting Created

Server calls Slotify API:

```python
meeting = await slotify_client.create_meeting(
    title="[CRITICAL] System Failure Review",
    description="AI-generated context about the alert",
    scheduled_time="2025-11-26T15:00:00Z",
    duration_minutes=60,
    attendees=["devops@company.com", "sre@company.com"],
    alert_reference="chainsync-alert-12345"
)
```

### 4. ChainSync Updated

Server updates ChainSync alert:

```python
await chainsync_client.update_alert_status(
    alert_id="chainsync-alert-12345",
    status="meeting_scheduled",
    meeting_url="https://slotify.com/meetings/xyz",
    notes="AI analysis complete. Meeting scheduled."
)
```

### 5. Database Persisted

All data saved to database:
- Alert record with RCA results
- Meeting record with context
- Learning data for future improvements

### 6. Response Returned

```json
{
  "status": "success",
  "message": "Alert processed and meeting created",
  "data": {
    "alert_id": "chainsync-alert-12345",
    "meeting_id": "slotify-meeting-xyz",
    "meeting_url": "https://slotify.com/meetings/xyz",
    "urgency": {
      "level": "CRITICAL",
      "score": 1.0,
      "recommended_response_time": "< 1 hour"
    }
  },
  "timestamp": "2025-11-26T10:30:15Z"
}
```

## Generating HMAC Signatures

### Python Example

```python
import hmac
import hashlib
import time
import json

def generate_signature(payload, secret_key):
    timestamp = str(int(time.time()))
    payload_str = json.dumps(payload)
    message = f"{timestamp}.{payload_str}"

    signature = hmac.new(
        secret_key.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    return signature, timestamp
```

### MuleSoft DataWeave

```dataweave
%dw 2.0
import * from dw::Crypto
output text/plain
---
HMac(vars.timestamp ++ "." ++ vars.payload, vars.secret_key, "HmacSHA256")
```

## Database Schema

### meetings
- `meeting_id`: Unique meeting identifier
- `alert_id`: Related alert ID
- `meeting_url`: Slotify meeting URL
- `urgency_level`: CRITICAL/HIGH/MEDIUM/LOW
- `why_scheduled`: AI-generated explanation
- `discussion_points`: JSON array of topics
- `status`: scheduled/completed/cancelled

### alerts
- `alert_id`: Unique alert identifier
- `root_cause`: AI-generated root cause
- `compliance_status`: COMPLIANT/NON_COMPLIANT
- `meeting_created`: Boolean
- `meeting_id`: Related meeting ID

### learning_data
- `agent_name`: Which agent learned
- `interaction_type`: Type of interaction
- `patterns_identified`: JSON array of patterns

## MuleSoft Integration

### Configure HTTP Request

In Anypoint Studio:

1. Add HTTP Request connector
2. Set URL: `http://your-server:8000/webhooks/chainsync/alert`
3. Set Method: POST
4. Add Headers:
   - X-API-Key: ${webhook.api.key}
   - X-Webhook-Signature: (calculated)
   - X-Webhook-Timestamp: (current time)

### Example Flow

See `docs/mulesoft_integration_flows.xml` for complete examples.

## Testing

### Test ChainSync Alert

```bash
curl -X POST http://localhost:8000/webhooks/chainsync/alert \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-webhook-api-key" \
  -d '{
    "alert_id": "test-001",
    "alert_type": "system_failure",
    "severity": "high",
    "description": "Test alert",
    "affected_systems": ["Test Service"],
    "detected_at": "2025-11-26T10:00:00Z",
    "context": {}
  }'
```

### View Recent Meetings

```bash
curl http://localhost:8000/meetings/recent
```

### View System Status

```bash
curl http://localhost:8000/status
```

## Production Deployment

### 1. Security Checklist
- [ ] Set strong WEBHOOK_API_KEY
- [ ] Set strong WEBHOOK_SECRET_KEY
- [ ] Use HTTPS in production
- [ ] Configure CORS properly
- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable request logging
- [ ] Set up monitoring

### 2. Database Migration
```bash
# For PostgreSQL
DATABASE_URL=postgresql://user:pass@localhost/chainsync_agents

# For MySQL
DATABASE_URL=mysql://user:pass@localhost/chainsync_agents
```

### 3. Scaling
- Use Redis for rate limiting
- Use message queue for async processing
- Add load balancer for multiple instances
- Use managed database service

## Troubleshooting

### Invalid Signature Error
- Check WEBHOOK_SECRET_KEY matches
- Verify timestamp is current (within 5 minutes)
- Ensure payload hasn't been modified

### Meeting Not Created
- Check SLOTIFY_API_KEY is valid
- Verify Slotify API is accessible
- Check logs for detailed error

### Alert Not Updated
- Check CHAINSYNC_API_KEY is valid
- Verify ChainSync API endpoint
- Check network connectivity

## Support

For issues or questions:
- Check logs in webhook server
- Review database records
- Check API documentation at `/docs`

## Next Steps

1. Configure production API keys
2. Set up monitoring and alerts
3. Configure backup and disaster recovery
4. Implement advanced features (email notifications, Slack integration, etc.)
