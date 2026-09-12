"""Token-refresh coordinator for Baltic Live Cam streams."""

from __future__ import annotations

from datetime import timedelta
import logging
import re

from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import CAMERAS, DOMAIN

_LOGGER = logging.getLogger(__name__)
AUTH_URL = "https://balticlivecam.com/wp-admin/admin-ajax.php"
REQUEST_HEADERS = {
    "Origin": "https://balticlivecam.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/152 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}
STREAM_PATTERN = re.compile(r"https://edge[^']+/index\.m3u8\?token=[^']+")


class VilniusLiveCamerasCoordinator(DataUpdateCoordinator[dict[str, str]]):
    """Refresh tokenized Baltic Live Cam HLS URLs."""

    def __init__(self, hass) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=5),
        )

    async def _async_update_data(self) -> dict[str, str]:
        session = async_get_clientsession(self.hass)
        # Preserve a previously working token when one refresh encounters a
        # transient upstream failure.
        streams: dict[str, str] = dict(self.data or {})
        for camera in CAMERAS:
            camera_id = camera.get("baltic_id")
            if camera_id is None:
                continue
            try:
                async with session.post(
                    AUTH_URL,
                    data={
                        "action": "auth_token",
                        "id": camera_id,
                        "embed": 0,
                        "main_referer": camera["page_url"],
                    },
                    headers={**REQUEST_HEADERS, "Referer": camera["page_url"]},
                ) as response:
                    if response.status != 200:
                        _LOGGER.warning("Baltic Live Cam auth returned HTTP %s for %s", response.status, camera["key"])
                        continue
                    match = STREAM_PATTERN.search(await response.text())
                    if match:
                        streams[camera["key"]] = match.group(0)
                    else:
                        _LOGGER.warning("Baltic Live Cam auth response had no stream for %s", camera["key"])
            except Exception as err:  # Keep other cameras usable if one source fails.
                _LOGGER.warning("Unable to refresh Baltic Live Cam stream for %s: %s", camera["key"], err)
        if not streams:
            # Make initial setup retryable instead of loading cameras whose
            # tokenized streams remain absent until a manual reload.
            raise UpdateFailed("Unable to obtain any Baltic Live Cam stream URLs")
        return streams
