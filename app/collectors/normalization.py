from __future__ import annotations
from datetime import timezone
from .earthquake import EarthquakeEvent

def normalize_earthquake(event: EarthquakeEvent) -> EarthquakeEvent:
    occurred_at = event.occurred_at
    if occurred_at and occurred_at.tzinfo is None: occurred_at = occurred_at.replace(tzinfo=timezone.utc)
    elif occurred_at: occurred_at = occurred_at.astimezone(timezone.utc)
    return EarthquakeEvent(
        source=event.source.strip().lower(), source_event_id=event.source_event_id.strip(),
        magnitude=float(event.magnitude) if event.magnitude is not None else None,
        depth_km=float(event.depth_km) if event.depth_km is not None else None,
        latitude=float(event.latitude), longitude=float(event.longitude),
        location=" ".join(event.location.split()), occurred_at=occurred_at,
        source_url=event.source_url.strip() if event.source_url else None)
