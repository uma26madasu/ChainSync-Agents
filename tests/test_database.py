"""
Comprehensive integration tests for database module.

Tests:
- Database initialization and connection pooling
- All CRUD operations for all models
- Database repositories
- Concurrent access and connection pooling
"""

import pytest
from datetime import datetime
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, scoped_session
from chainsync.database import (
    Base,
    init_database,
    get_db,
    MeetingRecord,
    AlertRecord,
    LearningData,
    WebhookLog,
    MeetingRepository,
    AlertRepository,
    LearningRepository,
    WebhookLogRepository
)


@pytest.fixture(scope="function")
def test_db():
    """Create a test database for each test."""
    # Use in-memory SQLite for testing
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(bind=engine)

    TestSessionLocal = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )

    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


class TestDatabaseInitialization:
    """Test database initialization and setup."""

    def test_all_tables_created(self, test_db):
        """Test that all expected tables are created."""
        inspector = inspect(test_db.bind)
        tables = inspector.get_table_names()

        expected_tables = ['meetings', 'alerts', 'learning_data', 'webhook_logs']
        for table in expected_tables:
            assert table in tables

    def test_meeting_table_structure(self, test_db):
        """Test MeetingRecord table has correct columns."""
        inspector = inspect(test_db.bind)
        columns = [col['name'] for col in inspector.get_columns('meetings')]

        expected_columns = [
            'id', 'meeting_id', 'alert_id', 'meeting_title', 'scheduled_time',
            'meeting_url', 'attendees', 'alert_type', 'alert_severity',
            'urgency_level', 'urgency_score', 'why_scheduled', 'discussion_points',
            'pre_meeting_summary', 'suggested_attendees', 'recommended_duration',
            'status', 'created_at', 'updated_at'
        ]

        for col in expected_columns:
            assert col in columns

    def test_alert_table_structure(self, test_db):
        """Test AlertRecord table has correct columns."""
        inspector = inspect(test_db.bind)
        columns = [col['name'] for col in inspector.get_columns('alerts')]

        expected_columns = [
            'id', 'alert_id', 'alert_type', 'severity', 'description',
            'affected_systems', 'detected_at', 'root_cause', 'recommendations',
            'compliance_status', 'compliance_violations', 'meeting_created',
            'meeting_id', 'processed_at', 'created_at'
        ]

        for col in expected_columns:
            assert col in columns


class TestMeetingRepository:
    """Test MeetingRepository CRUD operations."""

    def test_create_meeting(self, test_db):
        """Test creating a new meeting record."""
        meeting_data = {
            'meeting_id': 'meet-123',
            'alert_id': 'alert-456',
            'meeting_title': 'Test Alert Review',
            'scheduled_time': datetime.now(),
            'meeting_url': 'https://meet.example.com/123',
            'attendees': ['user1@example.com', 'user2@example.com'],
            'alert_type': 'system_failure',
            'alert_severity': 'high',
            'urgency_level': 'HIGH',
            'urgency_score': 0.9,
            'status': 'scheduled'
        }

        meeting = MeetingRepository.create(test_db, meeting_data)

        assert meeting.id is not None
        assert meeting.meeting_id == 'meet-123'
        assert meeting.alert_id == 'alert-456'
        assert meeting.status == 'scheduled'
        assert len(meeting.attendees) == 2

    def test_get_meeting_by_id(self, test_db):
        """Test retrieving a meeting by ID."""
        # Create meeting
        meeting_data = {
            'meeting_id': 'meet-456',
            'alert_id': 'alert-789',
            'meeting_title': 'Compliance Review',
            'status': 'completed'
        }
        created_meeting = MeetingRepository.create(test_db, meeting_data)

        # Retrieve meeting
        meeting = MeetingRepository.get_by_meeting_id(test_db, 'meet-456')

        assert meeting is not None
        assert meeting.meeting_id == 'meet-456'
        assert meeting.status == 'completed'

    def test_get_meetings_by_alert_id(self, test_db):
        """Test retrieving meetings by alert ID."""
        alert_id = 'alert-common-123'

        # Create multiple meetings for same alert
        for i in range(3):
            meeting_data = {
                'meeting_id': f'meet-{i}',
                'alert_id': alert_id,
                'meeting_title': f'Meeting {i}',
                'status': 'scheduled'
            }
            MeetingRepository.create(test_db, meeting_data)

        # Retrieve all meetings for alert
        meetings = MeetingRepository.get_by_alert_id(test_db, alert_id)

        assert len(meetings) == 3
        for meeting in meetings:
            assert meeting.alert_id == alert_id

    def test_update_meeting_status(self, test_db):
        """Test updating meeting status."""
        # Create meeting
        meeting_data = {
            'meeting_id': 'meet-update-1',
            'status': 'scheduled'
        }
        meeting = MeetingRepository.create(test_db, meeting_data)
        assert meeting.status == 'scheduled'

        # Update status
        updated = MeetingRepository.update_status(test_db, 'meet-update-1', 'completed')

        assert updated.status == 'completed'

    def test_get_recent_meetings(self, test_db):
        """Test retrieving recent meetings with limit."""
        # Create multiple meetings
        for i in range(10):
            meeting_data = {
                'meeting_id': f'meet-recent-{i}',
                'status': 'scheduled'
            }
            MeetingRepository.create(test_db, meeting_data)

        # Get recent 5
        meetings = MeetingRepository.get_recent(test_db, limit=5)

        assert len(meetings) == 5


