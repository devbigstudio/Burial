# BURIAL

**Emergency Event Detection & Alert System**, reserved by Andre Technologies.

BURIAL v0.1 continuously polls the public USGS earthquake GeoJSON feed, validates and normalizes events, atomically deduplicates them in SQLite, evaluates configurable magnitude alerts, and records Discord webhook delivery outcomes.

## Quick start

```powershell
Copy-Item .env.example .env
python -m pip install -r requirements.txt
python main.py health
python main.py once
python main.py run
```

Set `DISCORD_WEBHOOK_URL` only in the untracked `.env` file. Thresholds, polling, timeout, retries, and database location are environment-configurable. No `.env` file belongs in Git.

## Docker

```powershell
docker compose up -d --build
docker compose logs -f burial
```

The container runs as a non-root user and persists SQLite data through `./data`. Docker is required for this deployment path.

## Architecture

`USGS collector → validation → normalization → SQLite atomic deduplication → alert engine → Discord webhook`

Structured JSON logs include lifecycle, collection, validation, duplicate, alert, and failure events. Health reports application, database, collector, notification, version, and timestamp fields.

## Tests

`python -m unittest discover -s tests -v` runs the standard-library test suite; `pytest` is also supported.

## Scope and limitations

This is an information and alerting system, not a prediction or emergency-response system. It does not guarantee delivery during network or Discord outages, and an unconfigured webhook is reported as `not_configured`. The initial collector is USGS earthquakes only.
