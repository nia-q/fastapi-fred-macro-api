from app.clients.fred_client import fetch_series_observations
from app.models import IndicatorResponse, TrendResponse

def get_latest_observation(series_id: str) -> IndicatorResponse | None:
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
    try:
        data = fetch_series_observations(series_id, limit=months)
        observations = data.get("observations", [])

        # Need at least 2 data points
        if len(observations) < 2:
            return None

        # Oldest to newest (data is already in descending order, so reverse)
        observations = list(reversed(observations))
        values = [float(obs["value"]) for obs in observations if obs["value"] != "."]

        if len(values) < 2:
            return None

        start = values[0]
        end = values[-1]
        percent_change = ((end - start) / start) * 100
        avg_change = sum((values[i+1] - values[i]) for i in range(len(values)-1)) / (len(values)-1)

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
