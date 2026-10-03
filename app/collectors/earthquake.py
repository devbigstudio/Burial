from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class EarthquakeEvent:
    source: str
    source_event_id: str
    magnitude: float | None
    depth_km: float | None
    latitude: float
    longitude: float
    location: str
    occurred_at: datetime | None
    source_url: str | None = None

    @property
    def severity(self) -> str:
        if self.magnitude is None: return "unknown"
        if self.magnitude >= 7: return "critical"
        if self.magnitude >= 6: return "high"
        if self.magnitude >= 5: return "moderate"
        return "low"
