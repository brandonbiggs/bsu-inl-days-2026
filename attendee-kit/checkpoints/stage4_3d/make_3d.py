"""Stage 4 reference: interactive 3D surface (year x latitude x anomaly), plus optional STL.

Run from the attendee-kit folder:  uv run python checkpoints/stage4_3d/make_3d.py [--stl]
Reads outputs/gistemp_tidy.csv. Writes outputs/anomaly_surface_3d.html (plotly.js embedded,
works offline) and, with --stl, outputs/anomaly_surface.stl.
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go


def load_grid(tidy_path):
    tidy = pd.read_csv(tidy_path)
    tidy["lat_mid"] = (tidy.lat_min + tidy.lat_max) / 2
    grid = tidy.pivot_table(index="lat_mid", columns="year", values="anomaly").sort_index()
    return grid.columns.to_numpy(), grid.index.to_numpy(), grid.to_numpy()


def write_html(years, lats, z, path):
    lim = float(np.nanmax(np.abs(z)))
    fig = go.Figure(go.Surface(
        x=years, y=lats, z=z, colorscale="RdBu_r", cmin=-lim, cmax=lim, cmid=0,
        colorbar=dict(title="°C"),
        hovertemplate="Year %{x}<br>Band center %{y}°<br>Anomaly %{z:.2f} °C<extra></extra>",
    ))
    fig.update_layout(
        title="GISTEMP v4 temperature anomaly by year and latitude (vs 1951-1980)<br>"
              "<sup>Data: NASA GISS GISTEMP v4 zonal annual means, 8 non-overlapping bands</sup>",
        scene=dict(xaxis_title="Year", yaxis_title="Latitude (band center, °)",
                   zaxis_title="Anomaly (°C)", aspectratio=dict(x=2.2, y=1, z=0.6)),
        margin=dict(l=0, r=0, t=60, b=0),
    )
    # include_plotlyjs=True embeds plotly.js (~4.8 MB) so the file opens with no internet
    fig.write_html(path, include_plotlyjs=True, full_html=True)


def write_stl(years, lats, z, path, width_mm=180.0, depth_mm=80.0, z_mm_per_degc=12.0, base_mm=5.0):
    """Closed (watertight) solid: top surface = anomaly, flat bottom at z=0.

    Scale: years span width_mm, latitudes span depth_mm, 1 °C = z_mm_per_degc.
    The coldest point sits base_mm above the bottom, so the base is at least base_mm thick.
    """
    z = np.where(np.isnan(z), np.nanmin(z), z)
    ny, nx = z.shape
    X = np.interp(years, (years.min(), years.max()), (0, width_mm))
    Y = np.interp(lats, (lats.min(), lats.max()), (0, depth_mm))
    top = base_mm + (z - z.min()) * z_mm_per_degc

    def v(i, j, h):  # vertex at grid column i, row j, height h
        return (X[i], Y[j], h)

    tris = []
    for j in range(ny - 1):
        for i in range(nx - 1):
            a, b = v(i, j, top[j, i]), v(i + 1, j, top[j, i + 1])
            c, d = v(i + 1, j + 1, top[j + 1, i + 1]), v(i, j + 1, top[j + 1, i])
            tris += [(a, b, c), (a, c, d)]  # top, normal up
            a0, b0, c0, d0 = v(i, j, 0), v(i + 1, j, 0), v(i + 1, j + 1, 0), v(i, j + 1, 0)
            tris += [(a0, c0, b0), (a0, d0, c0)]  # bottom, normal down
    # four side walls
    for i in range(nx - 1):  # front (j=0) and back (j=ny-1)
        j = 0
        tris += [(v(i, j, 0), v(i + 1, j, 0), v(i + 1, j, top[j, i + 1])),
                 (v(i, j, 0), v(i + 1, j, top[j, i + 1]), v(i, j, top[j, i]))]
        j = ny - 1
        tris += [(v(i, j, 0), v(i + 1, j, top[j, i + 1]), v(i + 1, j, 0)),
                 (v(i, j, 0), v(i, j, top[j, i]), v(i + 1, j, top[j, i + 1]))]
    for j in range(ny - 1):  # left (i=0) and right (i=nx-1)
        i = 0
        tris += [(v(i, j, 0), v(i, j + 1, top[j + 1, i]), v(i, j + 1, 0)),
                 (v(i, j, 0), v(i, j, top[j, i]), v(i, j + 1, top[j + 1, i]))]
        i = nx - 1
        tris += [(v(i, j, 0), v(i, j + 1, 0), v(i, j + 1, top[j + 1, i])),
                 (v(i, j, 0), v(i, j + 1, top[j + 1, i]), v(i, j, top[j, i]))]

    save_binary_stl(np.array(tris, dtype=np.float32), path)
    return len(tris), float(top.max())


def save_binary_stl(tris, path):
    """Write triangles (n, 3, 3) as binary STL using numpy only (no extra package to install)."""
    normals = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
    normals /= np.linalg.norm(normals, axis=1, keepdims=True) + 1e-12
    rec = np.zeros(len(tris), dtype=[("n", "<f4", 3), ("v", "<f4", (3, 3)), ("attr", "<u2")])
    rec["n"], rec["v"] = normals, tris
    with open(path, "wb") as f:
        f.write(b"GISTEMP anomaly surface".ljust(80, b" "))
        f.write(np.uint32(len(tris)).tobytes())
        f.write(rec.tobytes())


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--tidy", type=Path, default=Path("outputs/gistemp_tidy.csv"))
    p.add_argument("--out", type=Path, default=Path("outputs"))
    p.add_argument("--stl", action="store_true", help="also write a printable STL (numpy only)")
    a = p.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    years, lats, z = load_grid(a.tidy)
    write_html(years, lats, z, a.out / "anomaly_surface_3d.html")
    print("Wrote", a.out / "anomaly_surface_3d.html")
    if a.stl:
        n, h = write_stl(years, lats, z, a.out / "anomaly_surface.stl")
        print(f"Wrote {a.out / 'anomaly_surface.stl'}: {n} triangles, 180 x 80 mm footprint, "
              f"max height {h:.1f} mm, base >= 5 mm")
