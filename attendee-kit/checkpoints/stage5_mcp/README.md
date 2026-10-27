# Stage 5 checkpoint: SQLite over MCP

## Catch up

1. Copy everything in `checkpoints/stage5_mcp/outputs/` into `outputs/`. This includes `outputs/data.db`.
2. Connect the server. Exit Claude (`/exit`) first, then run this from the attendee-kit folder:

   ```
   claude mcp add gistemp -- /path/to/attendee-kit/.venv/bin/python mcp/sqlite_server.py outputs/data.db
   ```

   Use the exact command printed by `uv run python verify_setup.py`. It points at the kit's `.venv` Python (on Windows, `.venv\Scripts\python.exe`). If the path has spaces, keep the quotes it prints.
3. Run `claude --continue`, then type `/mcp`. You should see `gistemp` with status **connected**. In a terminal, `claude mcp list` should show `gistemp: ... - ✔ Connected`.

`mcp_config_example.json` shows the same server as a project-scope `.mcp.json`, for presenters who want to share it. A project-scope server asks for approval the first time you start `claude`. The default local scope does not ask.

## If `/mcp` shows "failed"

| Check | Fix |
|---|---|
| Wrong Python (the one without `mcp` installed) | `claude mcp remove gistemp`, then add again using the Python path from `uv run python verify_setup.py` |
| Started Claude from a different folder | `cd` into the attendee-kit folder; the paths are relative to it |
| `outputs/data.db` missing | Do Step 1 of Stage 5, or copy the checkpoint |
| Still failing | Run `uv run python mcp/sqlite_server.py outputs/data.db` directly. It should wait silently (press Ctrl+C to stop). Any error it prints is the cause. |

## Files

- `build_db.py`: reference script that builds `outputs/data.db` from `outputs/gistemp_tidy.csv` (standard library only).
- `outputs/data.db`: table `anomalies(year INTEGER, band TEXT, lat_min REAL, lat_max REAL, anomaly REAL)`, 1168 rows (146 years x 8 bands).
- `mcp_config_example.json`: project-scope config example.

## Example questions and answers

These came from real test runs. Your wording and approach will differ. The numbers should not.

**1. Which decade had the largest warming at 64N-90N? Show the SQL.**

```sql
SELECT (year/10)*10 AS decade, COUNT(*) AS n_years, ROUND(AVG(anomaly), 3) AS mean_anomaly
FROM anomalies WHERE band = '64N-90N'
GROUP BY decade ORDER BY decade;
```

The answer depends on how you read "warming", and a good answer says so.
- The 2020s (2020-2025, only 6 years) have the highest mean, 2.60 °C.
- The biggest jump between decade means is from the 2000s (1.42) to the 2010s (2.29), +0.87 °C.

**2. For each band, 1951-1980 average vs 1996-2025 average. Which band warmed most and least?**

```sql
SELECT band,
  ROUND(AVG(CASE WHEN year BETWEEN 1951 AND 1980 THEN anomaly END), 2) AS base,
  ROUND(AVG(CASE WHEN year BETWEEN 1996 AND 2025 THEN anomaly END), 2) AS recent,
  ROUND(AVG(CASE WHEN year BETWEEN 1996 AND 2025 THEN anomaly END)
      - AVG(CASE WHEN year BETWEEN 1951 AND 1980 THEN anomaly END), 2) AS change
FROM anomalies GROUP BY band ORDER BY change DESC;
```

- Most warming: 64N-90N (Arctic), +1.85 °C.
- Least warming: 64S-44S (Southern Ocean), +0.28 °C.
- The baseline column is about 0 for every band, which is itself a good check, because anomalies are defined relative to 1951-1980.

**3. In which year did each band reach its record high?**

| Band | Record year | Anomaly (°C) |
|---|---|---|
| 64N-90N | 2016 | 3.24 |
| 44N-64N, 24N-44N, EQU-24N, 24S-EQU | 2024 | 1.95, 1.64, 1.22, 1.16 |
| 44S-24S, 64S-44S, 90S-64S | 2025 | 0.97, 0.55, 1.56 |

**Bonus: try to delete all rows.** This fails with `attempt to write a readonly database`, because the server opens the file with SQLite's read-only mode.
