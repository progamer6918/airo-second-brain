import os
import sqlite3
from pathlib import Path

from airo_personal_workflow.core.config import DATA_DIR, DB_PATH

SCHEMA_PATH = Path(__file__).with_name("schema.sql")

def init_db() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(schema)

    if os.environ.get("AIRO_DB_QUIET") != "1":
        print(f"DB_READY={DB_PATH}")

if __name__ == "__main__":
    init_db()
