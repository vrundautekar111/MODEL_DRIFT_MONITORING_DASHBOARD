
from fastapi import APIRouter, HTTPException

from app.schemas.sales import SalesFeatureInput
from database.repository import save_prediction
from src.models.predict import load_model, predict_one

router = APIRouter(
    prefix="/predictions",
    tags=["Predictions"],
)


@router.post("")
def create_prediction(payload: SalesFeatureInput):
    try:
        data = payload.model_dump()
        prediction = predict_one(data)
        bundle = load_model()

        record = {
            "target_date": data["date"],
            "product_id": data["product_id"],
            "store_id": data["store_id"],
            "predicted_units": round(prediction, 3),
            "model_version": bundle.get(
                "version", "local-v1"
            ),
        }

        record["prediction_id"] = save_prediction(
            record
        )

        return record

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        )
