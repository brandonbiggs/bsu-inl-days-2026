# Starter kit: How to Build Agentic AI Workflows for Research

An hour follow-along session for research faculty and students. Attendees take one public dataset (NASA GISTEMP v4 zonal temperature anomalies) through five stages in Claude Code: **plan, explore, graph, 3D, MCP**.

[Dataset from nasa.gov](https://data.giss.nasa.gov/gistemp/tabledata_v4/ZonAnn.Ts+dSST.csv)
## What's here

| Path | For | Contents |
|---|---|---|
| `attendee-kit/` | Attendees (zipped) | `START_HERE.md`, `PREWORK.md`, `prompts.md`, `CLAUDE.md`, `verify_setup.py`, `pyproject.toml` + `uv.lock`, raw `data/`, empty `outputs/`, `mcp/sqlite_server.py`, `checkpoints/` |
| `presenter/` | You | `SLIDES_OUTLINE.md`, `CONTINGENCY.md`, `PREFLIGHT_CHECKLIST.md`|
| `tools/` | You | `package_kit.sh` / `package_kit.ps1` (build the zip), `test_kit.sh` (prove the zip works) |
| `dist/attendee-kit.zip` | Attendees | The built kit |
| `BUILD_NOTES.md` | You | Decisions, verified versions and URLs, prompt test results, timings, open issues |

## Stage and folder names

The same numbering is used everywhere:

| Stage | Name | Minutes | Checkpoint folder |
|---|---|---|---|
| 0 | Setup check | 5 | (none) |
| 1 | Plan | 7 | `checkpoints/stage1_plan/` |
| 2 | Explore | 7 | `checkpoints/stage2_explore/` |
| 3 | Graphs | 7 | `checkpoints/stage3_graphs/` |
| 4 | 3D | 8 | `checkpoints/stage4_3d/` |
| 5 | MCP | 8 | `checkpoints/stage5_mcp/` |
| | Wrap-up | 3 | |

The brief numbered Stage 1 as "Setup check". The kit numbers setup as Stage 0, so stage numbers line up with the checkpoint folder names.

## Quick commands

```
tools/package_kit.sh                    # build dist/attendee-kit.zip
tools/test_kit.sh [path/to/python]      # unzip into a temp dir, uv sync, run the full reference pipeline
```

## Workflow for the presenter

1. Read `BUILD_NOTES.md` > "Decisions to review".
2. Edit `presenter/PREWORK_EMAIL.md` and send it with the zip, 3-5 days ahead.
3. Rehearse with `presenter/FACILITATOR_SCRIPT.md`; work through `presenter/PREFLIGHT_CHECKLIST.md`.
4. Keep `presenter/CONTINGENCY.md` open during the session.
