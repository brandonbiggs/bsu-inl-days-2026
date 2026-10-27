"""Check that this computer is ready for the workshop.

Run from this folder:
    uv run python verify_setup.py

Prints PASS/FAIL for each check and a hint for anything that fails.
Uses only the Python standard library for the checks themselves.
"""
import csv
import importlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "data" / "ZonAnn.Ts+dSST.csv"
PIP_HINT = "uv sync, then run this check again with: uv run python verify_setup.py"
BANDS = ["90S-64S", "64S-44S", "44S-24S", "24S-EQU", "EQU-24N", "24N-44N", "44N-64N", "64N-90N"]

results = []  # (ok, name, detail, hint)


def check(name, fn, hint):
    try:
        detail = fn()
        results.append((True, name, detail or "", ""))
    except Exception as e:  # noqa: BLE001
        results.append((False, name, str(e) or type(e).__name__, hint))


def python_version():
    v = sys.version_info
    if v < (3, 10):
        raise RuntimeError(f"found {v.major}.{v.minor}, need 3.10 or newer")
    return f"{v.major}.{v.minor}.{v.micro} at {sys.executable}"


def package(mod):
    def fn():
        m = importlib.import_module(mod)
        return getattr(m, "__version__", "") or "installed"
    return fn


def mcp_sdk():
    importlib.import_module("mcp.server.fastmcp")
    from importlib.metadata import version
    return version("mcp")


def data_file():
    if not DATA.exists():
        raise FileNotFoundError(f"missing {DATA.relative_to(HERE)}")
    with open(DATA, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    header, body = rows[0], rows[1:]
    missing = [b for b in ["Year", "Glob"] + BANDS if b not in header]
    if missing:
        raise ValueError(f"unexpected columns, missing {missing}")
    years = [int(r[0]) for r in body]
    return f"{len(body)} rows, years {min(years)}-{max(years)}, {len(header)} columns"


def plotting_works():
    os.environ.setdefault("MPLBACKEND", "Agg")
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import plotly.graph_objects as go
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])
    plt.close(fig)
    go.Figure(go.Surface(z=[[0, 1], [1, 0]])).to_html(include_plotlyjs=True)
    return "matplotlib and plotly can draw"


def outputs_writable():
    out = HERE / "outputs"
    out.mkdir(exist_ok=True)
    probe = out / ".write_test"
    probe.write_text("ok")
    probe.unlink()
    return str(out.relative_to(HERE)) + "/ is writable"


def claude_cli():
    exe = shutil.which("claude")
    if not exe:
        raise FileNotFoundError("'claude' not found on PATH")
    out = subprocess.run([exe, "--version"], capture_output=True, text=True, timeout=30)
    return (out.stdout or out.stderr).strip().splitlines()[0]


check("Python 3.10+", python_version, "Run: uv sync, then uv run python verify_setup.py (uv installs a suitable Python; see PREWORK.md).")
for mod in ["pandas", "numpy", "matplotlib", "plotly"]:
    check(f"package: {mod}", package(mod), f"Run: {PIP_HINT}")
check("package: mcp (for Stage 5)", mcp_sdk, f"Run: {PIP_HINT}")
check("data file parses", data_file, "Re-unzip the kit. The file data/ZonAnn.Ts+dSST.csv must be unchanged.")
check("plots render", plotting_works, f"Reinstall packages: {PIP_HINT}")
check("outputs folder writable", outputs_writable, "Unzip the kit somewhere you own, e.g. Documents, not a read-only or synced folder.")
check("Claude Code installed", claude_cli, "Install Claude Code: https://code.claude.com/docs/en/setup  (then open a NEW terminal)")

width = max(len(n) for _, n, _, _ in results)
print("\nWorkshop setup check\n" + "-" * 60)
for ok, name, detail, hint in results:
    print(f"{'PASS' if ok else 'FAIL'}  {name:<{width}}  {detail}")
    if not ok:
        print(f"      fix: {hint}")
fails = sum(not ok for ok, *_ in results)
print("-" * 60)
if fails:
    print(f"{fails} check(s) FAILED. Fix them using the hints above or PREWORK.md, then run this again.")
    print("Still stuck? Reply to the pre-work email and paste this whole output.")
else:
    print("All checks PASSED. You are ready for the workshop.")
py = f'"{sys.executable}"' if " " in sys.executable else sys.executable
print("\nFor Stage 5, your MCP command is (copy it then):")
print(f"  claude mcp add gistemp -- {py} mcp/sqlite_server.py outputs/data.db")
sys.exit(1 if fails else 0)
