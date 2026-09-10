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
        self.assertEqual(manifest["version"], "0.1.0")

    def test_catalog_contains_the_five_requested_cameras(self) -> None:
        source = (COMPONENT / "const.py").read_text()
        for key in (
            "national_philharmonic",
            "tv_tower",
            "white_bridge",
            "vilnius_panorama",
            "st_johns_street",
        ):
            self.assertIn(f'"key": "{key}"', source)
        self.assertEqual(source.count('"key": '), 5)

    def test_stream_and_snapshot_urls_are_https(self) -> None:
        source = (COMPONENT / "const.py").read_text()
        self.assertIn("https://tiesiogiai.kameros.com/stream/cam1.m3u8", source)
        self.assertIn("https://tiesiogiai.kameros.com/stream/cam2.m3u8", source)
        self.assertIn("https://map.sviesoforai.lt/camera/api/camera/Camera_048.jpg", source)
        self.assertIn("https://thumbs.balticlivecam.com/blc/VilniusRamda.jpg", source)
        self.assertIn("https://thumbs.balticlivecam.com/blc/VilniusNarutis2.jpg", source)


if __name__ == "__main__":
    unittest.main()

