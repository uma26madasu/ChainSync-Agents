"""
Security utilities for webhook authentication and authorization

Provides:
- API key authentication
- HMAC signature verification
- Rate limiting
- Security middleware for FastAPI
"""

import hmac
import hashlib
import time
from typing import Optional
from fastapi import HTTPException, Request, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .config import Config
import logging

logger = logging.getLogger(__name__)

# Simple in-memory rate limiter
rate_limit_store = {}


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
        logger.warning(f"Invalid API key attempt: {api_key[:10]}...")
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
    Simple in-memory rate limiting.

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

    # Clean up old entries
    for ip in list(rate_limit_store.keys()):
        rate_limit_store[ip] = [
            timestamp for timestamp in rate_limit_store[ip]
            if current_time - timestamp < window_seconds
        ]
        if not rate_limit_store[ip]:
            del rate_limit_store[ip]

    # Check rate limit
    if client_ip not in rate_limit_store:
        rate_limit_store[client_ip] = []

    request_times = rate_limit_store[client_ip]

    if len(request_times) >= max_requests:
        retry_after = int(window_seconds - (current_time - request_times[0]))
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Try again in {retry_after} seconds.",
            headers={"Retry-After": str(retry_after)}
        )

    # Add current request
    rate_limit_store[client_ip].append(current_time)
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
