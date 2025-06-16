from fastapi import APIRouter, HTTPException
from app.services.fred_client import get_latest_observation
from app.models import IndicatorResponse

router = APIRouter()

@router.get("/indicator/{series_id}", response_model=IndicatorResponse)
def indicator(series_id: str):
    data = get_latest_observation(series_id)
    if not data:
        raise HTTPException(status_code=404, detail="Series not found or no data")
    return data
