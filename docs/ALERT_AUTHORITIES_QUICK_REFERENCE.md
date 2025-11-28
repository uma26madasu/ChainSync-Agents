# Alert-Based Meeting Scheduler - Quick Reference Guide

## 🚀 Quick Command Reference

```bash
# Send a test alert
curl -X POST http://localhost:8000/webhooks/chainsync/alert \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-key" \
  -d @examples/alerts/critical_security.json

# Run demo
python examples/alert_based_meeting_demo.py all

# Show authority mappings
python examples/alert_based_meeting_demo.py mappings

# View recent meetings
curl http://localhost:8000/meetings/recent

# View recent alerts
curl http://localhost:8000/alerts/recent

# Check system status
curl http://localhost:8000/status
```

---

## 📋 Alert Types Cheat Sheet

| Alert Type | Weight | Attendees | Urgency (Critical) |
|-----------|--------|-----------|-------------------|
| **security_incident** | 1.0 | Security, CISO, Legal, IR, Mgmt, Exec | < 1 hour |
| **system_failure** | 1.0 | DevOps, Eng Lead, SRE, Infra, Mgmt | < 1 hour |
| **compliance_violation** | 0.9 | Compliance, Legal, Security, Mgmt, Exec | < 1 hour |
| **integration_failure** | 0.8 | Integration, MuleSoft, API, Partners | < 4 hours |
| **performance_degradation** | 0.7 | Engineering, DevOps, Product, Mgmt | < 4 hours |
| **data_quality_issue** | 0.6 | Data Eng, Analytics, QA | < 24 hours |
| **capacity_warning** | 0.5 | Infrastructure, DevOps, FinOps | < 48 hours |

---

## ⚡ Urgency Calculation

```
Score = Alert Severity × Alert Type Weight

CRITICAL (≥0.8) → < 1 hour   → 60 min meeting
HIGH     (≥0.6) → < 4 hours  → 45 min meeting
MEDIUM   (≥0.4) → < 24 hours → 30 min meeting
LOW      (<0.4) → < 48 hours → 15 min meeting
```

**Severity Scores:**
- `critical` = 1.0
- `high` = 0.8
- `medium` = 0.5
- `low` = 0.3

**Examples:**
```
Critical Security Incident:   1.0 × 1.0 = 1.0  → CRITICAL
High Compliance Violation:    0.8 × 0.9 = 0.72 → HIGH
Medium Performance Issue:     0.5 × 0.7 = 0.35 → LOW
```

---

## 🎯 Escalation Rules

| Condition | Additional Attendees |
|-----------|---------------------|
| severity = `critical` OR `high` | +Management |
| severity = `critical` OR `high` AND type = `compliance_violation` OR `security_incident` | +Executive Sponsor |
| affected_systems > 3 | Meeting duration → 60 min |

---

## 📄 Alert Payload Template

```json
{
  "alert_id": "UNIQUE-ID",
  "alert_type": "security_incident|system_failure|compliance_violation|integration_failure|performance_degradation|data_quality_issue|capacity_warning",
  "severity": "critical|high|medium|low",
  "description": "Clear description of the issue",
  "affected_systems": ["system1", "system2"],
  "detected_at": "2025-11-28T10:00:00Z",
  "context": {
    "key": "value"
  },
  "compliance_frameworks": ["SOC2", "GDPR", "HIPAA", "ISO27001", "PCI-DSS"]
}
```

---

## 🔧 Configuration Files

| File | Purpose |
|------|---------|
| `config/alert_authorities.yaml` | Customize authority lists and escalation rules |
| `.env` | API keys and URLs |
| `chainsync/config.py` | Application configuration |

---

## 📊 Database Quick Queries

```sql
-- Unscheduled high-priority alerts
SELECT alert_id, alert_type, severity, description
FROM alerts
WHERE severity IN ('critical', 'high')
  AND meeting_created = false
ORDER BY detected_at DESC;

-- Today's meetings by urgency
SELECT meeting_id, alert_id, meeting_title, urgency_level, scheduled_time
FROM meetings
WHERE DATE(scheduled_time) = CURRENT_DATE
  AND status = 'scheduled'
ORDER BY urgency_score DESC;

-- Alert → Meeting relationship
SELECT
  a.alert_id,
  a.alert_type,
  a.severity,
  m.meeting_id,
  m.urgency_level,
  m.scheduled_time
FROM alerts a
LEFT JOIN meetings m ON a.meeting_id = m.meeting_id
WHERE a.created_at > NOW() - INTERVAL '7 days'
ORDER BY a.created_at DESC;

-- Meeting effectiveness by alert type
SELECT
  alert_type,
  COUNT(*) as total_alerts,
  SUM(CASE WHEN meeting_created THEN 1 ELSE 0 END) as meetings_scheduled,
  ROUND(AVG(CASE WHEN meeting_created THEN 1 ELSE 0 END) * 100, 2) as meeting_rate
FROM alerts
WHERE created_at > NOW() - INTERVAL '30 days'
GROUP BY alert_type
ORDER BY meeting_rate DESC;
```

