from __future__ import annotations
import json, logging, sys
class JsonFormatter(logging.Formatter):
    def format(self, record):
        payload={"timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"), "level":record.levelname, "logger":record.name, "message":record.getMessage()}
        for key in ("event_count","attempt","error","event_id","channel","delivered","new_events","duplicate_events","rejected_events"): 
            if hasattr(record,key): payload[key]=getattr(record,key)
        return json.dumps(payload, default=str)
def configure_logging(level: str = "INFO"):
    handler=logging.StreamHandler(sys.stdout); handler.setFormatter(JsonFormatter()); root=logging.getLogger(); root.handlers.clear(); root.addHandler(handler); root.setLevel(level.upper())
