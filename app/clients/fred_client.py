import os
import httpx
from dotenv import load_dotenv
from datetime import date
from typing import List

# Load environment variables from .env file
load_dotenv()

# FRED API configuration
FRED_API_KEY = os.getenv("FRED_API_KEY")
FRED_BASE_URL = "https://api.stlouisfed.org/fred"

def fetch_series_observations(series_id: str, limit: int = 1):
    """
    Fetch time series observations from the FRED API.
    
    Args:
        series_id (str): The FRED series ID to fetch (e.g., 'CPIAUCSL' for Consumer Price Index)
        limit (int, optional): Number of most recent observations to fetch. Defaults to 1.
        
    Returns:
        dict: JSON response from FRED API containing observations
        
    Raises:
        HTTPException: If the API request fails or returns an error
    """
    url = f"{FRED_BASE_URL}/series/observations"
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "sort_order": "desc",  # Get most recent observations first
        "limit": limit
    }
    response = httpx.get(url, params=params)
    response.raise_for_status()
    return response.json() 

def get_observations(series_id: str, start: date, end: date) -> List[dict]:
    url = f"{FRED_BASE_URL}/series/observations"
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "observation_start": start.isoformat(),
        "observation_end": end.isoformat()
    }
    try:
        response = httpx.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("observations", [])
    except Exception:
        return []
