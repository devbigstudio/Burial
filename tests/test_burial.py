import os, tempfile, unittest
from datetime import datetime, timezone
from pathlib import Path
class BurialTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); os.environ["DATABASE_PATH"]=str(Path(self.tmp.name)/"test.db")
        import importlib; import app.config; importlib.reload(app.config)
        import app.database.sqlite as sql; importlib.reload(sql); sql.initialize_database()
    def tearDown(self): self.tmp.cleanup()
    def event(self, **kw):
        from app.collectors.earthquake import EarthquakeEvent
        values=dict(source="USGS",source_event_id="abc",magnitude=5.5,depth_km=10,latitude=1,longitude=2,location="  Test   place ",occurred_at=datetime.now(timezone.utc),source_url="https://example")
        values.update(kw); return EarthquakeEvent(**values)
    def test_validation_and_normalization(self):
        from app.collectors.validation import validate_earthquake
        from app.collectors.normalization import normalize_earthquake
        e=self.event(); self.assertEqual(validate_earthquake(e), []); n=normalize_earthquake(e); self.assertEqual(n.source,"usgs"); self.assertEqual(n.location,"Test place")
    def test_atomic_deduplication(self):
        from app.database.events import save_event
        e=self.event(); self.assertIsNotNone(save_event(e)); self.assertIsNone(save_event(e))
    def test_alert_threshold_is_configurable(self):
        import app.config; app.config.settings=app.config.Settings(alert_magnitude_threshold=6.0)
        from app.database.events import save_event
        from app.alerts.engine import evaluate_and_alert
        event_id=save_event(self.event()); self.assertFalse(evaluate_and_alert(event_id))
    def test_health_has_database(self):
        from app.monitoring.health import health_status
        self.assertEqual(health_status()["database"],"connected")
if __name__ == "__main__": unittest.main()
