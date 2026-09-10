# Isolated Home Assistant test environment

This harness runs Home Assistant locally on port `8124`, with its own config
and storage under `.ha-test/config`. It never mounts or writes MediaCenter's
configuration. The integration source is mounted read-only from the parent
project, so code changes are visible after a container restart.

The image is pinned to HA `2026.9.0`, matching MediaCenter at setup time.

## Commands

From the repository root:

```sh
./.ha-test/run.sh check
./.ha-test/run.sh start
./.ha-test/run.sh logs
./.ha-test/run.sh stop
./.ha-test/run.sh reset
```

Open `http://localhost:8124` after `start`. The first run creates a separate
local HA onboarding account; it is unrelated to the MediaCenter account.

If Docker is unavailable, start OrbStack/Docker Desktop and rerun the command.

`reset` removes only this harness's `.storage` and database files after a
confirmation prompt. It does not touch the integration source or MediaCenter.
