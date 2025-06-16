from fastapi import APIRouter, HTTPException
from app.services.macro_service import get_latest_observation, calculate_trend
from app.models import IndicatorResponse, TrendResponse

router = APIRouter()

@router.get("/indicator/{series_id}", response_model=IndicatorResponse)
async def get_indicator(series_id: str):
    result = get_latest_observation(series_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Series {series_id} not found or error occurred")
    return result

@router.get("/trend/{series_id}", response_model=TrendResponse, tags=["Macro Trends"])
def get_trend(series_id: str, months: int = 12):
    """
    Calculate percent change, average monthly change, and trend direction over the past `months`.
    """
    trend = calculate_trend(series_id, months)
    if not trend:
        raise HTTPException(status_code=404, detail="Not enough data to calculate trend.")
    return trend