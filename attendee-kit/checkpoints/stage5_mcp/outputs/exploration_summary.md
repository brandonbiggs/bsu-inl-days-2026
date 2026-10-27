# Exploration summary: GISTEMP v4 zonal annual anomalies

Source: NASA GISS GISTEMP v4, `data/ZonAnn.Ts+dSST.csv` (raw, unmodified). Units: °C anomaly relative to 1951-1980.

## Checks run

- Shape: 146 years (1880-2025) x 14 region columns.
- Missing values (`***` read as missing): 0 found. No rows dropped or filled.
- Baseline check: mean of Glob over 1951-1980 = 0.000 °C (expected ~0).
- Overlap check: columns overlap. Glob, NHem, SHem, 24N-90N, 24S-24N and 90S-24S are aggregates.
  Kept the 8 non-overlapping bands: 90S-64S, 64S-44S, 44S-24S, 24S-EQU, EQU-24N, 24N-44N, 44N-64N, 64N-90N.
- Derived 24N-44N from 24N-90N, 44N-64N, 64N-90N using area weights (sin φ2 − sin φ1): mean |diff| vs the file's 24N-44N = 0.032 °C, max = 0.201 °C. Used NASA's column.
- Area-weighted mean of the 8 bands vs Glob: mean |diff| = 0.016 °C, max = 0.102 °C.

## Per-band summary (°C)

```
         mean   std   min   max  change_1880-1909_to_1996-2025
90S-64S -0.05  0.77 -2.59  1.56                           0.49
64S-44S -0.04  0.29 -0.54  0.55                           0.52
44S-24S  0.06  0.35 -0.44  0.97                           0.82
24S-EQU  0.10  0.37 -0.58  1.16                           0.78
EQU-24N  0.08  0.37 -0.69  1.22                           0.80
24N-44N  0.07  0.47 -0.63  1.64                           1.17
44N-64N  0.16  0.64 -0.80  1.95                           1.60
64N-90N  0.32  1.04 -1.73  3.24                           2.65
```

## Oddities flagged

- 90S-64S (Antarctic) is much noisier before 1950 (std 0.82 vs 0.55 °C after). Few stations existed there then, so treat early Antarctic values with caution.
- 64N-90N (Arctic) has warmed the most: 2.65 °C between 1880-1909 and 1996-2025.
- Warmest years (Glob): 2024 (1.28), 2025 (1.18), 2023 (1.17), 2016 (1.01), 2020 (1.01).
- Latest year 2025 may be revised in later NASA releases.

## Files written

- `gistemp_8band_wide.csv`: Year + 8 non-overlapping bands (south to north).
- `gistemp_tidy.csv`: long format, columns year, band, lat_min, lat_max, anomaly (south latitudes negative).
