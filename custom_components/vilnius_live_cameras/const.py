"""Constants for Vilnius Live Cameras."""

from homeassistant.const import Platform

DOMAIN = "vilnius_live_cameras"
PLATFORMS = [Platform.CAMERA]

CAMERAS = (
    {
        "key": "national_philharmonic",
        "name": "Lietuvos nacionalinė filharmonija",
        "page_url": "https://lietuvoskameros.lt/lietuvos-nacionaline-filharmonija/",
        "still_image_url": None,
        "stream_source": None,
        "baltic_id": 5036,
        "generate_snapshot": True,
    },
    {
        "key": "white_bridge",
        "name": "Baltasis tiltas",
        "page_url": "https://lietuvoskameros.lt/baltasis-tiltas-tiesiogiai",
        "still_image_url": None,
        "stream_source": "https://tiesiogiai.kameros.com/stream/cam1.m3u8",
        "generate_snapshot": True,
    },
    {
        "key": "vilnius_panorama",
        "name": "Vilniaus miesto panorama",
        "page_url": "https://lietuvoskameros.lt/vilnius-tiesiogiai/",
        "still_image_url": None,
        "stream_source": "https://tiesiogiai.kameros.com/stream/cam2.m3u8",
        "generate_snapshot": True,
    },
    {
        "key": "st_johns_street",
        "name": "Šv. Jono gatvė",
        "page_url": "https://lietuvoskameros.lt/sv-jono-gatve-vilnius",
        "still_image_url": None,
        "stream_source": None,
        "baltic_id": 95327,
        "generate_snapshot": True,
    },
)
