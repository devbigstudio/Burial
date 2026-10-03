from __future__ import annotations
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from app.config import settings

@contextmanager
def get_connection():
    path = Path(settings.database_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def initialize_database() -> None:
    with get_connection() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT, source TEXT NOT NULL, source_event_id TEXT NOT NULL, event_type TEXT NOT NULL, magnitude REAL, depth_km REAL, latitude REAL NOT NULL, longitude REAL NOT NULL, location TEXT NOT NULL, occurred_at TEXT, severity TEXT NOT NULL, source_url TEXT, created_at TEXT NOT NULL, UNIQUE(source, source_event_id));
        CREATE TABLE IF NOT EXISTS alerts (id INTEGER PRIMARY KEY AUTOINCREMENT, event_id INTEGER NOT NULL REFERENCES events(id), channel TEXT NOT NULL, status TEXT NOT NULL, attempts INTEGER NOT NULL DEFAULT 0, sent_at TEXT, error TEXT, created_at TEXT NOT NULL, UNIQUE(event_id, channel));
        CREATE TABLE IF NOT EXISTS health (key TEXT PRIMARY KEY, value TEXT NOT NULL, updated_at TEXT NOT NULL);
        """)
