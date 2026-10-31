
from pydantic import BaseModel


class AlertOutput(BaseModel):
    id: int
    severity: str
    title: str
    details: str | None = None
    status: str
