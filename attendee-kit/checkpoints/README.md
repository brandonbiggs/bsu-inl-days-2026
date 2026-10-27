# Checkpoints

Reference results for anyone who falls behind. Each checkpoint's `outputs/` folder holds everything up to and including that stage, so copying one folder catches you up completely.

| Folder | Stage | What's in `outputs/` | Script that made it |
|---|---|---|---|
| `stage1_plan/` | 1 Plan | (no outputs) `plan_example.md` is a real example plan | |
| `stage2_explore/` | 2 Explore | `gistemp_tidy.csv` (1168 rows, 8 bands), `gistemp_8band_wide.csv`, `exploration_summary.md` | `explore.py` |
| `stage3_graphs/` | 3 Graphs | above + `global_anomaly.png/.svg`, `lat_year_heatmap.png/.svg` | `make_figures.py` |
| `stage4_3d/` | 4 3D | above + `anomaly_surface_3d.html` (offline), `anomaly_surface.stl` (stretch) | `make_3d.py --stl` |
| `stage5_mcp/` | 5 MCP | above + `data.db` | `build_db.py`; see `README.md` there |

**To rejoin**, ask Claude, for example:

```
Copy everything in checkpoints/stage3_graphs/outputs/ into outputs/, then list the figures.
```

Or copy the files yourself in your file browser.

**To regenerate everything** (from the attendee-kit folder):

```
uv run python checkpoints/stage2_explore/explore.py
uv run python checkpoints/stage3_graphs/make_figures.py
uv run python checkpoints/stage4_3d/make_3d.py --stl
uv run python checkpoints/stage5_mcp/build_db.py
```

Your own Claude-made files will have different names and styles. That is expected: compare the numbers, not the filenames.
