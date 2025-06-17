from app.clients.fred_client import fetch_series_observations, get_observations
from app.models import IndicatorResponse, TrendResponse, CompareResponse, SeriesCompareItem, IndicatorShift
from app.constants.constant import SUMMARY_SERIES
from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import List, Dict

def get_latest_observation(series_id: str) -> IndicatorResponse | None:
    """
    Get the most recent observation for a given FRED series.
    
    Args:
        series_id (str): The FRED series ID to fetch
        
    Returns:
        IndicatorResponse | None: Response containing the latest value and date, or None if error
    """
    try:
        data = fetch_series_observations(series_id)
        obs = data.get("observations", [])
        if not obs:
            return None
        latest = obs[0]
        return IndicatorResponse(
            title=series_id,
            date=latest["date"],
            value=float(latest["value"]) if latest["value"] != "." else None
        )
    except Exception:
        return None 
    

def calculate_trend(series_id: str, months: int = 12) -> TrendResponse | None:
    """
    Calculate trend analysis for a given FRED series over a specified time period.
    
    Args:
        series_id (str): The FRED series ID to analyze
        months (int, optional): Number of months to analyze. Defaults to 12.
        
    Returns:
        TrendResponse | None: Response containing trend analysis, or None if insufficient data
        
    Note:
        - Requires at least 2 valid data points
        - Handles missing values (marked as ".")
        - Calculates percent change, average monthly change, and trend direction
        - Trend direction is "up" if change > 0.1%, "down" if change < -0.1%, else "flat"
    """
    try:
        # Fetch the required number of observations
        data = fetch_series_observations(series_id, limit=months)
        observations = data.get("observations", [])

        # Need at least 2 data points for trend analysis
        if len(observations) < 2:
            return None

        # Convert to chronological order (oldest to newest)
        observations = list(reversed(observations))
        # Filter out missing values and convert to float
        values = [float(obs["value"]) for obs in observations if obs["value"] != "."]

        if len(values) < 2:
            return None

        # Calculate trend metrics
        start = values[0]
        end = values[-1]
        percent_change = ((end - start) / start) * 100
        # Calculate average change between consecutive months
        avg_change = sum((values[i+1] - values[i]) for i in range(len(values)-1)) / (len(values)-1)

        # Determine trend direction based on percent change
        direction = "flat"
        if percent_change > 0.1:
            direction = "up"
        elif percent_change < -0.1:
            direction = "down"

        return TrendResponse(
            series_id=series_id,
            percent_change=round(percent_change, 2),
            avg_monthly_change=round(avg_change, 2),
            trend_direction=direction
        )
    except Exception:
        return None
    
def compare_indicators(series_list: list[str], months: int = 12) -> CompareResponse:
    results = {}

    for series_id in series_list:
        # Get latest value
        latest = get_latest_observation(series_id)
        # Get trend
        trend = calculate_trend(series_id, months)

        if not latest or not trend:
            continue  # Skip if incomplete data

        results[series_id] = SeriesCompareItem(
            value=latest.value,
            percent_change=trend.percent_change,
            trend_direction=trend.trend_direction
        )

    return CompareResponse(results=results)

from app.models import CompareResponse, SeriesCompareItem

def get_macro_summary(months: int = 12) -> CompareResponse:
    results = {}

    for series_id in SUMMARY_SERIES.keys():
        latest = get_latest_observation(series_id)
        trend = calculate_trend(series_id, months)

        if not latest or not trend:
            continue

        results[series_id] = SeriesCompareItem(
            value=latest.value,
            percent_change=trend.percent_change,
            trend_direction=trend.trend_direction
        )

    return CompareResponse(results=results)

def determine_macro_regime(indicators: dict[str, float | None]) -> str:
    cpi = indicators.get("CPIAUCSL")
    unrate = indicators.get("UNRATE")
    gdp = indicators.get("GDP")
    fedfunds = indicators.get("FEDFUNDS")

    if cpi is None or unrate is None or gdp is None or fedfunds is None:
        return "unknown"

    if cpi > 3.0 and fedfunds > 3.0:
        return "tightening"
    elif gdp > 2.5 and unrate < 4.0:
        return "expansion"
    elif gdp < 1.0 and unrate > 5.0:
        return "stagnation"
    else:
        return "neutral"

def get_macro_regime() -> str:
    values = {}
    for key in SUMMARY_SERIES.keys():
        result = get_latest_observation(key)
        values[key] = result.value if result else None
    return determine_macro_regime(values)



def calculate_event_impact(
    series_ids: List[str], event_date: str, months_before: int, months_after: int
) -> Dict[str, IndicatorShift]:
    results = {}
    event_dt = datetime.strptime(event_date, "%Y-%m-%d")
    before_dt = event_dt - relativedelta(months=months_before)
    after_dt = event_dt + relativedelta(months=months_after)

    for series_id in series_ids:
        observations = get_observations(series_id, start=before_dt.date(), end=after_dt.date())
        if not observations:
            results[series_id] = IndicatorShift(before=None, after=None, percent_change=None)
            continue

        before_val = None
        after_val = None
        for obs in observations:
            obs_date = datetime.strptime(obs["date"], "%Y-%m-%d").date()
            if abs((obs_date - before_dt.date()).days) < 20:
                before_val = float(obs["value"]) if obs["value"] != "." else None
            if abs((obs_date - after_dt.date()).days) < 20:
                after_val = float(obs["value"]) if obs["value"] != "." else None

        percent_change = None
        if before_val is not None and after_val is not None and before_val != 0:
            percent_change = ((after_val - before_val) / before_val) * 100

        results[series_id] = IndicatorShift(
            before=before_val,
            after=after_val,
            percent_change=percent_change
        )

    return results
