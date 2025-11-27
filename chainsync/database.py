"""
Database models and persistence layer for ChainSync AI Agents

This module provides:
- SQLAlchemy models for meetings, alerts, and agent learning data
- Database initialization and session management
- CRUD operations for persistent storage
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, Boolean, JSON, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import datetime
from .config import Config
import logging

logger = logging.getLogger(__name__)

# Create base class for models
Base = declarative_base()

# Database engine and session
engine = None
SessionLocal = None


def init_database():
    """Initialize database connection with connection pooling and create tables."""
    global engine, SessionLocal

    database_url = Config.DATABASE_URL
    logger.info(f"Initializing database: {database_url}")

    # Connection pool configuration
    pool_config = {}
    if "sqlite" in database_url:
        # SQLite doesn't support connection pooling
        pool_config["connect_args"] = {"check_same_thread": False}
    else:
        # PostgreSQL/MySQL connection pool settings
        pool_config.update({
            "pool_size": 10,  # Number of connections to maintain
            "max_overflow": 20,  # Additional connections allowed when pool is exhausted
            "pool_timeout": 30,  # Seconds to wait for a connection
            "pool_pre_ping": True,  # Verify connections before using them
            "pool_recycle": 3600,  # Recycle connections after 1 hour
        })

    # Create engine with pooling
    engine = create_engine(
        database_url,
        echo=Config.DEBUG,
        **pool_config
    )

    # Create session factory
    SessionLocal = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )

    # Create all tables (use Alembic migrations in production)
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized successfully with connection pooling")


def get_db():
    """Get database session."""
    if SessionLocal is None:
        init_database()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class MeetingRecord(Base):
    """Database model for meeting history."""
    __tablename__ = "meetings"
    __table_args__ = (
        Index('ix_meetings_status_scheduled_time', 'status', 'scheduled_time'),
        Index('ix_meetings_alert_type_severity', 'alert_type', 'alert_severity'),
    )

    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(String(255), unique=True, index=True, nullable=False)
    alert_id = Column(String(255), index=True)
    meeting_title = Column(String(500))
    scheduled_time = Column(DateTime, index=True)  # Added index for time-based queries
    meeting_url = Column(String(500))
    attendees = Column(JSON)  # List of email addresses
    alert_type = Column(String(100))
    alert_severity = Column(String(50))
    urgency_level = Column(String(50))
    urgency_score = Column(Float)
    why_scheduled = Column(Text)
    discussion_points = Column(JSON)  # List of discussion points
    pre_meeting_summary = Column(Text)
    suggested_attendees = Column(JSON)  # List of suggested attendees
    recommended_duration = Column(String(50))
    status = Column(String(50), default="scheduled", index=True)  # Added index for status filtering
    created_at = Column(DateTime, default=datetime.now, index=True)  # Added index
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class AlertRecord(Base):
    """Database model for alert processing history."""
    __tablename__ = "alerts"
    __table_args__ = (
        Index('ix_alerts_type_severity', 'alert_type', 'severity'),
        Index('ix_alerts_meeting_created_processed', 'meeting_created', 'processed_at'),
    )

    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(String(255), unique=True, index=True, nullable=False)
    alert_type = Column(String(100), index=True)
    severity = Column(String(50), index=True)
    description = Column(Text)
    affected_systems = Column(JSON)  # List of affected systems
    detected_at = Column(DateTime, index=True)  # Added index for time-based queries
    root_cause = Column(Text)
    recommendations = Column(JSON)  # List of recommendations
    compliance_status = Column(String(50), index=True)  # Added index for compliance filtering
    compliance_violations = Column(JSON)  # List of violations
    meeting_created = Column(Boolean, default=False, index=True)  # Added index
    meeting_id = Column(String(255), index=True)  # Added index for lookups
    processed_at = Column(DateTime, default=datetime.now, index=True)  # Added index
    created_at = Column(DateTime, default=datetime.now, index=True)  # Added index


class LearningData(Base):
    """Database model for agent learning history."""
    __tablename__ = "learning_data"

    id = Column(Integer, primary_key=True, index=True)
    agent_name = Column(String(100), index=True)
    interaction_type = Column(String(100), index=True)  # query, rca, compliance, etc.
    query = Column(Text)
    response = Column(Text)
    feedback_score = Column(Float)  # 0.0 to 1.0
    context = Column(JSON)  # Additional context data
    patterns_identified = Column(JSON)  # List of identified patterns
    created_at = Column(DateTime, default=datetime.now, index=True)


class WebhookLog(Base):
    """Database model for webhook request logging."""
    __tablename__ = "webhook_logs"

    id = Column(Integer, primary_key=True, index=True)
    endpoint = Column(String(255), index=True)
    method = Column(String(10))
    payload = Column(JSON)
    headers = Column(JSON)
    response_status = Column(Integer)
    response_body = Column(Text)
    processing_time_ms = Column(Float)
    error = Column(Text)
    ip_address = Column(String(50))
    created_at = Column(DateTime, default=datetime.now, index=True)


# CRUD Operations

class MeetingRepository:
    """Repository for meeting operations."""

    @staticmethod
    def create(db, meeting_data: dict) -> MeetingRecord:
        """Create a new meeting record."""
        meeting = MeetingRecord(**meeting_data)
        db.add(meeting)
        db.commit()
        db.refresh(meeting)
        return meeting

    @staticmethod
    def get_by_meeting_id(db, meeting_id: str) -> MeetingRecord:
        """Get meeting by meeting_id."""
        return db.query(MeetingRecord).filter(MeetingRecord.meeting_id == meeting_id).first()

    @staticmethod
    def get_by_alert_id(db, alert_id: str) -> MeetingRecord:
        """Get meeting by alert_id."""
        return db.query(MeetingRecord).filter(MeetingRecord.alert_id == alert_id).first()

    @staticmethod
    def update_status(db, meeting_id: str, status: str):
        """Update meeting status."""
        meeting = MeetingRepository.get_by_meeting_id(db, meeting_id)
        if meeting:
            meeting.status = status
            meeting.updated_at = datetime.now()
            db.commit()
            db.refresh(meeting)
        return meeting

    @staticmethod
    def get_recent_meetings(db, limit: int = 50):
        """Get recent meetings."""
        return db.query(MeetingRecord).order_by(MeetingRecord.created_at.desc()).limit(limit).all()


class AlertRepository:
    """Repository for alert operations."""

    @staticmethod
    def create(db, alert_data: dict) -> AlertRecord:
        """Create a new alert record."""
        alert = AlertRecord(**alert_data)
        db.add(alert)
        db.commit()
        db.refresh(alert)
        return alert

    @staticmethod
    def get_by_alert_id(db, alert_id: str) -> AlertRecord:
        """Get alert by alert_id."""
        return db.query(AlertRecord).filter(AlertRecord.alert_id == alert_id).first()

    @staticmethod
    def update_meeting_info(db, alert_id: str, meeting_id: str):
        """Update alert with meeting information."""
        alert = AlertRepository.get_by_alert_id(db, alert_id)
        if alert:
            alert.meeting_created = True
            alert.meeting_id = meeting_id
            db.commit()
            db.refresh(alert)
        return alert

    @staticmethod
    def get_by_severity(db, severity: str, limit: int = 50):
        """Get alerts by severity."""
        return db.query(AlertRecord).filter(AlertRecord.severity == severity).order_by(AlertRecord.detected_at.desc()).limit(limit).all()


class LearningRepository:
    """Repository for learning data operations."""

    @staticmethod
    def create(db, learning_data: dict) -> LearningData:
        """Create a new learning data record."""
        learning = LearningData(**learning_data)
        db.add(learning)
        db.commit()
        db.refresh(learning)
        return learning

    @staticmethod
    def get_by_agent(db, agent_name: str, limit: int = 100):
        """Get learning data for a specific agent."""
        return db.query(LearningData).filter(LearningData.agent_name == agent_name).order_by(LearningData.created_at.desc()).limit(limit).all()

    @staticmethod
    def get_recent_patterns(db, agent_name: str, days: int = 30):
        """Get recent patterns identified by agent."""
        from datetime import timedelta
        since = datetime.now() - timedelta(days=days)
        return db.query(LearningData).filter(
            LearningData.agent_name == agent_name,
            LearningData.created_at >= since,
            LearningData.patterns_identified.isnot(None)
        ).all()


class WebhookLogRepository:
    """Repository for webhook log operations."""

    @staticmethod
    def create(db, log_data: dict) -> WebhookLog:
        """Create a new webhook log record."""
        log = WebhookLog(**log_data)
        db.add(log)
        db.commit()
        db.refresh(log)
        return log

    @staticmethod
    def get_recent_logs(db, limit: int = 100):
        """Get recent webhook logs."""
        return db.query(WebhookLog).order_by(WebhookLog.created_at.desc()).limit(limit).all()

    @staticmethod
    def get_failed_requests(db, limit: int = 50):
        """Get failed webhook requests."""
        return db.query(WebhookLog).filter(WebhookLog.error.isnot(None)).order_by(WebhookLog.created_at.desc()).limit(limit).all()
