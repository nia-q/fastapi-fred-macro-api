import os
import httpx
from app.models import IndicatorResponse
from dotenv import load_dotenv

load_dotenv()

FRED_API_KEY = os.getenv("FRED_API_KEY")
FRED_BASE_URL = "https://api.stlouisfed.org/fred"

def get_latest_observation(series_id: str):
    url = f"{FRED_BASE_URL}/series/observations"
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "sort_order": "desc",
        "limit": 1
    }
    try:
        response = httpx.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if "observations" not in data or not data["observations"]:
            return None
        obs = data["observations"][0]
        return IndicatorResponse(
            title=series_id,
            date=obs["date"],
            value=float(obs["value"]) if obs["value"] != "." else None
        )
    except Exception:
        return None
