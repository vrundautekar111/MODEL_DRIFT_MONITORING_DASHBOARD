
from typing import Any
from pydantic import BaseModel


class MonitoringOutput(BaseModel):
    status: str
    rows_checked: int
    quality: dict[str, Any]
    drift: list[dict[str, Any]]
    recommendation: str
