"""Tests for the static Vilnius camera catalog."""

from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).parents[1]
COMPONENT = ROOT / "custom_components" / "vilnius_live_cameras"


class CameraCatalogTestCase(unittest.TestCase):
    """Keep the configured sources complete and unambiguous."""

    def test_manifest_is_hacs_compatible(self) -> None:
        manifest = json.loads((COMPONENT / "manifest.json").read_text())
        self.assertEqual(manifest["domain"], "vilnius_live_cameras")
        self.assertTrue(manifest["config_flow"])
        self.assertEqual(manifest["version"], "0.1.4")

    def test_catalog_contains_the_four_live_cameras(self) -> None:
        source = (COMPONENT / "const.py").read_text()
        for key in (
            "national_philharmonic",
            "white_bridge",
            "vilnius_panorama",
            "st_johns_street",
        ):
            self.assertIn(f'"key": "{key}"', source)
        self.assertEqual(source.count('"key": '), 4)
        self.assertNotIn("tv_tower", source)

    def test_stream_and_snapshot_urls_are_https(self) -> None:
        source = (COMPONENT / "const.py").read_text()
        self.assertIn("https://tiesiogiai.kameros.com/stream/cam1.m3u8", source)
        self.assertIn("https://tiesiogiai.kameros.com/stream/cam2.m3u8", source)
        self.assertIn("https://thumbs.balticlivecam.com/blc/VilniusRamda.jpg", source)
        self.assertIn("https://thumbs.balticlivecam.com/blc/VilniusNarutis2.jpg", source)
        self.assertIn("vlcsnap-2025-06-07-15h25m49s037.png", source)
        self.assertIn("vlcsnap-2025-06-07-15h22m30s201.png", source)

    def test_baltic_auth_refresh_is_not_hard_coded(self) -> None:
        source = (COMPONENT / "coordinator.py").read_text()
        self.assertIn("action", source)
        self.assertIn("auth_token", source)
        self.assertIn("timedelta(minutes=5)", source)
        self.assertIn("STREAM_PATTERN", source)
        self.assertIn("X-Requested-With", source)
        self.assertIn("User-Agent", source)

    def test_camera_implements_ha_2026_camera_hooks(self) -> None:
        source = (COMPONENT / "camera.py").read_text()
        self.assertIn("async def async_camera_image", source)
        self.assertIn("async def stream_source", source)
        self.assertIn("CameraEntityFeature.STREAM", source)


if __name__ == "__main__":
    unittest.main()
