
import json

from src.monitoring.monitoring_service import run_monitoring
from src.alerts.alert_rules import build_alerts
from src.retraining.trigger_rules import (
    evaluate_retraining_trigger,
)


if __name__ == "__main__":
    result = run_monitoring()

    result["alerts"] = build_alerts(result)

    result["retraining"] = evaluate_retraining_trigger(
        result
    )

    print(
        json.dumps(
            result,
            indent=2,
            default=str,
        )
    )
