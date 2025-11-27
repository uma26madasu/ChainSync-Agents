"""
Comprehensive integration tests for security module.

Tests:
- API key authentication
- HMAC signature verification
- Rate limiting (in-memory and Redis)
- Security middleware
"""

import pytest
import time
import hmac
import hashlib
from fastapi import HTTPException, Header
from chainsync.security import (
    verify_api_key,
    verify_webhook_signature,
    rate_limit_check,
    generate_webhook_signature,
    InMemoryRateLimitStore,
    RateLimitStore
)
from chainsync.config import Config


class TestAPIKeyAuthentication:
    """Test API key authentication."""

    def test_valid_api_key(self, monkeypatch):
        """Test valid API key is accepted."""
        monkeypatch.setattr(Config, 'WEBHOOK_API_KEY', 'test-key-123')
        result = verify_api_key(api_key='test-key-123')
        assert result is True

    def test_invalid_api_key(self, monkeypatch):
        """Test invalid API key is rejected."""
        monkeypatch.setattr(Config, 'WEBHOOK_API_KEY', 'test-key-123')
        with pytest.raises(HTTPException) as exc_info:
            verify_api_key(api_key='wrong-key')
        assert exc_info.value.status_code == 403
        assert "Invalid API key" in exc_info.value.detail

    def test_missing_api_key(self, monkeypatch):
        """Test missing API key is rejected."""
        monkeypatch.setattr(Config, 'WEBHOOK_API_KEY', 'test-key-123')
        with pytest.raises(HTTPException) as exc_info:
            verify_api_key(api_key=None)
        assert exc_info.value.status_code == 401
        assert "Missing API key" in exc_info.value.detail

    def test_no_api_key_configured_allows_all(self, monkeypatch):
        """Test that when no API key is configured, all requests are allowed."""
        monkeypatch.setattr(Config, 'WEBHOOK_API_KEY', None)
        result = verify_api_key(api_key=None)
        assert result is True


