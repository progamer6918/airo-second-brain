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
        return self._conn

    def init_schema(self, schema_path: Optional[str] = None) -> None:
        conn = self.get_connection()
        if schema_path is None:
            schema_path = os.path.join(os.path.dirname(__file__), 'schema_sqlite.sql')
        with open(schema_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        conn.executescript(sql_script)
        conn.commit()

    def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None
