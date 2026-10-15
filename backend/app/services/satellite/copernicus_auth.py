import time
import httpx
import logging
from typing import Optional, Dict, Any
from app.core.config import settings

logger = logging.getLogger("illegal-mining-detection.satellite.auth")

class CopernicusAuthService:
    """
    OAuth2 token manager for Copernicus Data Space Ecosystem (CDSE)
    and Sentinel Hub APIs.
    """
    def __init__(self):
        self._access_token: Optional[str] = None
        self._token_expires_at: float = 0.0
        self._sentinelhub_token: Optional[str] = None
        self._sh_token_expires_at: float = 0.0

    @property
    def has_cdse_credentials(self) -> bool:
        return bool(
            (settings.COPERNICUS_CLIENT_ID and settings.COPERNICUS_CLIENT_SECRET) or
            (settings.CDSE_USERNAME and settings.CDSE_PASSWORD)
        )

    @property
    def has_sentinelhub_credentials(self) -> bool:
        return bool(settings.SENTINEL_HUB_CLIENT_ID and settings.SENTINEL_HUB_CLIENT_SECRET)

    async def get_cdse_token(self) -> Optional[str]:
        """
        Retrieves a valid OAuth2 access token for CDSE, requesting a new one
        if the current token is missing or near expiration.
        """
        if not self.has_cdse_credentials:
            return None

        # Return cached token if valid for at least 60 more seconds
        if self._access_token and time.time() < (self._token_expires_at - 60):
            return self._access_token

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                data: Dict[str, str] = {}
                if settings.COPERNICUS_CLIENT_ID and settings.COPERNICUS_CLIENT_SECRET:
                    data = {
                        "grant_type": "client_credentials",
                        "client_id": settings.COPERNICUS_CLIENT_ID,
                        "client_secret": settings.COPERNICUS_CLIENT_SECRET
                    }
                elif settings.CDSE_USERNAME and settings.CDSE_PASSWORD:
                    data = {
                        "grant_type": "password",
                        "username": settings.CDSE_USERNAME,
                        "password": settings.CDSE_PASSWORD,
                        "client_id": "cdse-public"
                    }

                resp = await client.post(settings.CDSE_AUTH_URL, data=data)
                if resp.status_code == 200:
                    token_data = resp.json()
                    self._access_token = token_data.get("access_token")
                    expires_in = token_data.get("expires_in", 3600)
                    self._token_expires_at = time.time() + float(expires_in)
                    logger.info("Successfully acquired new CDSE OAuth2 access token.")
                    return self._access_token
                else:
                    logger.warning(f"CDSE authentication failed: HTTP {resp.status_code} - {resp.text}")
                    return None
        except Exception as e:
            logger.error(f"CDSE authentication request error: {e}")
            return None

    async def get_auth_headers(self) -> Dict[str, str]:
        """Returns HTTP Authorization headers if authenticated, otherwise empty dict for public APIs."""
        token = await self.get_cdse_token()
        if token:
            return {"Authorization": f"Bearer {token}"}
        return {}

copernicus_auth = CopernicusAuthService()
