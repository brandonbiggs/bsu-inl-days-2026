"""Stage 5 reference: build data.db (SQLite) from the tidy file.

Run from the attendee-kit folder:  uv run python checkpoints/stage5_mcp/build_db.py
Reads outputs/gistemp_tidy.csv. Writes outputs/data.db (or --db PATH).
Table: anomalies(year INTEGER, band TEXT, lat_min REAL, lat_max REAL, anomaly REAL)
Uses only the Python standard library.
"""
import argparse
import csv
import sqlite3
from pathlib import Path


def main(tidy, db):
    if db.exists():
        db.unlink()
    con = sqlite3.connect(db)
    con.execute("""CREATE TABLE anomalies (
        year INTEGER NOT NULL,
        band TEXT NOT NULL,
        lat_min REAL NOT NULL,
        lat_max REAL NOT NULL,
        anomaly REAL,              -- °C vs 1951-1980; NULL if missing in source
        PRIMARY KEY (year, band))""")
    with open(tidy, newline="", encoding="utf-8") as f:
        rows = [(int(r["year"]), r["band"], float(r["lat_min"]), float(r["lat_max"]),
                 float(r["anomaly"]) if r["anomaly"] not in ("", "nan") else None)
                for r in csv.DictReader(f)]
    con.executemany("INSERT INTO anomalies VALUES (?,?,?,?,?)", rows)
    con.commit()
    n, y0, y1 = con.execute("SELECT COUNT(*), MIN(year), MAX(year) FROM anomalies").fetchone()
    con.close()
    print(f"Wrote {db}: {n} rows, years {y0}-{y1}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--tidy", type=Path, default=Path("outputs/gistemp_tidy.csv"))
    p.add_argument("--db", type=Path, default=Path("outputs/data.db"))
    a = p.parse_args()
    main(a.tidy, a.db)
