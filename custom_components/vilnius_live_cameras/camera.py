"""Camera platform for Vilnius Live Cameras."""

from __future__ import annotations

from datetime import datetime, timedelta
import logging
from typing import Any

from homeassistant.components.camera import Camera, CameraEntityFeature
from homeassistant.components.ffmpeg import async_get_image
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.util import dt as dt_util

from .const import CAMERAS, DOMAIN
from .coordinator import VilniusLiveCamerasCoordinator

_LOGGER = logging.getLogger(__name__)
GENERATED_SNAPSHOT_MAX_AGE = timedelta(minutes=30)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Create all configured Vilnius camera entities."""
    coordinator: VilniusLiveCamerasCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(VilniusLiveCamera(camera, coordinator) for camera in CAMERAS)


class VilniusLiveCamera(Camera):
    """A camera backed by an upstream HLS stream or JPEG snapshot."""

    _attr_has_entity_name = True

    def __init__(self, camera: dict[str, Any], coordinator: VilniusLiveCamerasCoordinator) -> None:
        super().__init__()
        self._camera = camera
        self._coordinator = coordinator
        self._attr_unique_id = f"{DOMAIN}_{camera['key']}"
        self._attr_name = camera["name"]
        self._attr_content_type = "image/jpeg"
        self._generated_snapshot: bytes | None = None
        self._generated_snapshot_at: datetime | None = None
        if camera["stream_source"] is not None or camera.get("baltic_id") is not None:
            self._attr_supported_features = CameraEntityFeature.STREAM

    async def async_camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Fetch an upstream still or generate a recent frame from live HLS."""
        if self.still_image_url is None:
            if not self._camera.get("generate_snapshot"):
                return None
            now = dt_util.utcnow()
            if (
                self._generated_snapshot is not None
                and self._generated_snapshot_at is not None
                and now - self._generated_snapshot_at < GENERATED_SNAPSHOT_MAX_AGE
            ):
                return self._generated_snapshot
            source = await self.stream_source()
            if source is None:
                return self._generated_snapshot
            try:
                image = await async_get_image(self.hass, source)
                if image:
                    self._generated_snapshot = image
                    self._generated_snapshot_at = now
                return self._generated_snapshot
            except Exception as err:
                _LOGGER.warning(
                    "Unable to generate snapshot for %s: %s", self._camera["key"], err
                )
                return self._generated_snapshot
        session = async_get_clientsession(self.hass)
        try:
            async with session.get(self.still_image_url) as response:
                if response.status != 200:
                    return None
                return await response.read()
        except Exception as err:  # Keep the entity available if a source is down.
            _LOGGER.warning("Unable to fetch still image for %s: %s", self._camera["key"], err)
            return None

    @property
    def still_image_url(self) -> str | None:
        """Return the upstream JPEG snapshot, when one exists."""
        return self._camera["still_image_url"]

    async def stream_source(self) -> str | None:
        """Return the upstream HLS stream, when one exists."""
        return self._coordinator.data.get(self._camera["key"], self._camera["stream_source"])

    @property
    def available(self) -> bool:
        """Remain available for JPEG cameras if Baltic token refresh fails."""
        return self._camera["still_image_url"] is not None or self.stream_source is not None

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        """Expose the canonical source page for attribution and recovery."""
        return {"source_page": self._camera["page_url"]}
