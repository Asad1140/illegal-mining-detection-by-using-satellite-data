import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "HEALTHY"

def test_dashboard_stats(client):
    response = client.get("/api/dashboard/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["total_monitored_areas"] == 128
    assert "risk_distribution" in data
    assert "district_summaries" in data

def test_alerts_and_dossier(client):
    response = client.get("/api/alerts")
    assert response.status_code == 200
    alerts = response.json()
    assert len(alerts) > 0
    
    # Test specific flagship alert
    alert_id = alerts[0]["id"]
    detail_res = client.get(f"/api/alerts/{alert_id}")
    assert detail_res.status_code == 200
    detail = detail_res.json()
    assert detail["id"] == alert_id
    assert "risk_factors" in detail
    assert "geometry" in detail

def test_satellite_timeline(client):
    response = client.get("/api/satellite/timeline/Keonjhar")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    assert data[0]["region"] == "Keonjhar"

def test_field_verification_submission(client):
    response = client.post("/api/verification/submit", json={
        "alert_id": "MG-2026-00421",
        "status": "FIELD_VERIFICATION",
        "comments": "Automated test field inspection note.",
        "gps_coordinates": "21.8523, 85.5932",
        "evidence_notes": "Boundary marker confirmed outside lease perimeter."
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "FIELD_VERIFICATION"
    assert data["alert_id"] == "MG-2026-00421"
