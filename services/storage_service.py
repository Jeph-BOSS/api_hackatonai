import os
import sqlite3
from typing import Optional, Dict, Any
from pydantic import BaseModel


DB_PATH = os.getenv("DB_PATH", "./data.db")


class StorageService:
    def __init__(self, db_path: str = DB_PATH) -> None:
        self.db_path = db_path
        self._ensure_schema()

    def _ensure_schema(self) -> None:
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS analyses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    raw_json TEXT NOT NULL,
                    geojson TEXT NOT NULL
                )
                """
            )
            conn.commit()
        finally:
            conn.close()

    def save_result(self, raw: Any, geojson: Any) -> str:
        import json
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute(
                "INSERT INTO analyses(raw_json, geojson) VALUES(?, ?)",
                (json.dumps(raw), json.dumps(geojson)),
            )
            conn.commit()
            cur = conn.execute("SELECT last_insert_rowid()")
            rid = cur.fetchone()[0]
            return str(rid)
        finally:
            conn.close()

    def get_result(self, record_id: str) -> Optional[Dict[str, Any]]:
        import json
        conn = sqlite3.connect(self.db_path)
        try:
            cur = conn.execute("SELECT id, raw_json, geojson FROM analyses WHERE id = ?", (record_id,))
            row = cur.fetchone()
            if not row:
                return None
            return {"id": str(row[0]), "raw": json.loads(row[1]), "geojson": json.loads(row[2])}
        finally:
            conn.close()


_storage_singleton: Optional[StorageService] = None


def get_storage() -> StorageService:
    global _storage_singleton
    if _storage_singleton is None:
        _storage_singleton = StorageService()
    return _storage_singleton




