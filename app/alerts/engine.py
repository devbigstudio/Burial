from __future__ import annotations
import logging
from app.config import settings
from app.database.alerts import create_alert, record_attempt
from app.database.events import get_event
from .discord import send_alert
log = logging.getLogger("burial.alerts")

def evaluate_and_alert(event_id: int) -> bool:
    event = get_event(event_id)
    if not event or event["magnitude"] is None or event["magnitude"] < settings.alert_magnitude_threshold: return False
    if not create_alert(event_id, "discord"): return False
    success, error = send_alert(dict(event)); record_attempt(event_id, "discord", success, error)
    log.info("alert_triggered", extra={"event_id": event_id, "delivered": success})
    return True