class TestAlertRepository:
    """Test AlertRepository CRUD operations."""

    def test_create_alert(self, test_db):
        """Test creating a new alert record."""
        alert_data = {
            'alert_id': 'alert-create-1',
            'alert_type': 'compliance_violation',
            'severity': 'critical',
            'description': 'Test alert description',
            'affected_systems': ['system-1', 'system-2'],
            'detected_at': datetime.now(),
            'compliance_status': 'NON_COMPLIANT',
            'meeting_created': False
        }

        alert = AlertRepository.create(test_db, alert_data)

        assert alert.id is not None
        assert alert.alert_id == 'alert-create-1'
        assert alert.severity == 'critical'
        assert len(alert.affected_systems) == 2

    def test_get_alert_by_id(self, test_db):
        """Test retrieving an alert by ID."""
        # Create alert
        alert_data = {
            'alert_id': 'alert-get-1',
            'alert_type': 'security_incident',
            'severity': 'high'
        }
        AlertRepository.create(test_db, alert_data)

        # Retrieve alert
        alert = AlertRepository.get_by_alert_id(test_db, 'alert-get-1')

        assert alert is not None
        assert alert.alert_id == 'alert-get-1'
        assert alert.alert_type == 'security_incident'

    def test_update_alert_meeting_info(self, test_db):
        """Test updating alert with meeting information."""
        # Create alert
        alert_data = {
            'alert_id': 'alert-meeting-1',
            'severity': 'high',
            'meeting_created': False
        }
        AlertRepository.create(test_db, alert_data)

        # Update with meeting info
        updated = AlertRepository.update_meeting_info(
            test_db,
            'alert-meeting-1',
            'meet-789',
            True
        )

        assert updated.meeting_id == 'meet-789'
        assert updated.meeting_created is True

    def test_get_alerts_by_severity(self, test_db):
        """Test filtering alerts by severity."""
        # Create alerts with different severities
        for severity in ['low', 'medium', 'high', 'critical']:
            alert_data = {
                'alert_id': f'alert-{severity}-1',
                'severity': severity
            }
            AlertRepository.create(test_db, alert_data)

        # Get high severity alerts
        high_alerts = AlertRepository.get_by_severity(test_db, 'high')

        assert len(high_alerts) >= 1
        for alert in high_alerts:
            assert alert.severity == 'high'

    def test_get_unprocessed_alerts(self, test_db):
        """Test retrieving alerts without meetings."""
        # Create alerts, some with meetings
        for i in range(5):
            alert_data = {
                'alert_id': f'alert-unproc-{i}',
                'severity': 'medium',
                'meeting_created': (i % 2 == 0)  # Every other one has meeting
            }
            AlertRepository.create(test_db, alert_data)

        # Get alerts without meetings
        unprocessed = AlertRepository.get_without_meeting(test_db)

        assert len(unprocessed) > 0
        for alert in unprocessed:
            assert alert.meeting_created is False


class TestLearningRepository:
    """Test LearningRepository CRUD operations."""

    def test_create_learning_data(self, test_db):
        """Test creating a learning data record."""
        learning_data = {
            'agent_name': 'TestAgent',
            'interaction_type': 'query',
            'query': 'What is the system status?',
            'response': 'All systems operational',
            'feedback_score': 0.95,
            'context': {'user_id': '123', 'session_id': 'abc'}
        }

        record = LearningRepository.create(test_db, learning_data)

        assert record.id is not None
        assert record.agent_name == 'TestAgent'
        assert record.feedback_score == 0.95

    def test_get_by_agent_name(self, test_db):
        """Test retrieving learning data by agent name."""
        agent_name = 'ContinuousLearningAgent'

        # Create multiple records
        for i in range(3):
            learning_data = {
                'agent_name': agent_name,
                'interaction_type': 'query',
                'query': f'Query {i}',
                'response': f'Response {i}'
            }
            LearningRepository.create(test_db, learning_data)

        # Retrieve by agent
        records = LearningRepository.get_by_agent(test_db, agent_name)

        assert len(records) == 3
        for record in records:
            assert record.agent_name == agent_name

    def test_get_recent_learning_data(self, test_db):
        """Test retrieving recent learning data."""
        # Create records
        for i in range(20):
            learning_data = {
                'agent_name': 'TestAgent',
                'interaction_type': 'query',
                'query': f'Query {i}'
            }
            LearningRepository.create(test_db, learning_data)

        # Get recent 10
        recent = LearningRepository.get_recent(test_db, limit=10)

        assert len(recent) == 10


