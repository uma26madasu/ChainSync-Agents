# Alert-Based Meeting Scheduler

## Overview

The **Alert-Based Meeting Scheduler** automatically schedules meetings in Slotify when ChainSync detects critical issues, ensuring the right authorities are notified and assembled immediately.

## 🎯 Key Features

- ✅ **Automatic Meeting Scheduling** - Triggers meetings based on alert severity
- ✅ **Smart Authority Selection** - Invites the right people based on alert type
- ✅ **AI-Powered Context** - Generates meeting agendas, discussion points, and summaries
- ✅ **Escalation Logic** - Automatically escalates critical issues to management
- ✅ **Multi-Framework Compliance** - Tracks SOC2, GDPR, HIPAA, ISO27001, PCI-DSS violations
- ✅ **Full Database Tracking** - Maintains audit trail of all alerts and meetings

---

## 📊 How It Works

```
┌─────────────────┐
│  ChainSync API  │
│  Detects Alert  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Webhook Server │
│  Receives Alert │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   AI Agents     │
│  • Root Cause   │
│  • Compliance   │
│  • Meeting Ctx  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Slotify API    │
│  Creates Meeting│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Notify Team    │
│  • Email        │
│  • Slack        │
│  • Calendar     │
└─────────────────┘
```

---

## 🚀 Quick Start

### 1. Send an Alert Webhook

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
    "context": {
      "ip_addresses": ["192.168.1.100"],
      "failed_attempts": 150
    },
    "compliance_frameworks": ["SOC2", "ISO27001"]
  }'
```

### 2. Meeting Automatically Scheduled

The system will:
1. ✅ Analyze the alert with AI agents
2. ✅ Calculate urgency (CRITICAL in this case)
3. ✅ Select attendees: Security Team, CISO, Legal, Management, Executive Sponsor
4. ✅ Generate meeting context and discussion points
5. ✅ Create Slotify meeting within 1 hour
6. ✅ Update ChainSync with meeting URL
7. ✅ Send notifications to all attendees

---

## 📋 Alert Types & Authorities

### 1. Security Incident
**Severity Weight:** 1.0 (Highest Priority)

**Attendees:**
- Security Team
- CISO
- Legal Team
- Incident Response Team
- **+Management** (for high/critical)
- **+Executive Sponsor** (for high/critical)

**Example:**
```json
{
  "alert_type": "security_incident",
  "severity": "critical"
}
```

**Urgency:** CRITICAL → Meeting within 1 hour (60 min duration)

---

### 2. Compliance Violation
**Severity Weight:** 0.9

**Attendees:**
- Compliance Officer
- Legal Team
- IT Security Lead
- Risk Manager
- **+Management** (for high/critical)
- **+Executive Sponsor** (for high/critical)

**Example:**
```json
{
  "alert_type": "compliance_violation",
  "severity": "high",
  "compliance_frameworks": ["PCI-DSS"]
}
```

**Urgency:** HIGH → Meeting within 4 hours (45 min duration)

---

### 3. System Failure
**Severity Weight:** 1.0

**Attendees:**
- DevOps Lead
- Engineering Lead
- SRE Team
- Infrastructure Manager
- On-Call Engineer
- **+Management** (for high/critical)

**Example:**
```json
{
  "alert_type": "system_failure",
  "severity": "critical",
  "affected_systems": ["prod-api", "database"]
}
```

**Urgency:** CRITICAL → Meeting within 1 hour (60 min duration)

---

### 4. Performance Degradation
**Severity Weight:** 0.7

**Attendees:**
- Engineering Team
- DevOps Team
- Product Manager
- Performance Engineer
- **+Management** (for high/critical)

**Example:**
```json
{
  "alert_type": "performance_degradation",
  "severity": "medium"
}
```

**Urgency:** MEDIUM → Meeting within 24 hours (30 min duration)

---

### 5. Data Quality Issue
**Severity Weight:** 0.6

**Attendees:**
- Data Engineering Lead
- Analytics Team
- QA Lead
- Data Steward

**Example:**
```json
{
  "alert_type": "data_quality_issue",
  "severity": "medium"
}
```

**Urgency:** MEDIUM → Meeting within 24 hours (30 min duration)

---

### 6. Integration Failure
**Severity Weight:** 0.8

**Attendees:**
- Integration Team
- MuleSoft Administrator
- API Team
- Partner Relations

**Example:**
```json
{
  "alert_type": "integration_failure",
  "severity": "high"
}
```

**Urgency:** HIGH → Meeting within 4 hours (45 min duration)

---

### 7. Capacity Warning
**Severity Weight:** 0.5

**Attendees:**
- Infrastructure Team
- DevOps Team
- Finance/FinOps
- Capacity Planning

**Example:**
```json
{
  "alert_type": "capacity_warning",
  "severity": "low"
}
```

**Urgency:** LOW → Meeting within 48 hours (15 min duration)

---

## ⚡ Urgency Calculation

The system calculates urgency using:

```
Urgency Score = Alert Severity × Alert Type Weight
```

| Urgency Level | Score Range | Response Time | Meeting Duration |
|---------------|-------------|---------------|------------------|
| **CRITICAL**  | ≥ 0.8      | < 1 hour      | 60 minutes       |
| **HIGH**      | ≥ 0.6      | < 4 hours     | 45 minutes       |
| **MEDIUM**    | ≥ 0.4      | < 24 hours    | 30 minutes       |
| **LOW**       | < 0.4      | < 48 hours    | 15 minutes       |

### Examples:

```python
# Example 1: Critical Security Incident
severity = "critical"       # Score: 1.0
alert_type = "security_incident"  # Weight: 1.0
urgency_score = 1.0 × 1.0 = 1.0  → CRITICAL

