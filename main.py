from __future__ import annotations
import argparse, json
from app.config import settings
from app.logging_config import configure_logging
from app.core.worker import run, process_cycle
from app.database.sqlite import initialize_database
from app.monitoring.health import health_status

def main():
    parser=argparse.ArgumentParser(description="BURIAL emergency event monitor")
    parser.add_argument("command", choices=("run","once","health"), nargs="?", default="run")
    args=parser.parse_args(); configure_logging(settings.log_level); initialize_database()
    if args.command=="run": run()
    elif args.command=="once": print(json.dumps(process_cycle(), indent=2))
    else: print(json.dumps(health_status(), indent=2))
if __name__ == "__main__": main()
