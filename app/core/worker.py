from __future__ import annotations
import logging, signal, time
from datetime import datetime, timezone
from app.collectors.usgs import fetch_earthquakes
from app.collectors.validation import validate_earthquake
from app.collectors.normalization import normalize_earthquake
from app.database.events import save_event
from app.database.sqlite import initialize_database
from app.alerts.engine import evaluate_and_alert
from app.config import settings
log=logging.getLogger("burial.worker")
_stop=False

def _handle_stop(signum, frame):
    global _stop; _stop=True; log.info("shutdown_requested")

def process_cycle() -> dict:
    events=fetch_earthquakes(); result={"total":len(events),"new":0,"duplicates":0,"rejected":0}
    for raw in events:
        errors=validate_earthquake(raw)
        if errors: result["rejected"]+=1; log.warning("validation_failure", extra={"error":"; ".join(errors)}); continue
        event=normalize_earthquake(raw); event_id=save_event(event)
        if event_id is None: result["duplicates"]+=1; log.info("duplicate_event", extra={"event_id":event.source_event_id}); continue
        result["new"]+=1; log.info("new_event", extra={"event_id":event.source_event_id}); evaluate_and_alert(event_id)
    log.info("cycle_complete", extra={"new_events":result["new"],"duplicate_events":result["duplicates"],"rejected_events":result["rejected"]}); return result

def run() -> None:
    signal.signal(signal.SIGINT, _handle_stop); signal.signal(signal.SIGTERM, _handle_stop); initialize_database(); log.info("application_startup")
    while not _stop:
        try: process_cycle()
        except Exception as exc: log.exception("collection_cycle_failure", extra={"error":str(exc)[:200]})
        if not _stop: time.sleep(settings.poll_interval_seconds)
    log.info("application_shutdown")
