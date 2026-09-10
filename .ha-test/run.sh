#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
COMPOSE="docker compose -f $ROOT/.ha-test/compose.yaml"

case "${1:-}" in
  check)
    docker info >/dev/null
    $COMPOSE run --rm homeassistant python -m homeassistant --script check_config --config /config
    ;;
  start)
    docker info >/dev/null
    $COMPOSE up -d
    echo "Home Assistant test instance: http://localhost:8124"
    ;;
  stop)
    $COMPOSE down
    ;;
  logs)
    $COMPOSE logs -f --tail=100 homeassistant
    ;;
  reset)
    printf '%s' 'Reset local HA test storage? type RESET: '
    read answer
    [ "$answer" = RESET ] || { echo 'Cancelled.'; exit 1; }
    find "$ROOT/.ha-test/config/.storage" -type f -delete 2>/dev/null || true
    find "$ROOT/.ha-test/config" -maxdepth 1 -type f -name 'home-assistant_v2.db*' -delete 2>/dev/null || true
    echo 'Local test storage reset.'
    ;;
  *)
    echo "Usage: $0 {check|start|logs|stop|reset}" >&2
    exit 2
    ;;
esac
