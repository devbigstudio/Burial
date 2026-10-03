from __future__ import annotations
from datetime import datetime, timezone
from app.config import settings
from app.database.sqlite import get_connection

def health_status(last_collection: str | None = None, collector: str = "unknown") -> dict:
    try:
        with get_connection() as db: db.execute("SELECT 1")
        database="connected"
    except Exception: database="error"
    discord="available" if settings.discord_webhook_url else "not_configured"
    return {"status":"healthy" if database=="connected" else "degraded", "application":"online", "database":database, "collector":collector, "last_successful_collection":last_collection, "discord":discord, "version":"0.1.0", "checked_at":datetime.now(timezone.utc).isoformat()}
