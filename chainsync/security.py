"""
Security utilities for webhook authentication and authorization

Provides:
- API key authentication
- HMAC signature verification
- Rate limiting (with optional Redis support for distributed deployments)
- Security middleware for FastAPI
"""

import hmac
import hashlib
import time
from typing import Optional, List
from abc import ABC, abstractmethod
from fastapi import HTTPException, Request, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .config import Config
import logging

logger = logging.getLogger(__name__)


class RateLimitStore(ABC):
    """Abstract interface for rate limit storage."""

    @abstractmethod
    def add_request(self, client_ip: str, timestamp: float):
        """Add a request timestamp for a client IP."""
        pass

    @abstractmethod
    def get_requests(self, client_ip: str, window_seconds: int) -> List[float]:
        """Get recent requests for a client IP within the time window."""
        pass

    @abstractmethod
    def cleanup_old_entries(self, window_seconds: int):
        """Clean up expired entries."""
        pass


class InMemoryRateLimitStore(RateLimitStore):
    """In-memory rate limit storage (not suitable for multi-process deployments)."""

    def __init__(self):
        self.store = {}
        logger.warning("Using in-memory rate limiting. Not suitable for distributed deployments. Consider using Redis.")

    def add_request(self, client_ip: str, timestamp: float):
        if client_ip not in self.store:
            self.store[client_ip] = []
        self.store[client_ip].append(timestamp)

    def get_requests(self, client_ip: str, window_seconds: int) -> List[float]:
        current_time = time.time()
        if client_ip not in self.store:
            return []
        # Filter to only recent requests
        recent = [ts for ts in self.store[client_ip] if current_time - ts < window_seconds]
        self.store[client_ip] = recent
        return recent

    def cleanup_old_entries(self, window_seconds: int):
        current_time = time.time()
        for ip in list(self.store.keys()):
            self.store[ip] = [ts for ts in self.store[ip] if current_time - ts < window_seconds]
            if not self.store[ip]:
                del self.store[ip]


class RedisRateLimitStore(RateLimitStore):
    """Redis-based rate limit storage (suitable for distributed deployments)."""

    def __init__(self, redis_client):
        self.redis = redis_client
        logger.info("Using Redis for rate limiting (distributed deployment ready)")

    def add_request(self, client_ip: str, timestamp: float):
        key = f"rate_limit:{client_ip}"
        self.redis.zadd(key, {str(timestamp): timestamp})

    def get_requests(self, client_ip: str, window_seconds: int) -> List[float]:
        key = f"rate_limit:{client_ip}"
        current_time = time.time()
        min_time = current_time - window_seconds

        # Remove old entries
        self.redis.zremrangebyscore(key, 0, min_time)

        # Get recent requests
        timestamps = self.redis.zrange(key, 0, -1)
        return [float(ts) for ts in timestamps]

    def cleanup_old_entries(self, window_seconds: int):
        # Redis handles expiration, but we can set TTL on keys
        # This is called periodically but Redis auto-expires
        pass


# Initialize rate limit store
def _init_rate_limit_store() -> RateLimitStore:
    """Initialize rate limit store (Redis if available, otherwise in-memory)."""
    redis_url = Config.DATABASE_URL if hasattr(Config, 'REDIS_URL') else None

    try:
        import redis
        redis_url = getattr(Config, 'REDIS_URL', None)
        if redis_url:
            redis_client = redis.from_url(redis_url, decode_responses=True)
            # Test connection
            redis_client.ping()
            return RedisRateLimitStore(redis_client)
    except (ImportError, Exception) as e:
        if isinstance(e, ImportError):
            logger.info("Redis not installed. Using in-memory rate limiting.")
        else:
            logger.warning(f"Failed to connect to Redis: {e}. Falling back to in-memory rate limiting.")

    return InMemoryRateLimitStore()


# Global rate limit store
rate_limit_store = _init_rate_limit_store()


def verify_api_key(api_key: Optional[str] = Header(None, alias="X-API-Key")) -> bool:
    """
    Verify API key from request header.

    Args:
        api_key: API key from X-API-Key header

    Returns:
        True if valid

    Raises:
        HTTPException: If API key is missing or invalid
    """
    if not Config.WEBHOOK_API_KEY:
        # If no API key configured, allow all requests (development mode)
        logger.warning("Webhook API key not configured - security disabled")
        return True

    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="Missing API key. Include X-API-Key header.",
            headers={"WWW-Authenticate": "ApiKey"}
        )

    if api_key != Config.WEBHOOK_API_KEY:
        logger.warning("Invalid API key attempt detected")
        raise HTTPException(
            status_code=403,
            detail="Invalid API key"
        )

    return True


