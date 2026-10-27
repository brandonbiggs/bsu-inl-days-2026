#!/usr/bin/env bash
# Prove the kit works: unzip dist/attendee-kit.zip into a clean temp dir, then
#   1. run verify_setup.py
#   2. run the reference pipeline (checkpoint scripts) end to end
#   3. check outputs against the shipped checkpoints (numbers, files, offline HTML, STL)
#   4. start the bundled MCP server and query it over the MCP protocol (read-only check)
# Does not call Claude (no network or account needed). Prompt tests are recorded in BUILD_NOTES.md.
#
# Usage: tools/test_kit.sh [python]      default: run "uv sync" in the unzipped kit and use its .venv
#                                        e.g. tools/test_kit.sh /tmp/aks-venv/bin/python to skip uv
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ZIP="$ROOT/dist/attendee-kit.zip"
[[ -f "$ZIP" ]] || { echo "No $ZIP. Run tools/package_kit.sh first."; exit 1; }
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
export MPLCONFIGDIR="$TMP/mpl" MPLBACKEND=Agg

pass=0; fail=0
ok()  { echo "PASS  $1"; pass=$((pass+1)); }
bad() { echo "FAIL  $1"; fail=$((fail+1)); }
step() { if eval "$2" >"$TMP/log" 2>&1; then ok "$1"; else bad "$1"; sed 's/^/      /' "$TMP/log" | tail -15; fi; }

cd "$TMP" && unzip -q "$ZIP" && cd attendee-kit
if [[ $# -ge 1 ]]; then
  PY="$(command -v "$1")"
else
  uv sync --locked ${UV_OFFLINE:+--offline} || { echo "uv sync failed"; exit 1; }
  PY="$PWD/.venv/bin/python"
fi
echo "Testing in $TMP/attendee-kit with $PY ($("$PY" --version))"

# Kit contents
step "starter outputs/ is empty"        '[ "$(ls -A outputs)" = ".gitkeep" ]'
step "pyproject.toml and uv.lock shipped" 'test -s pyproject.toml -a -s uv.lock'
step "data/ holds only raw CSV + README" '[ "$(ls data | tr "\n" " ")" = "README.md ZonAnn.Ts+dSST.csv " ]'
step "no derived files outside checkpoints" '! find . \( -path ./checkpoints -o -path ./.venv \) -prune -o \( -name "*.db" -o -name "*tidy*" -o -name "*.html" -o -name "*.stl" \) -print | grep -q .'
step "verify_setup.py all PASS (Claude check may be skipped)" \
     '"$PY" verify_setup.py | tee "$TMP/verify.txt"; ! grep -E "^FAIL" "$TMP/verify.txt" | grep -v "Claude Code installed" | grep -q .'

# Reference pipeline
step "stage 2 explore.py"       '"$PY" checkpoints/stage2_explore/explore.py'
step "stage 3 make_figures.py"  '"$PY" checkpoints/stage3_graphs/make_figures.py'
step "stage 4 make_3d.py --stl" '"$PY" checkpoints/stage4_3d/make_3d.py --stl'
step "stage 5 build_db.py"      '"$PY" checkpoints/stage5_mcp/build_db.py'

# Outputs match checkpoints
for f in gistemp_tidy.csv gistemp_8band_wide.csv; do
  step "$f identical to checkpoint" "cmp -s outputs/$f checkpoints/stage5_mcp/outputs/$f"
done
step "figures exist (PNG + SVG)" 'for f in global_anomaly lat_year_heatmap; do test -s outputs/$f.png -a -s outputs/$f.svg || exit 1; done'

cat > "$TMP/checks.py" <<'EOF'
import sqlite3, sys, re, struct, collections
import numpy as np
db = sqlite3.connect("outputs/data.db")
n, nb, y0, y1 = db.execute("SELECT COUNT(*), COUNT(DISTINCT band), MIN(year), MAX(year) FROM anomalies").fetchone()
assert (n, nb, y0) == (1168, 8, 1880), (n, nb, y0, y1)
# Area-weighted 8-band mean reproduces Glob (sanity check on the bands and lat bounds)
import csv
glob = {int(r["Year"]): float(r["Glob"]) for r in csv.DictReader(open("data/ZonAnn.Ts+dSST.csv"))}
w = {}
for year, a, lo, hi in db.execute("SELECT year, anomaly, lat_min, lat_max FROM anomalies"):
    w[year] = w.get(year, 0) + a * (np.sin(np.radians(hi)) - np.sin(np.radians(lo))) / 2
d = np.array([abs(w[y] - glob[y]) for y in w])
assert d.mean() < 0.03 and d.max() < 0.15, (d.mean(), d.max())
print(f"8-band area-weighted mean vs Glob: mean {d.mean():.3f}, max {d.max():.3f} C")
# HTML embeds plotly.js (no external <script src>)
html = open("outputs/anomaly_surface_3d.html", encoding="utf-8").read()
assert not re.search(r"<script[^>]+src=", html), "HTML loads an external script"
assert len(html) > 1_000_000, "plotly.js not embedded"
# STL is binary, sized correctly, and watertight
b = open("outputs/anomaly_surface.stl", "rb").read()
ntri = struct.unpack("<I", b[80:84])[0]
assert len(b) == 84 + 50 * ntri
rec = np.frombuffer(b[84:], dtype=[("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
edges = collections.Counter()
for t in np.round(rec["v"], 4):
    t = [tuple(p) for p in t]
    for e in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])):
        edges[e] += 1
assert all(c == 1 and edges.get((e[1], e[0])) == 1 for e, c in edges.items()), "STL not watertight"
print(f"STL: {ntri} triangles, watertight")
EOF
step "numbers, offline HTML, watertight STL" '"$PY" "$TMP/checks.py"'

cat > "$TMP/mcp_check.py" <<'EOF'
import asyncio, sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
async def main():
    p = StdioServerParameters(command=sys.executable, args=["mcp/sqlite_server.py", "outputs/data.db"])
    async with stdio_client(p) as (r, w), ClientSession(r, w) as s:
        await s.initialize()
        tools = sorted(t.name for t in (await s.list_tools()).tools)
        assert tools == ["describe_table", "list_tables", "read_query"], tools
        res = await s.call_tool("read_query", {"sql": "SELECT (year/10)*10 d, AVG(anomaly) a FROM anomalies WHERE band='64N-90N' GROUP BY d ORDER BY a DESC LIMIT 1"})
        assert not res.isError and "2020" in res.content[0].text, res
        res = await s.call_tool("read_query", {"sql": "DELETE FROM anomalies"})
        assert res.isError and "readonly" in res.content[0].text, res
        print("MCP tools:", tools, "| query ok | delete blocked (read-only)")
asyncio.run(main())
EOF
step "MCP server: tools, query, read-only" '"$PY" "$TMP/mcp_check.py"'
step "raw data unchanged after pipeline" '[ "$( (shasum -a 256 2>/dev/null || sha256sum) < data/ZonAnn.Ts+dSST.csv | cut -c1-64)" = fc6f526ef070878018ecad9a96092db6608a11ab090b26b0a26d8f67dec2cec3 ]'

echo "----"
echo "$pass passed, $fail failed"
[[ $fail -eq 0 ]]
