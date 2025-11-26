"""
API Clients for ChainSync and Slotify integration

This module provides HTTP clients to interact with:
- Slotify API (meeting scheduling)
- ChainSync API (alert management)
"""

import httpx
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from .config import Config

logger = logging.getLogger(__name__)


class SlotifyAPIClient:
    """
    Client for Slotify Meeting Scheduling API.

    Provides methods to:
    - Create meetings
    - Update meetings
    - Cancel meetings
    - Get meeting details
    """

    def __init__(self):
        """Initialize Slotify API client."""
        self.api_url = Config.SLOTIFY_API_URL
        self.api_key = Config.SLOTIFY_API_KEY
        self.timeout = Config.SLOTIFY_TIMEOUT
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}" if self.api_key else ""
        }

    async def create_meeting(
        self,
        title: str,
        description: str,
        scheduled_time: str,
        duration_minutes: int,
        attendees: List[str],
        alert_reference: Optional[str] = None,
        organizer: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new meeting in Slotify.

        Args:
            title: Meeting title
            description: Meeting description/agenda
            scheduled_time: ISO timestamp for meeting start
            duration_minutes: Duration in minutes
            attendees: List of attendee email addresses
            alert_reference: Optional ChainSync alert ID
            organizer: Optional organizer email

        Returns:
            Dict with meeting details including meeting_id and meeting_url

        Raises:
            httpx.HTTPError: If API call fails
        """
        if not self.api_key:
            logger.warning("Slotify API key not configured. Returning mock meeting.")
            return self._mock_create_meeting(title, scheduled_time, attendees)

        payload = {
            "title": title,
            "description": description,
            "scheduled_time": scheduled_time,
            "duration_minutes": duration_minutes,
            "attendees": attendees
        }

        if alert_reference:
            payload["alert_reference"] = alert_reference

        if organizer:
            payload["organizer"] = organizer

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.api_url}/meetings",
                    json=payload,
                    headers=self.headers
                )
                response.raise_for_status()
                result = response.json()

                logger.info(f"Created Slotify meeting: {result.get('meeting_id')}")
                return result

        except httpx.HTTPError as e:
            logger.error(f"Failed to create Slotify meeting: {str(e)}")
            raise

    def _mock_create_meeting(self, title: str, scheduled_time: str, attendees: List[str]) -> Dict:
        """Return mock meeting data when API key is not configured."""
        meeting_id = f"slotify-mock-{datetime.now().timestamp()}"
        return {
            "meeting_id": meeting_id,
            "meeting_url": f"https://slotify.com/meetings/{meeting_id}",
            "title": title,
            "scheduled_time": scheduled_time,
            "attendees": attendees,
            "status": "scheduled",
            "mock": True
        }

    async def update_meeting(
        self,
        meeting_id: str,
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update an existing meeting.

        Args:
            meeting_id: Slotify meeting ID
            updates: Dict with fields to update

        Returns:
            Updated meeting details
        """
        if not self.api_key:
            logger.warning("Slotify API key not configured.")
            return {"meeting_id": meeting_id, "updated": True, "mock": True}

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.patch(
                    f"{self.api_url}/meetings/{meeting_id}",
                    json=updates,
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json()

        except httpx.HTTPError as e:
            logger.error(f"Failed to update meeting {meeting_id}: {str(e)}")
            raise

    async def cancel_meeting(self, meeting_id: str, reason: Optional[str] = None) -> Dict:
        """Cancel a meeting."""
        if not self.api_key:
            return {"meeting_id": meeting_id, "cancelled": True, "mock": True}

        payload = {"status": "cancelled"}
        if reason:
            payload["cancellation_reason"] = reason

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.api_url}/meetings/{meeting_id}/cancel",
                    json=payload,
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json()

        except httpx.HTTPError as e:
            logger.error(f"Failed to cancel meeting {meeting_id}: {str(e)}")
            raise

    async def get_meeting(self, meeting_id: str) -> Dict:
        """Get meeting details by ID."""
        if not self.api_key:
            return {"meeting_id": meeting_id, "mock": True}

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.api_url}/meetings/{meeting_id}",
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json()

        except httpx.HTTPError as e:
            logger.error(f"Failed to get meeting {meeting_id}: {str(e)}")
            raise


class ChainSyncAPIClient:
    """
    Client for ChainSync API.

    Provides methods to:
    - Get alert details
    - Update alert status
    - Add alert comments
    - Get facility data
    """

    def __init__(self):
        """Initialize ChainSync API client."""
        self.api_url = Config.CHAINSYNC_API_URL
        self.api_key = Config.CHAINSYNC_API_KEY
        self.timeout = Config.CHAINSYNC_TIMEOUT
        self.headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key if self.api_key else ""
        }

    async def get_alert(self, alert_id: str) -> Dict[str, Any]:
        """
        Get full alert details from ChainSync.

        Args:
            alert_id: ChainSync alert ID

        Returns:
            Alert details with full context
        """
        if not self.api_key:
            logger.warning("ChainSync API key not configured. Returning mock alert.")
            return {"alert_id": alert_id, "mock": True}

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.api_url}/alerts/{alert_id}",
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json()

        except httpx.HTTPError as e:
            logger.error(f"Failed to get alert {alert_id}: {str(e)}")
            raise

    async def update_alert_status(
        self,
        alert_id: str,
        status: str,
        meeting_url: Optional[str] = None,
        notes: Optional[str] = None
    ) -> Dict:
        """
        Update alert status and attach meeting information.

        Args:
            alert_id: ChainSync alert ID
            status: New status (acknowledged, investigating, resolved, etc.)
            meeting_url: Optional Slotify meeting URL
            notes: Optional notes

        Returns:
            Updated alert data
        """
        if not self.api_key:
            return {"alert_id": alert_id, "status": status, "updated": True, "mock": True}

        payload = {"status": status}

        if meeting_url:
            payload["meeting_url"] = meeting_url

        if notes:
            payload["notes"] = notes

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.patch(
                    f"{self.api_url}/alerts/{alert_id}",
                    json=payload,
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json()

        except httpx.HTTPError as e:
            logger.error(f"Failed to update alert {alert_id}: {str(e)}")
            raise

    async def add_alert_comment(self, alert_id: str, comment: str, author: str = "AI Agent") -> Dict:
        """Add a comment to an alert."""
        if not self.api_key:
            return {"alert_id": alert_id, "comment_added": True, "mock": True}

        payload = {
            "comment": comment,
            "author": author,
            "timestamp": datetime.now().isoformat()
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.api_url}/alerts/{alert_id}/comments",
                    json=payload,
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json()

        except httpx.HTTPError as e:
            logger.error(f"Failed to add comment to alert {alert_id}: {str(e)}")
            raise

    async def get_facility_data(self, facility_id: str) -> Dict:
        """Get facility data from ChainSync."""
        if not self.api_key:
            return {"facility_id": facility_id, "mock": True}

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.api_url}/facilities/{facility_id}",
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json()

        except httpx.HTTPError as e:
            logger.error(f"Failed to get facility {facility_id}: {str(e)}")
            raise
