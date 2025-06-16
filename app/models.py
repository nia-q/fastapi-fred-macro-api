from pydantic import BaseModel

class IndicatorResponse(BaseModel):
    title: str
    date: str
    value: float | None

class TrendResponse(BaseModel):
    series_id: str
    percent_change: float
    avg_monthly_change: float
    trend_direction: str
