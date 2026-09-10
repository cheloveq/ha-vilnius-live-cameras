# Vilnius Live Cameras

Home Assistant custom integration exposing five Vilnius live cameras from [LietuvosKameros.lt](https://lietuvoskameros.lt/).

## Included cameras

- Lietuvos nacionalinė filharmonija — Baltic Live Cam HLS stream with refreshed token and poster fallback
- Vilniaus TV bokštas — direct JPEG snapshot
- Baltasis tiltas — direct HLS stream (`cam1.m3u8`)
- Vilniaus miesto panorama — direct HLS stream (`cam2.m3u8`)
- Šv. Jono gatvė — Baltic Live Cam HLS stream with refreshed token and poster fallback

Install `custom_components/vilnius_live_cameras` into Home Assistant's `custom_components` directory, restart Home Assistant, then add **Vilnius Live Cameras** from Settings → Devices & services.

The two HLS entities require Home Assistant's built-in stream support for live playback. The other three provide an upstream JPEG image; the Baltic Live Cam images are current upstream poster endpoints rather than a locally generated snapshot.

The integration refreshes Baltic Live Cam authorization tokens every five minutes; tokenized stream URLs are intentionally not hard-coded. The upstream URLs and auth flow were verified on 2026-09-10. They are external sources and may change independently of this integration.
