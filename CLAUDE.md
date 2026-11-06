# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

The source for a one-hour follow-along workshop, "How to Build Agentic AI Workflows for Research" (INL Days @ BSU). Attendees take NASA GISTEMP v4 zonal annual temperature anomalies through five stages in Claude Code: 1 Plan, 2 Explore, 3 Graphs, 4 3D, 5 MCP. Setup is Stage 0, so stage numbers match the checkpoint folder names.

There are two audiences with separate CLAUDE.md files:

- **This file**: for maintaining the kit as the presenter or author.
- **`attendee-kit/CLAUDE.md`**: ships to attendees and governs the Claude sessions they run inside the kit (save to `outputs/`, never touch `data/`, don't read `checkpoints/` unless asked, label °C and the 1951-1980 baseline, cite "Data: NASA GISS GISTEMP v4."). If you change it, you change the workshop's behavior, and the prompt-test results in `BUILD_NOTES.md` may no longer hold.

## Layout

- `attendee-kit/`: everything that goes to attendees. It is zipped into `dist/attendee-kit.zip`, which is committed, so rebuild it after any kit change.
  - `prompts.md`: the prompts for every stage in order, each with a "Stuck?" prompt that copies a checkpoint into `outputs/`.
  - `checkpoints/stageN_*/`: the reference answer key. Each holds one script plus its `outputs/`. The outputs are **cumulative** (stage N contains everything from stages 2 to N), so copying one folder catches an attendee up.
  - `mcp/sqlite_server.py`: a bundled FastMCP server (official `mcp` SDK) with the tools `list_tables`, `describe_table` and `read_query`. It opens the DB with SQLite `?mode=ro` through `Path.as_uri()` so it is read-only and handles Windows paths and spaces. Writes must fail; the test checks this.
  - `verify_setup.py`: stdlib-only setup check. It prints the exact `claude mcp add gistemp -- <venv python> mcp/sqlite_server.py outputs/data.db` line for the attendee's machine.
  - `data/ZonAnn.Ts+dSST.csv`: the raw NASA file. It must stay byte-identical (SHA-256 `fc6f526e…2cec3`), and `data/` may contain only it and `README.md`. The packaging script enforces both.
- `presenter/SLIDES.md`: Marp slide deck with the INL brand palette.
- `tools/`: packaging and end-to-end test scripts.
- `BUILD_NOTES.md` (gitignored): design decisions, verified versions and URLs, prompt test results, stage timings and open issues. Read "Decisions to review" before you change how the kit works.

## Commands

From the repo root:

```
tools/package_kit.sh                 # build dist/attendee-kit.zip (strips outputs/, .venv, .claude, caches; checks the data checksum)
tools/test_kit.sh                    # unzip into a temp dir, uv sync --locked, run the full pipeline, 15 checks
tools/test_kit.sh /path/to/python    # same, but skip uv and use this interpreter
UV_OFFLINE=1 tools/test_kit.sh       # uv sync --offline (no network)
```

`test_kit.sh` tests the **zip**, not the working tree, so run `package_kit.sh` first. It does not call Claude. Prompt behavior was tested separately with headless `claude -p` runs, which are recorded in `BUILD_NOTES.md`.

To regenerate the reference outputs, run these from inside `attendee-kit/`. The scripts use paths relative to the current directory: `data/…` and `outputs/…` by default, overridable with `--out`.

```
uv sync
uv run python checkpoints/stage2_explore/explore.py
uv run python checkpoints/stage3_graphs/make_figures.py
uv run python checkpoints/stage4_3d/make_3d.py --stl
uv run python checkpoints/stage5_mcp/build_db.py
uv run python verify_setup.py
```

These write to `attendee-kit/outputs/`, which must be empty in the shipped kit. `package_kit.sh` strips it anyway. To refresh a checkpoint, copy the new outputs into every `checkpoints/stageN_*/outputs/` from that stage onward, because the outputs are cumulative.

## Invariants the tests depend on

- Tidy data has **8 non-overlapping bands** (90S-64S … 64N-90N), 146 years (1880-2025), and **1168 rows**. The raw file's 15 columns overlap. Choosing these 8 is the Stage 2 lesson, and attendees get a nudge prompt when Claude keeps all 14.
- The area-weighted mean of the 8 bands reproduces `Glob` (mean |diff| < 0.03 °C).
- The DB table is `anomalies(year INTEGER, band TEXT, lat_min REAL, lat_max REAL, anomaly REAL)`. The example answers in `checkpoints/stage5_mcp/README.md` (for example, Arctic +1.85 °C) come from it.
- The 3D HTML embeds plotly.js (`include_plotlyjs=True`, no external `<script src>`) so it works offline. The STL is a binary file written with numpy only (`save_binary_stl`) and must be watertight.
- No new dependencies: the kit has to work offline at the venue, and the attendee prompts tell Claude not to install packages. Dependencies in `attendee-kit/pyproject.toml` are loose minimums for Python 3.10 and later, and `uv.lock` pins the versions. Rerun `uv lock` if you change them.
- Missing values are `***` in GISTEMP. This copy has none, but scripts must still handle them and report "none found".

## Known gaps

- `BUILD_NOTES.md` still mentions files that were removed: `START_HERE.md`, `PREWORK.md`, `SLIDES_OUTLINE.md`, `CONTINGENCY.md`, `FACILITATOR_SCRIPT.md`, `PREWORK_EMAIL.md`, and `package_kit.ps1`. The attendee setup guide is now `attendee-kit/README.md`. `presenter/PREFLIGHT_CHECKLIST.md` and `BUILD_NOTES.md` exist locally but are gitignored, so don't link them from tracked files.
- Everything has been tested on macOS only. Windows and Linux are untested.
