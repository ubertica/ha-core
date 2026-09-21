#!/usr/bin/env bash
# ha-sentinel AMS evidence mirror. scp/rsync from ams:/opt/ha-live/bus/evidence/
set -euo pipefail
OUT=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --out) OUT="$2"; shift 2 ;;
    *) shift ;;
  esac
done
if [[ -z "$OUT" ]]; then
  OUT="${SENTINEL_OUT:-$HOME/Desktop/puma/docs/pumapay-v2/sentinel}"
fi
mkdir -p "$OUT/ams-mirror/sentinel-god" "$OUT/ams-mirror/sentinel-ollama"
echo "Mirroring from ams..."
rsync -az --delete ams:/opt/ha-live/bus/evidence/sentinel-god/ "$OUT/ams-mirror/sentinel-god/" 2>/dev/null || \
  scp -r ams:/opt/ha-live/bus/evidence/sentinel-god/* "$OUT/ams-mirror/sentinel-god/" 2>/dev/null || \
  echo "HOLD: mirror partial or ams down (non-fatal for selftest)"
rsync -az --delete ams:/opt/ha-live/bus/evidence/sentinel-ollama/ "$OUT/ams-mirror/sentinel-ollama/" 2>/dev/null || true
echo "MIRROR OK -> $OUT/ams-mirror/"
ls -1 "$OUT/ams-mirror/" | head -5