# Example 2: Medium Performance Issue
severity = "medium"         # Score: 0.5
alert_type = "performance_degradation"  # Weight: 0.7
urgency_score = 0.5 × 0.7 = 0.35  → LOW

# Example 3: High Compliance Violation
severity = "high"           # Score: 0.8
alert_type = "compliance_violation"  # Weight: 0.9
urgency_score = 0.8 × 0.9 = 0.72  → HIGH
```

---

## 🎯 Escalation Rules

### Rule 1: High Severity Escalation
```yaml
Trigger: severity = "critical" OR "high"
Action: Add "Management" to attendees
```

### Rule 2: Executive Escalation
```yaml
Trigger:
  - severity = "critical" OR "high"
  - alert_type = "compliance_violation" OR "security_incident"
Action: Add "Executive Sponsor" to attendees
```

### Rule 3: Multiple Systems
```yaml
Trigger: affected_systems.length > 3
Action: Increase meeting duration to 60 minutes
```

---

## 🤖 AI-Generated Meeting Context

For each meeting, the AI generates:

### 1. Why Scheduled
Clear explanation of:
- What triggered the meeting
- Why it requires immediate attention
- Potential business impact

**Example:**
```
This meeting was automatically scheduled due to a critical security incident
detected on production systems. Unauthorized access attempts were identified
from unknown IP addresses, representing a potential data breach. Immediate
coordination between Security, Legal, and Executive teams is required to
assess impact and implement containment measures.
```

### 2. Discussion Points (5-7 specific items)
**Example:**
```
1. Review detailed logs of unauthorized access attempts and affected systems
2. Assess scope of potential data exposure and customer impact
3. Activate incident response protocol and assign roles
4. Implement immediate containment measures (firewall rules, access revocation)
5. Determine regulatory notification requirements (GDPR, SOC2)
6. Plan customer communication strategy
7. Schedule follow-up forensic analysis
```

### 3. Pre-Meeting Summary
2-minute brief covering:
- Alert overview
- Current status
- Key metrics
- Immediate actions taken
- Decisions needed

---

## 📦 Database Tracking

All alerts and meetings are stored in the database for audit trails:

### Alert Record
```sql
SELECT * FROM alerts WHERE alert_id = 'SEC-2025-001';
```

**Fields:**
- `alert_id`, `alert_type`, `severity`, `description`
- `affected_systems` (JSON)
- `root_cause` (AI-generated)
- `recommendations` (JSON)
- `compliance_status`, `compliance_violations`
- `meeting_created`, `meeting_id`
- `detected_at`, `processed_at`, `created_at`

### Meeting Record
```sql
SELECT * FROM meetings WHERE alert_id = 'SEC-2025-001';
```

**Fields:**
- `meeting_id`, `alert_id`, `meeting_title`
- `scheduled_time`, `meeting_url`
- `attendees` (JSON)
- `urgency_level`, `urgency_score`
- `why_scheduled`, `discussion_points` (JSON)
- `pre_meeting_summary`
- `status` (scheduled/completed/cancelled)

---

## 🔧 Configuration

### Customize Authority Lists

Edit `config/alert_authorities.yaml`:

```yaml
alert_types:
  security_incident:
    severity_weight: 1.0
    typical_attendees:
      - Security Team
      - CISO
      - Your Custom Role
    email_addresses:
      - security@yourcompany.com
      - ciso@yourcompany.com
      - custom@yourcompany.com
