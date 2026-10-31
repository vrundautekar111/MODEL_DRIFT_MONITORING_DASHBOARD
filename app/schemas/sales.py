
from pydantic import BaseModel, Field


class SalesFeatureInput(BaseModel):
    date: str
    product_id: str
    category: str
    store_id: str
    price: float = Field(ge=0)
    discount_pct: float = Field(ge=0, le=100)
    marketing_spend: float = Field(ge=0)
    stock_available: int = Field(ge=0)
    day_of_week: int = Field(ge=0, le=6)
    is_weekend: int = Field(ge=0, le=1)
    is_promotion: int = Field(ge=0, le=1)


class ActualSalesInput(BaseModel):
    target_date: str
    product_id: str
    store_id: str
    actual_units: float = Field(ge=0)

