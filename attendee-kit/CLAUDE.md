# Project: Agentic AI workflows for research (workshop folder)

This folder is for a hands-on workshop. We analyze NASA GISTEMP v4 zonal annual
temperature anomalies in five stages: plan, explore, graph, 3D, and query via MCP.

## Files
- `data/ZonAnn.Ts+dSST.csv`: raw NASA data. `data/README.md` describes it.
- `outputs/`: everything we create goes here.
- `checkpoints/`: reference answers for people who fall behind. Do not read,
  copy, or use them unless the user explicitly asks.
- `mcp/sqlite_server.py`: a small read-only database server used in Stage 5.

## Conventions
- Save all outputs (data, figures, scripts, reports) to `outputs/`.
- Never modify, move, or overwrite anything in `data/`.
- Prefer Python with pandas, matplotlib, and plotly. These are already installed
  in `.venv` by uv; do not install new packages without asking. (There may be no internet.)
- Run Python with `uv run python ...` so it uses this folder's `.venv`.
- Write analysis as a script in `outputs/` and run it, so results are reproducible.
- Before analysis, state your assumptions in a short list.

## Research rules
- Report how missing data were handled (GISTEMP marks missing values as `***`),
  even if none were found.
- Values are temperature anomalies in °C relative to the 1951-1980 baseline.
  Label units and baseline on every axis, table, and summary.
- Cite the data source in every figure caption:
  "Data: NASA GISS GISTEMP v4."
- If something is not in the data, say "not reported" rather than guessing.

## Verification habit
- After producing any result, state one check you ran and what it showed
  (for example: row counts, a recomputed value, or a plot you inspected).
