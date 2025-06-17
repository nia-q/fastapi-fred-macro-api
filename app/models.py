from pydantic import BaseModel
from typing import Dict, List, Optional

class IndicatorResponse(BaseModel):
    """
    Response model for a single economic indicator observation.
    
    Attributes:
        title (str): The name or ID of the indicator (e.g., 'CPIAUCSL')
        date (str): The date of the observation in YYYY-MM-DD format
        value (float | None): The observed value, or None if data is missing
    """
    title: str
    date: str
    value: float | None

class TrendResponse(BaseModel):
    """
    Response model for trend analysis of an economic indicator.
    
    Attributes:
        series_id (str): The ID of the economic series
        percent_change (float): Total percentage change over the period
        avg_monthly_change (float): Average change per month
        trend_direction (str): Direction of trend ('up', 'down', or 'flat')
    """
    series_id: str
    percent_change: float
    avg_monthly_change: float
    trend_direction: str


class SeriesCompareItem(BaseModel):
    """
    Model for comparing multiple economic indicators.
    
    Attributes:
        value (float | None): Current value of the indicator
        percent_change (float): Percentage change over the period
        trend_direction (str): Direction of trend ('up', 'down', or 'flat')
    """
    value: float | None
    percent_change: float
    trend_direction: str

class CompareResponse(BaseModel):
    """
    Response model for comparing multiple economic indicators.
    
    Attributes:
        results (Dict[str, SeriesCompareItem]): Dictionary where:
            - Key (str): The ID of the economic indicator (e.g., 'CPIAUCSL')
            - Value (SeriesCompareItem): Comparison data for that indicator
            
    Example:
        {
            "CPIAUCSL": SeriesCompareItem(value=320.58, percent_change=3.2, trend_direction="up"),
            "UNRATE": SeriesCompareItem(value=3.7, percent_change=-0.5, trend_direction="down")
        }
    """
    results: Dict[str, SeriesCompareItem]


class EventImpactRequest(BaseModel):
    series_ids: List[str]
    event_date: str  # ISO format "YYYY-MM-DD"
    months_before: int = 6
    months_after: int = 6

class IndicatorShift(BaseModel):
    before: Optional[float]
    after: Optional[float]
    percent_change: Optional[float]

class EventImpactResponse(BaseModel):
    results: Dict[str, IndicatorShift]