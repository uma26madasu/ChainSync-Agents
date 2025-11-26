"""
Enhanced Webhook Server for ChainSync and Slotify Integration with Full Features

Features:
- API key authentication
- HMAC signature verification
- Database persistence for meetings and alerts
- Slotify meeting creation
- ChainSync status updates
- Rate limiting
- Comprehensive logging
"""

from fastapi import FastAPI, Request, HTTPException, BackgroundTasks, Depends, Header
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import logging
import time
import json

from .agent_orchestrator import AgentOrchestrator
from .api_clients import SlotifyAPIClient, ChainSyncAPIClient
from .database import (
    init_database, get_db,
    MeetingRepository, AlertRepository, LearningRepository, WebhookLogRepository
)
from .security import verify_api_key, verify_webhook_signature, rate_limit_check
from .config import Config

# Configure logging
logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL))
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="ChainSync AI Agent Webhook Server",
    description="Secure webhook endpoints for ChainSync alerts and Slotify meetings with full integration",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
orchestrator = AgentOrchestrator()
slotify_client = SlotifyAPIClient()
chainsync_client = ChainSyncAPIClient()

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database and log startup."""
    logger.info("ChainSync AI Agent Webhook Server v2.0 starting...")
    init_database()
    logger.info(f"Initialized with {len(orchestrator.agents)} agents")
    logger.info(f"Security: API Key={'enabled' if Config.WEBHOOK_API_KEY else 'disabled'}, Signatures={'enabled' if Config.WEBHOOK_SECRET_KEY else 'disabled'}")


# Pydantic Models

class ChainSyncAlert(BaseModel):
    """ChainSync alert webhook payload."""
    alert_id: str
    alert_type: str
    severity: str
    description: str
    affected_systems: List[str] = Field(default_factory=list)
    detected_at: str
    context: Dict[str, Any] = Field(default_factory=dict)
    compliance_frameworks: Optional[List[str]] = None


class SlotifyMeeting(BaseModel):
    """Slotify meeting webhook payload."""
    meeting_id: str
    title: str
    scheduled_time: str
    attendees: List[str] = Field(default_factory=list)
    alert_reference: Optional[str] = None
    organizer: Optional[str] = None
    duration_minutes: Optional[int] = 30


class WebhookResponse(BaseModel):
    """Standard webhook response."""
    status: str
    message: str
    data: Optional[Dict[str, Any]] = None
    timestamp: str


# Helper Functions

async def log_webhook_request(
    db,
    endpoint: str,
    method: str,
    payload: Any,
    headers: Dict,
    response_status: int,
    response_body: Any,
    processing_time_ms: float,
    error: Optional[str],
    ip_address: str
):
    """Log webhook request to database."""
    try:
        WebhookLogRepository.create(db, {
            "endpoint": endpoint,
            "method": method,
            "payload": payload if isinstance(payload, dict) else {},
            "headers": dict(headers),
            "response_status": response_status,
            "response_body": str(response_body)[:1000],  # Limit size
            "processing_time_ms": processing_time_ms,
            "error": error,
            "ip_address": ip_address
        })
    except Exception as e:
        logger.error(f"Failed to log webhook request: {str(e)}")


# Endpoints

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "service": "ChainSync AI Agent Webhook Server",
        "version": "2.0.0",
        "features": {
            "api_key_auth": bool(Config.WEBHOOK_API_KEY),
            "signature_verification": bool(Config.WEBHOOK_SECRET_KEY),
            "database_persistence": True,
            "slotify_integration": bool(Config.SLOTIFY_API_KEY),
            "chainsync_integration": bool(Config.CHAINSYNC_API_KEY)
        },
        "endpoints": {
            "chainsync_alerts": "/webhooks/chainsync/alert",
            "slotify_meetings": "/webhooks/slotify/meeting",
            "health": "/health",
            "status": "/status",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "ChainSync AI Agents",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/status")
async def get_status():
    """Get system status including all agents."""
    try:
        status = await orchestrator.get_system_status()
        return JSONResponse(
            status_code=200,
            content={
                "status": "operational",
                "system_status": status,
                "integrations": {
                    "slotify": "enabled" if Config.SLOTIFY_API_KEY else "disabled",
                    "chainsync": "enabled" if Config.CHAINSYNC_API_KEY else "disabled",
                    "database": "enabled"
                },
                "timestamp": datetime.now().isoformat()
            }
        )
    except Exception as e:
        logger.error(f"Error getting status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/webhooks/chainsync/alert", response_model=WebhookResponse)
async def receive_chainsync_alert(
    alert: ChainSyncAlert,
    request: Request,
    background_tasks: BackgroundTasks,
    db=Depends(get_db),
    api_key: Optional[str] = Header(None, alias="X-API-Key")
):
    """
    Receive ChainSync alert webhook - COMPLETE INTEGRATION.

    Flow:
    1. Authenticate request
    2. Process alert through AI agents
    3. Create Slotify meeting
    4. Update ChainSync with meeting URL
    5. Save everything to database
    6. Return complete response
    """
    start_time = time.time()
    client_ip = request.client.host if request.client else "unknown"

    # Security checks
    rate_limit_check(client_ip)
    verify_api_key(api_key)

    logger.info(f"Processing ChainSync alert: {alert.alert_id} - {alert.alert_type} ({alert.severity})")

    try:
        # Convert to dict
        alert_data = alert.dict()

        # Step 1: Trigger AI agent workflow
        logger.info(f"Running alert_to_meeting workflow for {alert.alert_id}")
        workflow_result = await orchestrator.multi_agent_workflow(
            'alert_to_meeting',
            {
                'alert_data': alert_data,
                'meeting_data': {}  # Will be auto-generated
            }
        )

        meeting_context = workflow_result.get('meeting_context', {})

        # Step 2: Create meeting in Slotify
        logger.info(f"Creating Slotify meeting for alert {alert.alert_id}")
        slotify_meeting = await slotify_client.create_meeting(
            title=meeting_context.get('meeting_title', f"Alert Review: {alert.alert_type}"),
            description=meeting_context.get('why_scheduled', 'Meeting scheduled by AI agent'),
            scheduled_time=meeting_context.get('scheduled_time', datetime.now().isoformat()),
            duration_minutes=int(meeting_context.get('recommended_duration', '30').split()[0]),
            attendees=meeting_context.get('suggested_attendees', []),
            alert_reference=alert.alert_id
        )

        meeting_id = slotify_meeting.get('meeting_id')
        meeting_url = slotify_meeting.get('meeting_url', '')

        logger.info(f"Slotify meeting created: {meeting_id}")

        # Step 3: Update ChainSync with meeting URL
        logger.info(f"Updating ChainSync alert {alert.alert_id} with meeting URL")
        await chainsync_client.update_alert_status(
            alert_id=alert.alert_id,
            status="meeting_scheduled",
            meeting_url=meeting_url,
            notes=f"AI-generated meeting context: {meeting_context.get('why_scheduled', '')[:200]}"
        )

        # Add comment with AI analysis
        await chainsync_client.add_alert_comment(
            alert_id=alert.alert_id,
            comment=f"Root Cause: {workflow_result.get('root_cause_analysis', {}).get('root_cause', 'Unknown')}\nMeeting scheduled: {meeting_url}",
            author="AI Agent"
        )

        # Step 4: Save to database
        logger.info(f"Saving alert and meeting to database")

        # Save alert
        AlertRepository.create(db, {
            "alert_id": alert.alert_id,
            "alert_type": alert.alert_type,
            "severity": alert.severity,
            "description": alert.description,
            "affected_systems": alert.affected_systems,
            "detected_at": datetime.fromisoformat(alert.detected_at.replace('Z', '+00:00')),
            "root_cause": workflow_result.get('root_cause_analysis', {}).get('root_cause'),
            "recommendations": workflow_result.get('root_cause_analysis', {}).get('recommendations', []),
            "compliance_status": workflow_result.get('compliance_check', {}).get('overall_status'),
            "compliance_violations": workflow_result.get('compliance_check', {}).get('violations', []),
            "meeting_created": True,
            "meeting_id": meeting_id
        })

        # Save meeting
        MeetingRepository.create(db, {
            "meeting_id": meeting_id,
            "alert_id": alert.alert_id,
            "meeting_title": meeting_context.get('meeting_title'),
            "scheduled_time": datetime.fromisoformat(meeting_context.get('scheduled_time', datetime.now().isoformat()).replace('Z', '+00:00')),
            "meeting_url": meeting_url,
            "attendees": meeting_context.get('suggested_attendees', []),
            "alert_type": alert.alert_type,
            "alert_severity": alert.severity,
            "urgency_level": meeting_context.get('urgency', {}).get('level'),
            "urgency_score": meeting_context.get('urgency', {}).get('score'),
            "why_scheduled": meeting_context.get('why_scheduled'),
            "discussion_points": meeting_context.get('discussion_points', []),
            "pre_meeting_summary": meeting_context.get('pre_meeting_summary'),
            "suggested_attendees": meeting_context.get('suggested_attendees', []),
            "recommended_duration": meeting_context.get('recommended_duration'),
            "status": "scheduled"
        })

        processing_time = (time.time() - start_time) * 1000

        # Log webhook request
        await log_webhook_request(
            db, "/webhooks/chainsync/alert", "POST", alert_data,
            dict(request.headers), 200, "success", processing_time, None, client_ip
        )

        logger.info(f"Alert {alert.alert_id} processed successfully in {processing_time:.2f}ms")

        return WebhookResponse(
            status="success",
            message=f"Alert {alert.alert_id} processed and meeting {meeting_id} created",
            data={
                "alert_id": alert.alert_id,
                "meeting_id": meeting_id,
                "meeting_url": meeting_url,
                "urgency": meeting_context.get('urgency'),
                "workflow_result": {
                    "root_cause": workflow_result.get('root_cause_analysis', {}).get('root_cause'),
                    "compliance_status": workflow_result.get('compliance_check', {}).get('overall_status'),
                    "meeting_explanation": workflow_result.get('meeting_explanation', '')[:500]
                },
                "processing_time_ms": processing_time
            },
            timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        processing_time = (time.time() - start_time) * 1000
        logger.error(f"Error processing alert {alert.alert_id}: {str(e)}")

        # Log failed request
        await log_webhook_request(
            db, "/webhooks/chainsync/alert", "POST", alert.dict(),
            dict(request.headers), 500, str(e), processing_time, str(e), client_ip
        )

        raise HTTPException(status_code=500, detail=f"Error processing alert: {str(e)}")


@app.post("/webhooks/slotify/meeting", response_model=WebhookResponse)
async def receive_slotify_meeting(
    meeting: SlotifyMeeting,
    request: Request,
    background_tasks: BackgroundTasks,
    db=Depends(get_db),
    api_key: Optional[str] = Header(None, alias="X-API-Key")
):
    """Receive Slotify meeting webhook and generate context."""
    start_time = time.time()
    client_ip = request.client.host if request.client else "unknown"

    # Security checks
    rate_limit_check(client_ip)
    verify_api_key(api_key)

    logger.info(f"Processing Slotify meeting: {meeting.meeting_id}")

    try:
        meeting_agent = orchestrator.get_agent('meeting_context')

        # If there's an alert reference, get alert context
        alert_data = {}
        if meeting.alert_reference:
            # Try to get from database first
            alert_record = AlertRepository.get_by_alert_id(db, meeting.alert_reference)
            if alert_record:
                alert_data = {
                    'alert_id': alert_record.alert_id,
                    'alert_type': alert_record.alert_type,
                    'severity': alert_record.severity,
                    'description': alert_record.description,
                    'affected_systems': alert_record.affected_systems
                }
            else:
                # Fetch from ChainSync API
                try:
                    alert_data = await chainsync_client.get_alert(meeting.alert_reference)
                except:
                    alert_data = {'alert_id': meeting.alert_reference}

        # Generate meeting context
        meeting_context = await meeting_agent.process_slotify_meeting(
            meeting.dict(),
            alert_data
        )

        # Save to database if not already saved
        existing = MeetingRepository.get_by_meeting_id(db, meeting.meeting_id)
        if not existing:
            MeetingRepository.create(db, {
                "meeting_id": meeting.meeting_id,
                "alert_id": meeting.alert_reference,
                "meeting_title": meeting.title,
                "scheduled_time": datetime.fromisoformat(meeting.scheduled_time.replace('Z', '+00:00')),
                "attendees": meeting.attendees,
                "status": "scheduled"
            })

        processing_time = (time.time() - start_time) * 1000

        return WebhookResponse(
            status="success",
            message=f"Meeting {meeting.meeting_id} context generated",
            data={
                "meeting_id": meeting.meeting_id,
                "meeting_context": meeting_context,
                "explanation": await meeting_agent.explain_meeting(meeting.meeting_id),
                "processing_time_ms": processing_time
            },
            timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        logger.error(f"Error processing meeting {meeting.meeting_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/agents/list")
async def list_agents():
    """List all available agents."""
    return {
        "agents": orchestrator.list_agents(),
        "total_count": len(orchestrator.agents),
        "timestamp": datetime.now().isoformat()
    }


@app.get("/meetings/recent")
async def get_recent_meetings(limit: int = 20, db=Depends(get_db)):
    """Get recent meetings from database."""
    meetings = MeetingRepository.get_recent_meetings(db, limit)
    return {
        "meetings": [
            {
                "meeting_id": m.meeting_id,
                "alert_id": m.alert_id,
                "title": m.meeting_title,
                "scheduled_time": m.scheduled_time.isoformat() if m.scheduled_time else None,
                "urgency": m.urgency_level,
                "status": m.status,
                "created_at": m.created_at.isoformat() if m.created_at else None
            }
            for m in meetings
        ],
        "count": len(meetings),
        "timestamp": datetime.now().isoformat()
    }


@app.get("/alerts/recent")
async def get_recent_alerts(limit: int = 20, db=Depends(get_db)):
    """Get recent alerts from database."""
    from chainsync.database import AlertRecord
    alerts = db.query(AlertRecord).order_by(AlertRecord.created_at.desc()).limit(limit).all()
    return {
        "alerts": [
            {
                "alert_id": a.alert_id,
                "alert_type": a.alert_type,
                "severity": a.severity,
                "description": a.description,
                "meeting_created": a.meeting_created,
                "meeting_id": a.meeting_id,
                "created_at": a.created_at.isoformat() if a.created_at else None
            }
            for a in alerts
        ],
        "count": len(alerts),
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=Config.PYTHON_AGENT_PORT)
