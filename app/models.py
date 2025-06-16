from pydantic import BaseModel

class IndicatorResponse(BaseModel):
    title: str
    date: str
    value: float | None
