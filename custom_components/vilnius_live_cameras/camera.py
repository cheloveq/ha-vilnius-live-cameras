"""Camera platform for Vilnius Live Cameras."""

from __future__ import annotations

from typing import Any

from homeassistant.components.camera import Camera
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CAMERAS, DOMAIN
from .coordinator import VilniusLiveCamerasCoordinator


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

    @property
    def still_image_url(self) -> str | None:
        """Return the upstream JPEG snapshot, when one exists."""
        return self._camera["still_image_url"]

    @property
    def stream_source(self) -> str | None:
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