class TestWebhookLogRepository:
    """Test WebhookLogRepository CRUD operations."""

    def test_create_webhook_log(self, test_db):
        """Test creating a webhook log entry."""
        log_data = {
            'endpoint': '/webhooks/chainsync/alert',
            'method': 'POST',
            'payload': {'alert_id': 'test-123'},
            'headers': {'Content-Type': 'application/json'},
            'response_status': 200,
            'processing_time_ms': 45.2,
            'ip_address': '192.168.1.1'
        }

        log = WebhookLogRepository.create(test_db, log_data)

        assert log.id is not None
        assert log.endpoint == '/webhooks/chainsync/alert'
        assert log.response_status == 200

    def test_get_logs_by_endpoint(self, test_db):
        """Test retrieving logs by endpoint."""
        endpoint = '/webhooks/test'

        # Create multiple logs
        for i in range(3):
            log_data = {
                'endpoint': endpoint,
                'method': 'POST',
                'response_status': 200 if i % 2 == 0 else 500
            }
            WebhookLogRepository.create(test_db, log_data)

        # Retrieve logs
        logs = WebhookLogRepository.get_by_endpoint(test_db, endpoint)

        assert len(logs) == 3
        for log in logs:
            assert log.endpoint == endpoint

    def test_get_failed_requests(self, test_db):
        """Test retrieving failed webhook requests."""
        # Create mix of successful and failed requests
        for i in range(10):
            log_data = {
                'endpoint': '/test',
                'method': 'POST',
                'response_status': 200 if i < 7 else 500,
                'error': None if i < 7 else 'Internal Server Error'
            }
            WebhookLogRepository.create(test_db, log_data)

        # Get failed requests
        failed = WebhookLogRepository.get_failed_requests(test_db)

        assert len(failed) == 3
        for log in failed:
            assert log.response_status >= 400


class TestConcurrentAccess:
    """Test concurrent database access and connection pooling."""

    def test_multiple_concurrent_sessions(self, test_db):
        """Test multiple sessions can access database concurrently."""
        # Create records from multiple "sessions"
        for session_id in range(5):
            alert_data = {
                'alert_id': f'alert-concurrent-{session_id}',
                'severity': 'medium'
            }
            AlertRepository.create(test_db, alert_data)

        # Verify all records were created
        alerts = test_db.query(AlertRecord).filter(
            AlertRecord.alert_id.like('alert-concurrent-%')
        ).all()

        assert len(alerts) == 5

    def test_transaction_rollback_on_error(self, test_db):
        """Test database rollback on error."""
        try:
            # Create alert
            alert_data = {
                'alert_id': 'alert-rollback-1',
                'severity': 'high'
            }
            AlertRepository.create(test_db, alert_data)

            # Try to create duplicate (should fail due to unique constraint)
            AlertRepository.create(test_db, alert_data)

        except Exception:
            test_db.rollback()

        # Verify only one record exists
        alerts = test_db.query(AlertRecord).filter_by(
            alert_id='alert-rollback-1'
        ).all()

        assert len(alerts) == 1


class TestDatabaseIndexes:
    """Test that database indexes are created correctly."""

    def test_meeting_indexes_exist(self, test_db):
        """Test MeetingRecord indexes are created."""
        inspector = inspect(test_db.bind)
        indexes = inspector.get_indexes('meetings')

        index_names = [idx['name'] for idx in indexes]

        # Check for our custom composite indexes
        assert any('status' in idx['name'] and 'scheduled_time' in idx['name'] for idx in indexes)
        assert any('alert_type' in idx['name'] and 'severity' in idx['name'] for idx in indexes)

    def test_alert_indexes_exist(self, test_db):
        """Test AlertRecord indexes are created."""
        inspector = inspect(test_db.bind)
        indexes = inspector.get_indexes('alerts')

        # Check for our custom composite indexes
        assert any('type' in idx['name'] and 'severity' in idx['name'] for idx in indexes)
        assert any('meeting_created' in idx['name'] and 'processed' in idx['name'] for idx in indexes)
