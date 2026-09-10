# Vilnius Live Cameras

Home Assistant custom integration exposing four Vilnius live cameras from [LietuvosKameros.lt](https://lietuvoskameros.lt/).

## Included cameras

- Lietuvos nacionalinė filharmonija — Baltic Live Cam HLS stream with refreshed token and poster fallback
- Baltasis tiltas — direct HLS stream (`cam1.m3u8`)
- Vilniaus miesto panorama — direct HLS stream (`cam2.m3u8`)
- Šv. Jono gatvė — Baltic Live Cam HLS stream with refreshed token and poster fallback

Install `custom_components/vilnius_live_cameras` into Home Assistant's `custom_components` directory, restart Home Assistant, then add **Vilnius Live Cameras** from Settings → Devices & services.

The two direct HLS entities require Home Assistant's built-in stream support for live playback. The Baltic Live Cam entities use current upstream poster endpoints as fallbacks rather than locally generated snapshots.

The integration refreshes Baltic Live Cam authorization tokens every five minutes; tokenized stream URLs are intentionally not hard-coded. The upstream URLs and auth flow were verified on 2026-09-10. They are external sources and may change independently of this integration.

## HACS installation

1. Install HACS if it is not already installed.
2. In HACS, open **Integrations**, choose the three-dot menu, and select **Custom repositories**.
3. Add `https://github.com/cheloveq/ha-vilnius-live-cameras` as an **Integration**.
4. Install **Vilnius Live Cameras**, restart Home Assistant, and add it from Settings → Devices & services.

The repository is public so HACS can access it directly. The integration creates four camera entities.
