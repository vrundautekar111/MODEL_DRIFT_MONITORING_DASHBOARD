
from fastapi import APIRouter, HTTPException

from app.schemas.sales import ActualSalesInput
from database.repository import (
    add_actual,
    get_labeled_predictions,
)
from src.monitoring.performance import (
    evaluate_labeled_predictions,
)

router = APIRouter(
    prefix="/sales",
    tags=["Actual Sales"],
)


@router.post("/actual")
def submit_actual(payload: ActualSalesInput):
    updated = add_actual(
        payload.target_date,
        payload.product_id,
        payload.store_id,
        payload.actual_units,
    )

    if updated == 0:
        raise HTTPException(
            status_code=404,
            detail=(
                "No matching prediction found. "
                "Use the same date, product and store."
            ),
        )

    return {
        "updated_records": updated,
        "message": "Actual sales saved.",
    }


@router.get("/performance")
def performance():
    return evaluate_labeled_predictions(
        get_labeled_predictions()
    )