```

### Add Custom Alert Types

```yaml
custom_alert_types:
  sla_breach:
    severity_weight: 0.85
    category: Customer Success
    typical_attendees:
      - Account Manager
      - Customer Success Lead
    email_addresses:
      - am@yourcompany.com
      - cs@yourcompany.com
```

---

## 🧪 Testing & Demo

### Run Complete Demo

```bash
# Demo all alert types
python examples/alert_based_meeting_demo.py all

# Show authority mappings
python examples/alert_based_meeting_demo.py mappings

# Test specific alert type
python examples/alert_based_meeting_demo.py critical_security
```

### Demo Output Example

```
================================================================================
🚨 SIMULATING ALERT: SEC-2025-001
================================================================================
Type: security_incident
Severity: CRITICAL
Description: Unauthorized access attempt detected on production database
Affected Systems: prod-db-01, prod-db-02, auth-service

🤖 Running AI Agent Analysis...
✓ Root Cause Analysis Complete
✓ Compliance Check Complete

📅 MEETING SCHEDULED IN SLOTIFY
────────────────────────────────────────────────────────────────────────────────
Title: URGENT: Security Incident Response - Unauthorized Access
Urgency: CRITICAL (Score: 1.0)
Response Time: < 1 hour
Duration: 60 minutes

👥 CONCERNED AUTHORITIES INVITED:
────────────────────────────────────────────────────────────────────────────────
  • Security Team
  • CISO
  • Legal Team
  • Incident Response Team
  • Management
  • Executive Sponsor
```

---

## 🔌 API Endpoints

### Webhook Endpoint
```
POST /webhooks/chainsync/alert
```

**Headers:**
```
X-API-Key: your-webhook-api-key
Content-Type: application/json
```

**Response:**
```json
{
  "status": "success",
  "message": "Alert SEC-2025-001 processed and meeting MTG-001 created",
  "data": {
    "alert_id": "SEC-2025-001",
    "meeting_id": "MTG-001",
    "meeting_url": "https://slotify.com/meetings/MTG-001",
    "urgency": {
      "level": "CRITICAL",
      "score": 1.0,
      "recommended_response_time": "< 1 hour"
    },
    "workflow_result": {
      "root_cause": "Brute force attack from compromised credentials",
      "compliance_status": "violation_detected"
    }
  }
}
```

### Query Recent Meetings
```
GET /meetings/recent?limit=20
```

### Query Recent Alerts
```
GET /alerts/recent?limit=20
```

---

## 🚀 Production Deployment

### 1. Set Environment Variables

```bash
# API Keys
export OPENAI_API_KEY="your-openai-key"
export CHAINSYNC_API_KEY="your-chainsync-key"
export SLOTIFY_API_KEY="your-slotify-key"
export WEBHOOK_API_KEY="your-webhook-key"
export WEBHOOK_SECRET_KEY="your-secret-key"

