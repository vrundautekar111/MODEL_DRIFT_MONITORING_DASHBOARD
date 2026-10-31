
from pydantic import BaseModel


class PredictionOutput(BaseModel):
    prediction_id: int
    predicted_units: float
    product_id: str
    store_id: str
    target_date: str
    model_version: str
