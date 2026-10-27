"""Stage 3 reference: global anomaly line chart and latitude-by-year heatmap.

Run from the attendee-kit folder:  uv run python checkpoints/stage3_graphs/make_figures.py
Reads outputs/gistemp_tidy.csv (from Stage 2) and data/ZonAnn.Ts+dSST.csv.
Writes global_anomaly.png/.svg and lat_year_heatmap.png/.svg to outputs/ (or --out DIR).
"""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.colors import TwoSlopeNorm  # noqa: E402

SOURCE = "Data: NASA GISS GISTEMP v4 (zonal annual means), anomaly vs 1951-1980."
SMOOTH = 10  # years, centered rolling mean

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "svg.fonttype": "none",
})


def main(tidy_path, out):
    out.mkdir(parents=True, exist_ok=True)
    raw = pd.read_csv("data/ZonAnn.Ts+dSST.csv", na_values=["***", "****", "*****"])
    tidy = pd.read_csv(tidy_path)

    # 1) Global line chart, Okabe-Ito colors (colorblind-safe)
    g = raw[["Year", "Glob"]].dropna()
    smooth = g["Glob"].rolling(SMOOTH, center=True, min_periods=SMOOTH).mean()
    fig, ax = plt.subplots(figsize=(7, 3.6))
    ax.axhline(0, color="0.6", lw=0.8)
    ax.plot(g.Year, g.Glob, color="#999999", lw=1, marker="o", ms=2, label="Annual mean")
    ax.plot(g.Year, smooth, color="#D55E00", lw=2.2, label=f"{SMOOTH}-year centered mean")
    ax.set_xlabel("Year")
    ax.set_ylabel("Temperature anomaly (°C)")
    ax.set_title("Global surface temperature anomaly, 1880-%d" % g.Year.max())
    ax.legend(frameon=False, loc="upper left")
    fig.text(0.01, 0.01, SOURCE, fontsize=7, color="0.35")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    for ext in ("png", "svg"):
        fig.savefig(out / f"global_anomaly.{ext}", dpi=200)
    plt.close(fig)

    # 2) Heatmap: rows = bands (south at bottom), columns = years, diverging map centered at 0
    grid = tidy.pivot_table(index=["lat_min", "band"], columns="year", values="anomaly").sort_index()
    lim = np.nanmax(np.abs(grid.values))
    fig, ax = plt.subplots(figsize=(8, 3.6))
    years = grid.columns.to_numpy()
    x_edges = np.append(years - 0.5, years[-1] + 0.5)
    im = ax.pcolormesh(x_edges, np.arange(len(grid) + 1), grid.values,
                       cmap="RdBu_r", norm=TwoSlopeNorm(vcenter=0, vmin=-lim, vmax=lim))
    ax.set_yticks(np.arange(len(grid)) + 0.5)
    ax.set_yticklabels([b for _, b in grid.index])
    ax.set_xlabel("Year")
    ax.set_ylabel("Latitude band")
    ax.set_title("Temperature anomaly by latitude band")
    cb = fig.colorbar(im, ax=ax, pad=0.02)
    cb.set_label("Anomaly (°C)")
    fig.text(0.01, 0.01, SOURCE + " 8 non-overlapping bands.", fontsize=7, color="0.35")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    for ext in ("png", "svg"):
        fig.savefig(out / f"lat_year_heatmap.{ext}", dpi=200)
    plt.close(fig)
    print("Wrote figures to", out)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--tidy", type=Path, default=Path("outputs/gistemp_tidy.csv"))
    p.add_argument("--out", type=Path, default=Path("outputs"))
    a = p.parse_args()
    main(a.tidy, a.out)
