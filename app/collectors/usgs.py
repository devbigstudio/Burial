from __future__ import annotations
import json, logging, time
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from .earthquake import EarthquakeEvent
from app.config import settings

log = logging.getLogger("burial.collector")

def fetch_earthquakes() -> list[EarthquakeEvent]:
    last_error: Exception | None = None
    for attempt in range(1, settings.retry_attempts + 1):
        try:
            request = Request(settings.feed_url, headers={"User-Agent": "BURIAL/0.1.0"})
            with urlopen(request, timeout=settings.request_timeout_seconds) as response:
                payload = json.load(response)
            events = [_parse_feature(item) for item in payload.get("features", [])]
            log.info("collection_success", extra={"event_count": len(events), "attempt": attempt})
            return [event for event in events if event is not None]
        except (OSError, ValueError, HTTPError, URLError) as exc:
            last_error = exc
            log.warning("collection_failure", extra={"attempt": attempt, "error": str(exc)[:200]})
            if attempt < settings.retry_attempts: time.sleep(settings.retry_backoff_seconds * (2 ** (attempt - 1)))
    raise RuntimeError(f"USGS collection failed after {settings.retry_attempts} attempts: {last_error}")

def _parse_feature(item: dict) -> EarthquakeEvent | None:
    props, geometry = item.get("properties") or {}, item.get("geometry") or {}
    coords = geometry.get("coordinates") or []
    if len(coords) < 2: return None
    timestamp = props.get("time")
    occurred = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc) if timestamp is not None else None
    return EarthquakeEvent("usgs", str(item.get("id") or ""), props.get("mag"), coords[2] if len(coords) > 2 else None,
        coords[1], coords[0], props.get("place") or "Unknown", occurred, props.get("url"))
