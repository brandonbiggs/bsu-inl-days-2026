"""A small, read-only SQLite MCP server for the session.

Usage (Claude Code starts it for you; see prompts.md, Stage 5):
    uv run python mcp/sqlite_server.py outputs/data.db

Read-only by design: the database is opened with SQLite's mode=ro, so no tool can change it.
Built on the official MCP Python SDK (package "mcp"). About 60 lines: read it before you trust it.
"""
import sqlite3
import sys
from contextlib import closing
from pathlib import Path

from mcp.server.fastmcp import FastMCP

DB = Path(sys.argv[1] if len(sys.argv) > 1 else "outputs/data.db").resolve()
MAX_ROWS = 500

mcp = FastMCP("gistemp-db")


def connect():
    if not DB.exists():
        raise FileNotFoundError(f"Database not found: {DB}. Build it first (see prompts.md, Stage 5).")
    return closing(sqlite3.connect(DB.as_uri() + "?mode=ro", uri=True))  # as_uri handles Windows drives and spaces


@mcp.tool()
def list_tables() -> list[str]:
    """List the tables in the database."""
    with connect() as con:
        return [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]


@mcp.tool()
def describe_table(table: str) -> list[dict]:
    """Show the columns (name, type) of one table."""
    with connect() as con:
        rows = con.execute("SELECT name, type FROM pragma_table_info(?)", (table,)).fetchall()
    if not rows:
        raise ValueError(f"No table named {table!r}")
    return [{"name": n, "type": t} for n, t in rows]


@mcp.tool()
def read_query(sql: str) -> dict:
    """Run one read-only SQL query (SELECT or WITH) and return columns and rows (max 500 rows)."""
    with connect() as con:
        cur = con.execute(sql)
        cols = [d[0] for d in cur.description or []]
        rows = cur.fetchmany(MAX_ROWS + 1)
    return {"columns": cols, "rows": [list(r) for r in rows[:MAX_ROWS]],
            "truncated": len(rows) > MAX_ROWS}


if __name__ == "__main__":
    mcp.run()