---

## 🚨 Example Alerts

### Critical Security Incident
```json
{
  "alert_id": "SEC-2025-001",
  "alert_type": "security_incident",
  "severity": "critical",
  "description": "Unauthorized access attempt detected",
  "affected_systems": ["prod-db-01", "auth-service"],
  "detected_at": "2025-11-28T10:00:00Z",
  "compliance_frameworks": ["SOC2", "ISO27001"]
}
```
**→ CRITICAL urgency, < 1 hour, 60 min meeting**
**→ Attendees:** Security Team, CISO, Legal, IR Team, Management, Executive Sponsor

---

### High Compliance Violation
```json
{
  "alert_id": "COMP-2025-042",
  "alert_type": "compliance_violation",
  "severity": "high",
  "description": "PCI-DSS violation: unencrypted payment data in logs",
  "affected_systems": ["payment-gateway", "logging-service"],
  "detected_at": "2025-11-28T11:00:00Z",
  "compliance_frameworks": ["PCI-DSS"]
}
```
**→ HIGH urgency, < 4 hours, 45 min meeting**
**→ Attendees:** Compliance Officer, Legal, IT Security, Risk Manager, Management, Executive Sponsor

---

### Medium Performance Issue
```json
{
  "alert_id": "PERF-2025-123",
  "alert_type": "performance_degradation",
  "severity": "medium",
  "description": "API response time increased 300%",
  "affected_systems": ["api-gateway", "microservice-cluster"],
  "detected_at": "2025-11-28T12:00:00Z"
}
```
**→ MEDIUM urgency, < 24 hours, 30 min meeting**
**→ Attendees:** Engineering, DevOps, Product, Performance Engineer

---

### Low Capacity Warning
```json
{
  "alert_id": "INFRA-2025-089",
  "alert_type": "capacity_warning",
  "severity": "low",
  "description": "Database storage at 70% capacity",
  "affected_systems": ["prod-db-01"],
  "detected_at": "2025-11-28T13:00:00Z"
}
```
**→ LOW urgency, < 48 hours, 15 min meeting**
**→ Attendees:** Infrastructure, DevOps, FinOps, Capacity Planning

---

## 🔒 Security Headers

All webhook requests require:

```http
POST /webhooks/chainsync/alert HTTP/1.1
Host: your-server.com
Content-Type: application/json
X-API-Key: your-webhook-api-key
X-Webhook-Signature: sha256=<hmac_signature>
X-Webhook-Timestamp: 1732791600
```

---

## 🐛 Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| Meeting not created | Check `SLOTIFY_API_KEY` in `.env` |
| Wrong attendees | Verify `config/alert_authorities.yaml` |
| Urgency incorrect | Check severity and alert_type values |
| No notifications sent | Verify `SLACK_WEBHOOK_URL` or email config |
| Database errors | Run `init_database()` or check `DATABASE_URL` |
| Webhook rejected | Verify `X-API-Key` header |

---

## 📞 Support Checklist

Before contacting support, gather:
- [ ] Alert ID
- [ ] Alert type and severity
- [ ] Expected vs actual attendees
- [ ] Webhook request/response logs
- [ ] Database records (`SELECT * FROM alerts WHERE alert_id = 'XXX'`)
- [ ] System status (`/status` endpoint)
- [ ] Configuration files

---

## 🎓 Best Practices

✅ **DO:**
- Use specific, descriptive alert IDs
- Include all affected systems
- Provide rich context data
- Set severity accurately
- Test with demo script first

❌ **DON'T:**
- Send duplicate alert IDs
- Use generic descriptions
- Omit affected_systems for multi-system issues
- Over-escalate (use correct severity)
- Skip authentication headers

---

## 📈 Metrics to Track

```sql
-- Response time by urgency level
SELECT
  urgency_level,
  AVG(EXTRACT(EPOCH FROM (scheduled_time - created_at))/60) as avg_response_minutes
FROM meetings
WHERE created_at > NOW() - INTERVAL '30 days'
GROUP BY urgency_level;

-- Alert types requiring most meetings
SELECT
  alert_type,
  COUNT(*) as meeting_count
FROM meetings
WHERE created_at > NOW() - INTERVAL '30 days'
GROUP BY alert_type
ORDER BY meeting_count DESC;

-- Average attendees per urgency level
SELECT
  urgency_level,
  AVG(jsonb_array_length(attendees)) as avg_attendees
FROM meetings
WHERE created_at > NOW() - INTERVAL '30 days'
GROUP BY urgency_level;
```

---

## 🔗 Quick Links

- [Full Documentation](./ALERT_BASED_MEETING_SCHEDULER.md)
- [Configuration Guide](../config/alert_authorities.yaml)
- [Demo Script](../examples/alert_based_meeting_demo.py)
- [Integration Guide](./INTEGRATION_GUIDE.md)

---

**Print this page for your incident response playbook!**
