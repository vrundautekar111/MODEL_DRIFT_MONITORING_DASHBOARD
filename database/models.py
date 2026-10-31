
from typing import Optional
from pydantic import BaseModel


class PredictionRecord(BaseModel):
    target_date: str
    product_id: str
    store_id: str
    predicted_units: float
    actual_units: Optional[float] = None
    model_version: str = "local-v1"
