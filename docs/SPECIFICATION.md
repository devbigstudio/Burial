# BURIAL v0.1 Operational Specification

## Pipeline

External USGS GeoJSON is fetched with a bounded timeout and exponential backoff, parsed into `EarthquakeEvent`, validated as untrusted input, normalized to UTC and stable strings, and persisted with a unique `(source, source_event_id)` key. Only the insert winner can trigger an alert.

## Persistence

SQLite uses WAL mode and parameterized queries. `events` stores identity, event type, coordinates, magnitude, depth, place, occurrence time, severity, source URL, and creation time. `alerts` stores channel, status, attempts, sent time, error, and creation time.

## Reliability and security

The worker catches cycle failures, continues polling, and handles SIGINT/SIGTERM. Credentials are environment-only; logs never emit the webhook URL. Compose persists the database and restarts the service.

## Health

`python main.py health` returns machine-readable JSON with application, database, collector, Discord, version, and check timestamp. Collector recency is available to the worker integration and is `unknown` before a cycle runs.
