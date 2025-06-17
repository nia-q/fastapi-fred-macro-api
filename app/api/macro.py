from fastapi import APIRouter, HTTPException
from app.services.macro_service import get_latest_observation, calculate_trend, compare_indicators, get_macro_summary, get_macro_regime, calculate_event_impact
from app.models import IndicatorResponse, TrendResponse, CompareResponse, EventImpactRequest, EventImpactResponse

# Create a router for macro-economic data endpoints
router = APIRouter()

@router.get("/indicator/{series_id}", response_model=IndicatorResponse)
async def get_indicator(series_id: str):
    """
    Get the latest observation for a given FRED series ID.
    
    Args:
        series_id (str): The FRED series ID (e.g., 'CPIAUCSL' for Consumer Price Index)
        
    Returns:
        IndicatorResponse: Object containing the latest value, date, and series title
        
    Raises:
        HTTPException: 404 if the series is not found or an error occurs
    """
    result = get_latest_observation(series_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Series {series_id} not found or error occurred")
    return result

@router.get("/trend/{series_id}", response_model=TrendResponse, tags=["Macro Trends"])
def get_trend(series_id: str, months: int = 12):
    """
    Calculate trend analysis for a given FRED series over a specified time period.
    
    Args:
        series_id (str): The FRED series ID (e.g., 'CPIAUCSL' for Consumer Price Index)
        months (int, optional): Number of months to analyze. Defaults to 12.
        
    Returns:
        TrendResponse: Object containing:
            - percent_change: Total percentage change over the period
            - avg_monthly_change: Average change per month
            - trend_direction: "up", "down", or "flat" based on the overall trend
            
    Raises:
        HTTPException: 404 if there's not enough data to calculate the trend
    """
    trend = calculate_trend(series_id, months)
    if not trend:
        raise HTTPException(status_code=404, detail="Not enough data to calculate trend.")
    return trend

@router.get("/compare", response_model=CompareResponse, tags=["Macro Comparison"])
def get_comparison(series: str, months: int = 12):
    """
    Compare the latest values and trends of multiple indicators.
    Pass comma-separated series IDs, like: CPIAUCSL,UNRATE,GDP
    """
    series_ids = [s.strip() for s in series.split(",")]
    result = compare_indicators(series_ids, months)
    if not result.results:
        raise HTTPException(status_code=404, detail="No valid series found.")
    return result
from app.services.macro_service import get_macro_summary

@router.get("/summary", response_model=CompareResponse, tags=["Macro Summary"])
def get_macro_summary_route():
    """
    Returns a curated summary of core macroeconomic indicators:
    CPI, GDP, Unemployment Rate, and Fed Funds Rate.
    """
    summary = get_macro_summary()
    if not summary.results:
        raise HTTPException(status_code=404, detail="Could not retrieve summary.")
    return summary

@router.get("/regime")
def get_macro_regime_route():
    regime = get_macro_regime()
    return {"regime": regime}

@router.post("/event-impact", response_model=EventImpactResponse)
def analyze_event_impact(request: EventImpactRequest):
    impact = calculate_event_impact(
        series_ids=request.series_ids,
        event_date=request.event_date,
        months_before=request.months_before,
        months_after=request.months_after
    )
    return EventImpactResponse(results=impact)
