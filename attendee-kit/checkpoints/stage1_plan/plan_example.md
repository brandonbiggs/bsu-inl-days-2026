# Example plan (Stage 1)

This is a real plan Claude Code produced in plan mode during testing (2026-10-26), after the
"Revise the plan" prompt. **Yours will be different.** Use it to compare, not to copy.

## Reviewer notes: what to notice

- Good: it states assumptions, names every output file, says how missing values are handled,
  and has a verification step after each phase.
- Worth questioning: the Assumptions section keeps all 14 bands in the tidy file, including the overlapping
  aggregates (`Glob`, `NHem`, ...). That is a defensible choice, but it means anything that
  sums or averages across bands double-counts. This is exactly the kind of assumption that is
  cheapest to catch here. In Stage 2 we ask Claude to keep only the 8 non-overlapping bands.

---

# Plan: Explore GISTEMP v4 zonal data → short report with two figures (+3D)

## Context
Workshop analysis of NASA GISTEMP v4 zonal annual anomalies (`data/ZonAnn.Ts+dSST.csv`,
146 rows, 1880-2025, 15 columns, °C vs 1951-1980 baseline). All outputs go to `outputs/`
(currently empty); `data/` is read-only; `checkpoints/` is not used.
**Execution scope on approval: Phase 1 (Explore) only, then stop and report its checks.**

## Assumptions
- The local copy is the authoritative input; no download (may be offline).
- Values are annual means in °C relative to 1951-1980; no re-baselining.
- `***` is the only missing-value marker; parsed as NaN. README says none exist (a grep
  found 0); the script checks and reports anyway.
- Latitudes are signed degrees (south negative, EQU = 0, poles ±90).
- The tidy file keeps all 14 bands (including overlapping ones like `Glob`, `NHem`);
  anything latitude-resolved filters to the 8 non-overlapping bands from `data/README.md`.
- Trends = OLS linear fits in °C/decade; GISTEMP uncertainty is "not reported" in this file.
- Python + pandas + matplotlib + plotly only; no new packages.

## Phase 1: Explore — `outputs/explore.py`
1. Load CSV with `na_values="***"`; check shape, contiguous years, numeric dtypes,
   NaN count per column.
2. Build `outputs/gistemp_tidy.csv` (long format), columns exactly:
   `year, band, lat_min, lat_max, anomaly` (anomaly in °C vs 1951-1980).
   Band→latitude map, e.g. `Glob` −90/90, `NHem` 0/90, `SHem` −90/0, `24N-90N` 24/90,
   `24S-24N` −24/24, `90S-24S` −90/−24, `64N-90N` 64/90 … `90S-64S` −90/−64.
3. Summary table `outputs/summary_table.csv` per band: 1880-1909 mean, 1996-2025 mean,
   change, OLS trend 1880-2025 and 1975-2025 (°C/decade), warmest year + value.
   Units and baseline in headers.
4. Write all check results to `outputs/explore_checks.txt`.

**Verify Phase 1:**
- Raw: 146 rows × 15 columns, years 1880-2025 with no gaps, NaN count (expect 0).
- Tidy: 146 × 14 = 2044 rows; no NaNs; round-trip: pivot tidy back to wide and confirm
  it equals the raw table exactly.
- Lat map: the 8 non-overlapping bands tile −90..90 with no gaps or overlaps.
- Consistency: area-weighted mean of the 8 bands vs `Glob` (README expects mean abs
  diff ≈0.016 °C, max ≈0.10 °C).
- Spot-check: 2024 `Glob` = 1.28 °C in both raw and tidy, and is the warmest `Glob` year.
→ **Stop here and show checks to the user.**

## Phase 2: Figures — `outputs/figures.py` (reads `gistemp_tidy.csv`)
1. `fig1_global_hemispheres.png`: Glob/NHem/SHem time series + 10-yr centred rolling mean,
   zero line = baseline.
2. `fig2_latitude_heatmap.png`: year × 8 bands (south→north), diverging colormap centred
   on 0, colorbar labelled.
Axes/colorbar: "Temperature anomaly (°C, vs 1951-1980)"; captions end
"Data: NASA GISS GISTEMP v4."

**Verify Phase 2:** open both PNGs and inspect labels, caption, legend, colour centring;
confirm heatmap has 8 rows × 146 columns and the 2024 Glob point plots at 1.28.

## Phase 3: 3D — `outputs/surface3d.py`
1. `outputs/surface3d.html`: plotly surface, x = year, y = band midpoint latitude
   (8 non-overlapping bands only), z = anomaly; diverging colours centred on 0; axis titles
   with units/baseline; source note in title/annotation.

**Verify Phase 3:** surface grid shape is 8 × 146; z min/max equal the tidy file's min/max
for those 8 bands; open the HTML and check orientation (Arctic at +90 shows the strongest
recent warming).

## Phase 4: Report — `outputs/report.md`
About 1 page: data source and citation (from README), assumptions, missing-data handling,
key numbers from `summary_table.csv`, both figures with captions, link to the 3D HTML,
limitations ("not reported" for anything not in the data), checks from each phase.

**Verify Phase 4:** every number in the report is traced to `summary_table.csv` or
`explore_checks.txt` (re-read and compare); all linked files exist; every figure caption
cites the source and every value states units and baseline.