def verify_webhook_signature(
    request_body: bytes,
    signature: Optional[str] = Header(None, alias="X-Webhook-Signature"),
    timestamp: Optional[str] = Header(None, alias="X-Webhook-Timestamp")
) -> bool:
    """
    Verify HMAC signature of webhook request.

    This prevents replay attacks and ensures request integrity.

    Args:
        request_body: Raw request body bytes
        signature: HMAC signature from X-Webhook-Signature header
        timestamp: Request timestamp from X-Webhook-Timestamp header

    Returns:
        True if signature is valid

    Raises:
        HTTPException: If signature is missing or invalid
    """
    if not Config.WEBHOOK_SECRET_KEY:
        # If no secret key configured, skip signature verification
        logger.warning("Webhook secret key not configured - signature verification disabled")
        return True

    if not signature or not timestamp:
        raise HTTPException(
            status_code=401,
            detail="Missing webhook signature or timestamp headers"
        )

    # Check timestamp to prevent replay attacks (allow 5 minute window)
    try:
        request_time = int(timestamp)
        current_time = int(time.time())
        time_diff = abs(current_time - request_time)

        if time_diff > 300:  # 5 minutes
            raise HTTPException(
                status_code=401,
                detail="Request timestamp too old. Possible replay attack."
            )
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid timestamp format"
        )

    # Compute expected signature
    message = f"{timestamp}.{request_body.decode('utf-8')}"
    expected_signature = hmac.new(
        Config.WEBHOOK_SECRET_KEY.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    # Compare signatures (constant-time comparison to prevent timing attacks)
    if not hmac.compare_digest(signature, expected_signature):
        logger.warning("Invalid webhook signature")
        raise HTTPException(
            status_code=403,
            detail="Invalid webhook signature"
        )

    return True


def rate_limit_check(
    client_ip: str,
    max_requests: int = 100,
    window_seconds: int = 60
) -> bool:
    """
    Rate limiting with pluggable storage backend (in-memory or Redis).

    Args:
        client_ip: Client IP address
        max_requests: Maximum requests allowed in window
        window_seconds: Time window in seconds

    Returns:
        True if within rate limit

    Raises:
        HTTPException: If rate limit exceeded
    """
    current_time = time.time()

    # Get recent requests for this client
    request_times = rate_limit_store.get_requests(client_ip, window_seconds)

    # Check if limit exceeded
    if len(request_times) >= max_requests:
        oldest_request = min(request_times) if request_times else current_time
        retry_after = int(window_seconds - (current_time - oldest_request))
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Try again in {retry_after} seconds.",
            headers={"Retry-After": str(max(1, retry_after))}
        )

    # Add current request
    rate_limit_store.add_request(client_ip, current_time)

    # Periodically cleanup (every ~100 requests)
    import random
    if random.randint(1, 100) == 1:
        rate_limit_store.cleanup_old_entries(window_seconds)

    return True


async def security_middleware(request: Request):
    """
    Combined security middleware for webhook endpoints.

    Performs:
    1. Rate limiting
    2. API key verification
    3. Signature verification (for POST requests)

    Args:
        request: FastAPI Request object

    Returns:
        True if all security checks pass

    Raises:
        HTTPException: If any security check fails
    """
    # Get client IP
    client_ip = request.client.host if request.client else "unknown"

    # Rate limiting
    rate_limit_check(client_ip)

    # API key verification
    api_key = request.headers.get("X-API-Key")
    verify_api_key(api_key)

    # Signature verification for POST/PUT/PATCH requests
    if request.method in ["POST", "PUT", "PATCH"]:
        body = await request.body()
        signature = request.headers.get("X-Webhook-Signature")
        timestamp = request.headers.get("X-Webhook-Timestamp")
        verify_webhook_signature(body, signature, timestamp)

    return True


def generate_webhook_signature(payload: str, secret_key: str = None) -> tuple:
    """
    Generate HMAC signature for webhook payload.

    This is a utility function for testing or for webhook clients to
    generate proper signatures when sending requests.

    Args:
        payload: JSON payload as string
        secret_key: Secret key (defaults to Config.WEBHOOK_SECRET_KEY)

    Returns:
        Tuple of (signature, timestamp)
    """
    if secret_key is None:
        secret_key = Config.WEBHOOK_SECRET_KEY

    if not secret_key:
        raise ValueError("Secret key not provided")

    timestamp = str(int(time.time()))
    message = f"{timestamp}.{payload}"

    signature = hmac.new(
        secret_key.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    return signature, timestamp


# Dependency for FastAPI
def get_current_api_key(api_key: str = Header(..., alias="X-API-Key")) -> str:
    """FastAPI dependency for API key authentication."""
    verify_api_key(api_key)
    return api_key
