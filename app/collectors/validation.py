from __future__ import annotations
from math import isfinite
from .earthquake import EarthquakeEvent

def _finite_number(value: object) -> bool:
    try:
        return isfinite(float(value))
    except (TypeError, ValueError):
        return False

def validate_earthquake(event: EarthquakeEvent) -> list[str]:
    errors: list[str] = []
    if not isinstance(event.source, str) or not event.source.strip(): errors.append("missing source")
    if not isinstance(event.source_event_id, str) or not event.source_event_id.strip(): errors.append("missing source event ID")
    if event.magnitude is None or not _finite_number(event.magnitude): errors.append("missing or non-finite magnitude")
    elif not -2 <= float(event.magnitude) <= 10: errors.append("magnitude outside valid range")
    for name, value, low, high in (("latitude", event.latitude, -90, 90), ("longitude", event.longitude, -180, 180)):
        if not _finite_number(value) or not low <= float(value) <= high: errors.append(f"{name} outside valid range")
    if event.depth_km is not None and (not _finite_number(event.depth_km) or float(event.depth_km) < 0): errors.append("depth must be non-negative")
    if not isinstance(event.location, str) or not event.location.strip(): errors.append("missing location")
    if event.occurred_at is None: errors.append("missing timestamp")
    return errors
