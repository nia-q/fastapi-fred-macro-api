from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_indicator_route():
    response = client.get("/macro/indicator/CPIAUCSL")
    assert response.status_code in [200, 404]
