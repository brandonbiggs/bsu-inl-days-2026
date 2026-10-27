#!/usr/bin/env bash
# Zip attendee-kit/ into dist/attendee-kit.zip, leaving out generated and personal files.
# Usage: tools/package_kit.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
KIT="$ROOT/attendee-kit"
DIST="$ROOT/dist"
STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT

# Copy, then clean, so the zip never contains anything made during a rehearsal.
cp -R "$KIT" "$STAGE/attendee-kit"
cd "$STAGE/attendee-kit"
find outputs -mindepth 1 ! -name .gitkeep -exec rm -rf {} + 2>/dev/null || true
rm -rf .venv .mcp.json .claude data.db
find . \( -name __pycache__ -o -name .DS_Store -o -name '*.pyc' \) -exec rm -rf {} + 2>/dev/null || true

# Guard: raw data must be untouched and derived files must not be in the starter area.
EXPECTED="fc6f526ef070878018ecad9a96092db6608a11ab090b26b0a26d8f67dec2cec3"
ACTUAL="$(shasum -a 256 data/ZonAnn.Ts+dSST.csv 2>/dev/null || sha256sum data/ZonAnn.Ts+dSST.csv)"
[[ "$ACTUAL" == "$EXPECTED"* ]] || { echo "ERROR: data/ZonAnn.Ts+dSST.csv checksum changed"; exit 1; }
[[ "$(ls data)" == $'README.md\nZonAnn.Ts+dSST.csv' ]] || { echo "ERROR: unexpected files in data/: $(ls data)"; exit 1; }

mkdir -p "$DIST"
rm -f "$DIST/attendee-kit.zip"
cd "$STAGE"
zip -qr -X "$DIST/attendee-kit.zip" attendee-kit
echo "Wrote $DIST/attendee-kit.zip ($(du -h "$DIST/attendee-kit.zip" | cut -f1), $(unzip -l "$DIST/attendee-kit.zip" | tail -1 | awk '{print $2}') files)"