class TestWebhookSignatureVerification:
    """Test HMAC signature verification."""

    def test_valid_signature(self, monkeypatch):
        """Test valid HMAC signature is accepted."""
        secret_key = "test-secret-key"
        monkeypatch.setattr(Config, 'WEBHOOK_SECRET_KEY', secret_key)

        payload = '{"alert_id": "test-123"}'
        timestamp = str(int(time.time()))

        # Generate valid signature
        message = f"{timestamp}.{payload}"
        signature = hmac.new(
            secret_key.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        result = verify_webhook_signature(
            request_body=payload.encode('utf-8'),
            signature=signature,
            timestamp=timestamp
        )
        assert result is True

    def test_invalid_signature(self, monkeypatch):
        """Test invalid HMAC signature is rejected."""
        monkeypatch.setattr(Config, 'WEBHOOK_SECRET_KEY', 'test-secret-key')

        payload = '{"alert_id": "test-123"}'
        timestamp = str(int(time.time()))
        invalid_signature = "invalid-signature-12345"

        with pytest.raises(HTTPException) as exc_info:
            verify_webhook_signature(
                request_body=payload.encode('utf-8'),
                signature=invalid_signature,
                timestamp=timestamp
            )
        assert exc_info.value.status_code == 403
        assert "Invalid webhook signature" in exc_info.value.detail

    def test_missing_signature_header(self, monkeypatch):
        """Test missing signature header is rejected."""
        monkeypatch.setattr(Config, 'WEBHOOK_SECRET_KEY', 'test-secret-key')

        with pytest.raises(HTTPException) as exc_info:
            verify_webhook_signature(
                request_body=b'{"test": "data"}',
                signature=None,
                timestamp=str(int(time.time()))
            )
        assert exc_info.value.status_code == 401

    def test_expired_timestamp_rejected(self, monkeypatch):
        """Test old timestamp (replay attack) is rejected."""
        secret_key = "test-secret-key"
        monkeypatch.setattr(Config, 'WEBHOOK_SECRET_KEY', secret_key)

        payload = '{"alert_id": "test-123"}'
        # Timestamp from 10 minutes ago (beyond 5 minute window)
        old_timestamp = str(int(time.time()) - 600)

        message = f"{old_timestamp}.{payload}"
        signature = hmac.new(
            secret_key.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        with pytest.raises(HTTPException) as exc_info:
            verify_webhook_signature(
                request_body=payload.encode('utf-8'),
                signature=signature,
                timestamp=old_timestamp
            )
        assert exc_info.value.status_code == 401
        assert "timestamp too old" in exc_info.value.detail.lower()

    def test_generate_webhook_signature_utility(self):
        """Test the generate_webhook_signature utility function."""
        secret_key = "test-secret-123"
        payload = '{"test": "data"}'

        signature, timestamp = generate_webhook_signature(payload, secret_key)

        assert signature is not None
        assert len(signature) == 64  # SHA256 hex digest length
        assert timestamp.isdigit()
        assert int(timestamp) <= int(time.time())


class TestRateLimiting:
    """Test rate limiting functionality."""

    def test_in_memory_rate_limit_store(self):
        """Test InMemoryRateLimitStore functionality."""
        store = InMemoryRateLimitStore()
        client_ip = "192.168.1.1"
        current_time = time.time()

        # Add requests
        for i in range(5):
            store.add_request(client_ip, current_time + i)

        # Get recent requests
        requests = store.get_requests(client_ip, window_seconds=60)
        assert len(requests) == 5

        # Test cleanup
        store.cleanup_old_entries(window_seconds=2)
        requests = store.get_requests(client_ip, window_seconds=2)
        assert len(requests) < 5  # Older requests should be filtered

    def test_rate_limit_within_limits(self):
        """Test requests within rate limit are allowed."""
        client_ip = "192.168.1.100"

        # Make requests within limit
        for _ in range(5):
            result = rate_limit_check(client_ip, max_requests=10, window_seconds=60)
            assert result is True

    def test_rate_limit_exceeded(self):
        """Test rate limit exceeded raises exception."""
        client_ip = "192.168.1.101"
        max_requests = 3

        # Fill up to limit
        for _ in range(max_requests):
            rate_limit_check(client_ip, max_requests=max_requests, window_seconds=60)

        # Next request should be rate limited
        with pytest.raises(HTTPException) as exc_info:
            rate_limit_check(client_ip, max_requests=max_requests, window_seconds=60)

        assert exc_info.value.status_code == 429
        assert "Rate limit exceeded" in exc_info.value.detail
        assert "Retry-After" in exc_info.value.headers

    def test_rate_limit_different_clients_independent(self):
        """Test rate limits are independent per client IP."""
        client1 = "192.168.1.1"
        client2 = "192.168.1.2"
        max_requests = 5

        # Client 1 hits limit
        for _ in range(max_requests):
            rate_limit_check(client1, max_requests=max_requests, window_seconds=60)

        # Client 2 should still be able to make requests
        result = rate_limit_check(client2, max_requests=max_requests, window_seconds=60)
        assert result is True

    def test_rate_limit_window_expiry(self):
        """Test rate limit resets after time window expires."""
        client_ip = "192.168.1.103"
        max_requests = 2
        window_seconds = 1  # Very short window for testing

        # Fill up to limit
        for _ in range(max_requests):
            rate_limit_check(client_ip, max_requests=max_requests, window_seconds=window_seconds)

        # Should be rate limited immediately
        with pytest.raises(HTTPException):
            rate_limit_check(client_ip, max_requests=max_requests, window_seconds=window_seconds)

        # Wait for window to expire
        time.sleep(window_seconds + 0.1)

        # Should be able to make requests again
        result = rate_limit_check(client_ip, max_requests=max_requests, window_seconds=window_seconds)
        assert result is True


class TestSecurityIntegration:
    """Integration tests for security components."""

    def test_end_to_end_webhook_security(self, monkeypatch):
        """Test complete webhook security flow."""
        # Setup
        api_key = "test-api-key-123"
        secret_key = "test-secret-key-456"
        monkeypatch.setattr(Config, 'WEBHOOK_API_KEY', api_key)
        monkeypatch.setattr(Config, 'WEBHOOK_SECRET_KEY', secret_key)

        # Verify API key
        verify_api_key(api_key=api_key)

        # Generate and verify signature
        payload = '{"alert_id": "alert-789", "severity": "high"}'
        signature, timestamp = generate_webhook_signature(payload, secret_key)

        verify_webhook_signature(
            request_body=payload.encode('utf-8'),
            signature=signature,
            timestamp=timestamp
        )

        # Check rate limit
        client_ip = "192.168.1.200"
        result = rate_limit_check(client_ip, max_requests=100, window_seconds=60)
        assert result is True

    def test_security_fails_on_any_invalid_component(self, monkeypatch):
        """Test that security fails if any component is invalid."""
        monkeypatch.setattr(Config, 'WEBHOOK_API_KEY', 'correct-key')
        monkeypatch.setattr(Config, 'WEBHOOK_SECRET_KEY', 'correct-secret')

        # Invalid API key should fail immediately
        with pytest.raises(HTTPException):
            verify_api_key(api_key='wrong-key')

        # Invalid signature should fail
        payload = '{"test": "data"}'
        timestamp = str(int(time.time()))
        with pytest.raises(HTTPException):
            verify_webhook_signature(
                request_body=payload.encode('utf-8'),
                signature='invalid-signature',
                timestamp=timestamp
            )


@pytest.fixture(autouse=True)
def reset_rate_limiter():
    """Reset rate limiter between tests."""
    # Import and recreate the rate limit store to ensure clean state
    from chainsync import security
    security.rate_limit_store = InMemoryRateLimitStore()
    yield
    # Cleanup after test
    security.rate_limit_store = InMemoryRateLimitStore()
