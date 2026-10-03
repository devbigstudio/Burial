from __future__ import annotations
from datetime import datetime, timezone
from .sqlite import get_connection

def create_alert(event_id: int, channel: str) -> bool:
    with get_connection() as db:
        cur = db.execute("INSERT OR IGNORE INTO alerts (event_id,channel,status,created_at) VALUES (?,?,?,?)", (event_id, channel, "pending", datetime.now(timezone.utc).isoformat()))
        return bool(cur.rowcount)

def record_attempt(event_id: int, channel: str, success: bool, error: str | None = None) -> None:
    with get_connection() as db:
        db.execute("UPDATE alerts SET status=?, attempts=attempts+1, sent_at=?, error=? WHERE event_id=? AND channel=?", ("sent" if success else "failed", datetime.now(timezone.utc).isoformat() if success else None, error[:500] if error else None, event_id, channel))
