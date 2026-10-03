from __future__ import annotations
from math import isfinite
from .earthquake import EarthquakeEvent

def validate_earthquake(event: EarthquakeEvent) -> list[str]:
    errors: list[str] = []
    if not event.source.strip(): errors.append("missing source")
    if not event.source_event_id.strip(): errors.append("missing source event ID")
    if event.magnitude is None or not isfinite(event.magnitude): errors.append("missing or non-finite magnitude")
    elif not -2 <= event.magnitude <= 10: errors.append("magnitude outside valid range")
    for name, value, low, high in (("latitude", event.latitude, -90, 90), ("longitude", event.longitude, -180, 180)):
        if not isfinite(value) or not low <= value <= high: errors.append(f"{name} outside valid range")
    if event.depth_km is not None and (not isfinite(event.depth_km) or event.depth_km < 0): errors.append("depth must be non-negative")
    if not event.location.strip(): errors.append("missing location")
    if event.occurred_at is None: errors.append("missing timestamp")
    return errors
