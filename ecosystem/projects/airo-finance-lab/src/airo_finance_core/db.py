import sqlite3
import os
from typing import Optional

class DatabaseManager:
    def __init__(self, db_path: str = ':memory:'):
        self.db_path = db_path
        self._conn: Optional[sqlite3.Connection] = None

    def get_connection(self) -> sqlite3.Connection:
        if self._conn is None:
            self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self._conn.row_factory = sqlite3.Row
            self._conn.execute('PRAGMA foreign_keys = ON;')
            if self.db_path != ':memory:':
                self._conn.execute('PRAGMA journal_mode = WAL;')
        return self._conn

    def init_schema(self, schema_path: Optional[str] = None) -> None:
        conn = self.get_connection()
        if schema_path is None:
            schema_path = os.path.join(os.path.dirname(__file__), 'schema_sqlite.sql')
        with open(schema_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        conn.executescript(sql_script)
        
        # Idempotently ensure columns exist for existing tables
        self._ensure_column_exists(conn, "accounts", "is_active", "INTEGER NOT NULL DEFAULT 1")
        self._ensure_column_exists(conn, "accounts", "provider", "TEXT")
        self._ensure_column_exists(conn, "accounts", "account_class", "TEXT NOT NULL DEFAULT 'LIQUID'")
        self._ensure_column_exists(conn, "accounts", "dashboard_group", "TEXT NOT NULL DEFAULT 'CASH'")
        self._ensure_column_exists(conn, "accounts", "parent_account_id", "TEXT")
        self._ensure_column_exists(conn, "accounts", "aliases", "TEXT NOT NULL DEFAULT ''")

        self._ensure_column_exists(conn, "categories", "is_active", "INTEGER NOT NULL DEFAULT 1")
        self._ensure_column_exists(conn, "categories", "keywords", "TEXT NOT NULL DEFAULT ''")
        self._ensure_column_exists(conn, "categories", "dashboard_group", "TEXT NOT NULL DEFAULT 'GENERAL'")
        self._ensure_column_exists(conn, "categories", "domain", "TEXT NOT NULL DEFAULT 'PERSONAL'")
        self._ensure_column_exists(conn, "categories", "event_type", "TEXT NOT NULL DEFAULT 'REGULAR'")

        self._ensure_column_exists(conn, "transactions", "subcategory_id", "TEXT REFERENCES subcategories(id)")
        self._ensure_column_exists(conn, "transactions", "status", "TEXT NOT NULL DEFAULT 'ACTIVE'")
        self._ensure_column_exists(conn, "transactions", "voided_at", "TEXT")
        self._ensure_column_exists(conn, "transactions", "void_reason", "TEXT")
        self._ensure_column_exists(conn, "transactions", "updated_at", "TEXT")

        self._ensure_column_exists(conn, "assets", "asset_class", "TEXT DEFAULT 'OTHER'")
        self._ensure_column_exists(conn, "assets", "weight_grams", "REAL DEFAULT 0.0")
        self._ensure_column_exists(conn, "assets", "purchase_cost", "REAL DEFAULT 0.0")
        self._ensure_column_exists(conn, "assets", "average_cost_per_gram", "REAL DEFAULT 0.0")
        self._ensure_column_exists(conn, "assets", "current_unit_price", "REAL DEFAULT 0.0")
        conn.commit()

    def _ensure_column_exists(self, conn: sqlite3.Connection, table: str, column: str, col_def: str) -> None:
        cur = conn.execute(f"PRAGMA table_info({table})")
        existing_cols = [r["name"] for r in cur.fetchall()]
        if column not in existing_cols:
            conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {col_def}")


    def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None
