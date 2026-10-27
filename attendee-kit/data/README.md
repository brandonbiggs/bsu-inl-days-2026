# Data: NASA GISTEMP v4 zonal annual temperature anomalies

`ZonAnn.Ts+dSST.csv` is the raw file exactly as NASA publishes it. **Do not edit it.** Save anything you derive to `outputs/`.

## Source

| | |
|---|---|
| Dataset | GISS Surface Temperature Analysis (GISTEMP), version 4: zonal annual means, land + ocean (`Ts+dSST`) |
| URL | https://data.giss.nasa.gov/gistemp/tabledata_v4/ZonAnn.Ts+dSST.csv |
| Landing page | https://data.giss.nasa.gov/gistemp/ |
| Copy in this kit | Obtained 2026-10-08 (file timestamp). Years 1880-2025, 146 rows. SHA-256 `fc6f526ef070878018ecad9a96092db6608a11ab090b26b0a26d8f67dec2cec3` |
| License | NASA data are public domain in the US (not copyrighted). NASA asks you to credit the source. |

You can download the file from the URL above, or use the copy in this kit. NASA updates the file every month, so a fresh download may have slightly different recent values or an extra year.

**Suggested citation:** GISTEMP Team, 2026: GISS Surface Temperature Analysis (GISTEMP), version 4. NASA Goddard Institute for Space Studies. Dataset accessed 2026-10-08 at https://data.giss.nasa.gov/gistemp/. Also cite Lenssen, N., et al. (2024), *JGR Atmospheres*, doi:10.1029/2023JD040179.

## What the numbers mean

- Each value is an **annual mean temperature anomaly in degrees Celsius**, relative to the **1951-1980 baseline**. For example, 1.28 means 1.28 °C warmer than the 1951-1980 average for that region.
- Values are rounded to 0.01 °C.
- Missing values are written as `***` in GISTEMP files. **This copy has none**: every band has a value for every year from 1880 to 2025. Your analysis should still check for missing values and report what it found.

## Columns (15)

| Column | Meaning | Latitude range |
|---|---|---|
| `Year` | Calendar year | |
| `Glob` | Global mean | 90S-90N |
| `NHem` | Northern Hemisphere | EQU-90N |
| `SHem` | Southern Hemisphere | 90S-EQU |
| `24N-90N` | Northern extratropics | 24N-90N |
| `24S-24N` | Tropics | 24S-24N |
| `90S-24S` | Southern extratropics | 90S-24S |
| `64N-90N` | Arctic | 64N-90N |
| `44N-64N` | Northern mid/high latitudes | 44N-64N |
| `24N-44N` | Northern subtropics/mid latitudes | 24N-44N |
| `EQU-24N` | Northern tropics | 0-24N |
| `24S-EQU` | Southern tropics | 24S-0 |
| `44S-24S` | Southern subtropics/mid latitudes | 44S-24S |
| `64S-44S` | Southern Ocean | 64S-44S |
| `90S-64S` | Antarctic | 90S-64S |

## Overlapping bands (important for the 3D surface)

The columns **overlap**. `Glob`, the hemispheres, and the three wide bands (`24N-90N`, `24S-24N`, `90S-24S`) are each made up of the narrower bands. Only these **8 columns** tile the globe without overlap:

`90S-64S, 64S-44S, 44S-24S, 24S-EQU, EQU-24N, 24N-44N, 44N-64N, 64N-90N`

Use only these 8 for a year-by-latitude heatmap or surface. Otherwise some latitudes are counted twice.

## Area weights and a consistency check

The fraction of Earth's surface between latitudes φ1 and φ2 is (sin φ2 − sin φ1) / 2. As a fraction of one hemisphere it is just sin φ2 − sin φ1:

| Band | Hemisphere fraction |
|---|---|
| 64-90 | 0.1012 |
| 44-64 | 0.2041 |
| 24-44 | 0.2879 |
| 0-24 | 0.4067 |
| 24-90 (sum of the three above) | 0.5933 |

Two checks, both run on this copy:

1. **Rebuild `24N-44N` from the wide band.** 24N-44N ≈ (0.5933 × `24N-90N` − 0.2041 × `44N-64N` − 0.1012 × `64N-90N`) / 0.2879. This matches NASA's `24N-44N` column with a mean difference of 0.03 °C and a worst case of 0.20 °C. The gap comes from 0.01 °C rounding being amplified by dividing by a small area, and NASA may also compute each band independently. Older versions of this file did not include `24N-44N`, and this formula is how you would derive it.
2. **Rebuild `Glob` from the 8 bands.** The area-weighted mean of the 8 non-overlapping bands matches `Glob` within 0.016 °C on average (worst case 0.10 °C).
