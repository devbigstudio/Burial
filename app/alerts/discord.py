from __future__ import annotations
import json, logging
from urllib.request import Request, urlopen
from app.config import settings
log = logging.getLogger("burial.discord")

def send_alert(event: dict) -> tuple[bool, str | None]:
    if not settings.discord_webhook_url: return False, "DISCORD_WEBHOOK_URL is not configured"
    content = f"BURIAL earthquake alert | M{event['magnitude']:.1f} | {event['location']} | {event['occurred_at']}"
    request = Request(settings.discord_webhook_url, data=json.dumps({"content": content[:1900]}).encode(), headers={"Content-Type":"application/json","User-Agent":"BURIAL/0.1.0"}, method="POST")
    try:
        with urlopen(request, timeout=settings.request_timeout_seconds): pass
        log.info("alert_delivered", extra={"channel":"discord","event_id":event["id"]}); return True, None
    except Exception as exc:
        log.error("alert_delivery_failure", extra={"channel":"discord","event_id":event["id"],"error":str(exc)[:200]}); return False, str(exc)
