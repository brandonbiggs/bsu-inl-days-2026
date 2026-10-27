"""Stage 2 reference: load GISTEMP zonal annual anomalies, check them, and write tidy files.

Run from the attendee-kit folder:  uv run python checkpoints/stage2_explore/explore.py
Writes to outputs/ (or --out DIR): gistemp_8band_wide.csv, gistemp_tidy.csv, exploration_summary.md
"""
import argparse
import math
from pathlib import Path

import pandas as pd

RAW = Path("data/ZonAnn.Ts+dSST.csv")

# The 8 non-overlapping bands, south to north: (column, lat_min, lat_max)
BANDS = [
    ("90S-64S", -90, -64),
    ("64S-44S", -64, -44),
    ("44S-24S", -44, -24),
    ("24S-EQU", -24, 0),
    ("EQU-24N", 0, 24),
    ("24N-44N", 24, 44),
    ("44N-64N", 44, 64),
    ("64N-90N", 64, 90),
]


def area(lat1, lat2):
    """Fraction of one hemisphere between two latitudes (degrees)."""
    return math.sin(math.radians(lat2)) - math.sin(math.radians(lat1))


def main(out):
    out.mkdir(parents=True, exist_ok=True)
    raw = pd.read_csv(RAW, na_values=["***", "****", "*****"])
    missing = raw.isna().sum()
    n_missing = int(missing.sum())

    # Check 1: rebuild 24N-44N from the wide 24N-90N band using area weights
    derived = (area(24, 90) * raw["24N-90N"] - area(44, 64) * raw["44N-64N"]
               - area(64, 90) * raw["64N-90N"]) / area(24, 44)
    d_diff = (derived - raw["24N-44N"]).abs()

    # Check 2: area-weighted mean of the 8 bands should reproduce Glob
    weights = {c: area(a, b) / 2 for c, a, b in BANDS}
    glob_rebuilt = sum(raw[c] * w for c, w in weights.items())
    g_diff = (glob_rebuilt - raw["Glob"]).abs()

    cols = [c for c, _, _ in BANDS]
    wide = raw[["Year"] + cols]
    wide.to_csv(out / "gistemp_8band_wide.csv", index=False)

    tidy = wide.melt(id_vars="Year", var_name="band", value_name="anomaly")
    meta = pd.DataFrame(BANDS, columns=["band", "lat_min", "lat_max"])
    tidy = (tidy.merge(meta, on="band").rename(columns={"Year": "year"})
            [["year", "band", "lat_min", "lat_max", "anomaly"]]
            .sort_values(["year", "lat_min"]))
    tidy.to_csv(out / "gistemp_tidy.csv", index=False)

    # Summaries for the report
    stats = wide[cols].agg(["mean", "std", "min", "max"]).T.round(2)
    early = wide[wide.Year.between(1880, 1909)][cols].mean()
    late = wide[wide.Year.between(1996, 2025)][cols].mean()
    stats["change_1880-1909_to_1996-2025"] = (late - early).round(2)
    warmest = raw.nlargest(5, "Glob")[["Year", "Glob"]]
    base = raw[raw.Year.between(1951, 1980)]["Glob"].mean()
    sd_ant = (wide[wide.Year < 1950]["90S-64S"].std(), wide[wide.Year >= 1950]["90S-64S"].std())

    lines = [
        "# Exploration summary: GISTEMP v4 zonal annual anomalies",
        "",
        f"Source: NASA GISS GISTEMP v4, `{RAW.as_posix()}` (raw, unmodified). "
        "Units: °C anomaly relative to 1951-1980.",
        "",
        "## Checks run",
        "",
        f"- Shape: {raw.shape[0]} years ({raw.Year.min()}-{raw.Year.max()}) x {raw.shape[1] - 1} region columns.",
        f"- Missing values (`***` read as missing): {n_missing} found."
        + (" No rows dropped or filled." if n_missing == 0 else
           " Left as missing (NaN); not filled or interpolated."),
        f"- Baseline check: mean of Glob over 1951-1980 = {base:.3f} °C (expected ~0).",
        "- Overlap check: columns overlap. Glob, NHem, SHem, 24N-90N, 24S-24N and 90S-24S are aggregates.",
        "  Kept the 8 non-overlapping bands: " + ", ".join(cols) + ".",
        f"- Derived 24N-44N from 24N-90N, 44N-64N, 64N-90N using area weights (sin φ2 − sin φ1): "
        f"mean |diff| vs the file's 24N-44N = {d_diff.mean():.3f} °C, max = {d_diff.max():.3f} °C. Used NASA's column.",
        f"- Area-weighted mean of the 8 bands vs Glob: mean |diff| = {g_diff.mean():.3f} °C, max = {g_diff.max():.3f} °C.",
        "",
        "## Per-band summary (°C)",
        "",
        stats.to_markdown() if _has_tabulate() else "```\n" + stats.to_string() + "\n```",
        "",
        "## Oddities flagged",
        "",
        f"- 90S-64S (Antarctic) is much noisier before 1950 (std {sd_ant[0]:.2f} vs {sd_ant[1]:.2f} °C after). "
        "Few stations existed there then, so treat early Antarctic values with caution.",
        f"- 64N-90N (Arctic) has warmed the most: {stats.loc['64N-90N', 'change_1880-1909_to_1996-2025']} °C "
        "between 1880-1909 and 1996-2025.",
        "- Warmest years (Glob): " + ", ".join(f"{int(y)} ({v:.2f})" for y, v in warmest.values) + ".",
        f"- Latest year {raw.Year.max()} may be revised in later NASA releases.",
        "",
        "## Files written",
        "",
        "- `gistemp_8band_wide.csv`: Year + 8 non-overlapping bands (south to north).",
        "- `gistemp_tidy.csv`: long format, columns year, band, lat_min, lat_max, anomaly (south latitudes negative).",
    ]
    (out / "exploration_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def _has_tabulate():
    try:
        import tabulate  # noqa: F401
        return True
    except ImportError:
        return False


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=Path, default=Path("outputs"))
    main(p.parse_args().out)
