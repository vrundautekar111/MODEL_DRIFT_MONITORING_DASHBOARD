
def test_monitoring_modules_import():
    from src.monitoring.monitoring_service import run_monitoring

    assert callable(run_monitoring)