# API URLs
export CHAINSYNC_API_URL="https://api.chainsync.com"
export SLOTIFY_API_URL="https://api.slotify.com"

# Database
export DATABASE_URL="postgresql://user:pass@localhost/chainsync"
```

### 2. Start the Server

```bash
uvicorn chainsync.webhook_server:app --host 0.0.0.0 --port 8000
```

### 3. Configure ChainSync Webhook

In your ChainSync settings, configure the webhook URL:
```
https://your-server.com/webhooks/chainsync/alert
```

Add authentication headers:
```
X-API-Key: your-webhook-api-key
```

---

## 📊 Monitoring & Analytics

### View System Status
```bash
curl http://localhost:8000/status
```

### Health Check
```bash
curl http://localhost:8000/health
```

### Database Queries

```sql
-- High-priority alerts needing meetings
SELECT * FROM alerts
WHERE severity IN ('critical', 'high')
  AND meeting_created = false
ORDER BY detected_at DESC;

-- Upcoming meetings by urgency
SELECT * FROM meetings
WHERE status = 'scheduled'
  AND scheduled_time > NOW()
ORDER BY urgency_score DESC;

-- Meeting effectiveness (alerts with meetings vs without)
SELECT
  COUNT(*) as total_alerts,
  SUM(CASE WHEN meeting_created THEN 1 ELSE 0 END) as with_meetings,
  AVG(CASE WHEN meeting_created THEN 1 ELSE 0 END) * 100 as meeting_rate
FROM alerts
WHERE created_at > NOW() - INTERVAL '30 days';
```

---

## 🔒 Security

### Webhook Authentication

All webhook requests must include:

1. **API Key Header:** `X-API-Key`
2. **HMAC Signature:** `X-Webhook-Signature`
3. **Timestamp:** `X-Webhook-Timestamp` (validated within 5 minutes)

### Rate Limiting

- Default: 100 requests per minute per IP
- Configurable via environment variables

### Request Size Limits

- Maximum payload: 1MB
- Prevents DoS attacks

---

## 🎓 Best Practices

### 1. Authority Lists
- ✅ Keep email addresses up-to-date
- ✅ Use distribution lists for teams
- ✅ Test escalation paths regularly

### 2. Alert Configuration
- ✅ Set appropriate severity thresholds
- ✅ Avoid alert fatigue with proper filtering
- ✅ Review and adjust weights quarterly

### 3. Meeting Management
- ✅ Ensure attendees review pre-meeting summaries
- ✅ Track meeting outcomes in database
- ✅ Use discussion points as agenda

### 4. Compliance
- ✅ Maintain audit trail of all alerts
- ✅ Document meeting decisions
- ✅ Regular compliance framework reviews

---

## 🐛 Troubleshooting

### Meeting Not Created

**Check:**
1. Slotify API key configured?
2. Alert severity meets threshold?
3. Check logs: `/var/log/chainsync-webhook.log`

### Wrong Attendees Invited

**Solution:**
1. Review `config/alert_authorities.yaml`
2. Check alert type matches configuration
3. Verify escalation rules

### Urgency Calculation Wrong

**Debug:**
```python
severity_score = {"critical": 1.0, "high": 0.8, "medium": 0.5, "low": 0.3}[severity]
alert_weight = alert_types[alert_type]["severity_weight"]
urgency = severity_score * alert_weight
```

---

## 📚 Additional Resources

- [Integration Guide](./INTEGRATION_GUIDE.md)
- [API Documentation](./API.md)
- [Agent Architecture](./ARCHITECTURE.md)
- [Database Schema](./DATABASE.md)

---

## 🤝 Support

For issues or questions:
- GitHub Issues: https://github.com/uma26madasu/ChainSync-Agents/issues
- Email: support@yourcompany.com

---

**Last Updated:** 2025-11-28
**Version:** 2.0.0
