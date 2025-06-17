from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_indicator_route():
    response = client.get("/macro/indicator/CPIAUCSL")
    assert response.status_code in [200, 404]

def test_trend_route():
    response = client.get("/macro/trend/CPIAUCSL?months=12")
    assert response.status_code in [200, 404]

def test_compare_route():
    response = client.get("/macro/compare?series=CPIAUCSL,UNRATE")
    assert response.status_code in [200, 404]

def test_summary_route():
    response = client.get("/macro/summary")
    assert response.status_code in [200, 404]

def test_regime_route():
    response = client.get("/macro/regime")
    assert response.status_code in [200, 404]

def test_event_impact_route():
    response = client.post("/macro/event-impact", json={"series_ids": ["CPIAUCSL", "UNRATE"], "event_date": "2024-01-01"})
    assert response.status_code in [200, 404]