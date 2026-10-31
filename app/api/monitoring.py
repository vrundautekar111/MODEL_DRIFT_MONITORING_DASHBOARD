
from fastapi import APIRouter, HTTPException

from src.monitoring.monitoring_service import run_monitoring
from src.alerts.alert_rules import build_alerts
from src.retraining.trigger_rules import (
    evaluate_retraining_trigger,
)
from database.repository import save_monitoring, list_monitoring

router = APIRouter(
    prefix="/monitoring",
    tags=["Monitoring"],
)


@router.post("/run")
def monitor():
    try:
        result = run_monitoring()

        result["alerts"] = build_alerts(result)

        result["retraining"] = (
            evaluate_retraining_trigger(result)
        )

        result["run_id"] = save_monitoring(result)

        return result

    except (FileNotFoundError, ValueError) as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.get("/history")
def history():
    return list_monitoring()
