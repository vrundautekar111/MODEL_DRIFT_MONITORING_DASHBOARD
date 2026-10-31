
from fastapi import APIRouter, HTTPException

from database.repository import (
    list_alerts,
    resolve_alert,
)

router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"],
)


@router.get("")
def alerts():
    return list_alerts()


@router.post("/{alert_id}/resolve")
def resolve(alert_id: int):
    count = resolve_alert(alert_id)

    if count == 0:
        raise HTTPException(
            status_code=404,
            detail="Alert not found",
        )

    return {
        "resolved": True,
        "alert_id": alert_id,
    }
