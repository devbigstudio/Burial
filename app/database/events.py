from __future__ import annotations
from datetime import datetime, timezone
from app.collectors.earthquake import EarthquakeEvent
from .sqlite import get_connection

def save_event(event: EarthquakeEvent) -> int | None:
    with get_connection() as db:
        cur = db.execute("INSERT OR IGNORE INTO events (source,source_event_id,event_type,magnitude,depth_km,latitude,longitude,location,occurred_at,severity,source_url,created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (event.source,event.source_event_id,"earthquake",event.magnitude,event.depth_km,event.latitude,event.longitude,event.location,event.occurred_at.isoformat() if event.occurred_at else None,event.severity,event.source_url,datetime.now(timezone.utc).isoformat()))
        return cur.lastrowid if cur.rowcount else None

def get_event(event_id: int):
    with get_connection() as db: return db.execute("SELECT * FROM events WHERE id=?", (event_id,)).fetchone()
