import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check_real_mode():
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "HEALTHY"
    assert "REAL SATELLITE" in data["mode"] or "DEMO" in data["mode"]

def test_global_mining_sites_api():
    resp = client.get("/api/mining-sites")
    assert resp.status_code == 200
    sites = resp.json()
    assert len(sites) >= 8
    assert any(s["country"] == "Australia" for s in sites)
    assert any(s["country"] == "Brazil" for s in sites)
    assert any(s["country"] == "Chile" for s in sites)

def test_copernicus_satellite_search_api():
    # Search for real Sentinel scenes in Keonjhar
    payload = {
        "point": [85.58, 21.84],
        "start_date": "2024-01-01",
        "end_date": "2026-08-25",
        "sensors": ["sentinel-2", "sentinel-1"],
        "max_cloud_cover": 50.0,
        "limit": 5
    }
    resp = client.post("/api/satellite/search", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "observations" in data
    assert data["total_found"] > 0
    obs = data["observations"][0]
    assert "product_id" in obs
    assert "acquisition_date" in obs
    assert "mission" in obs

def test_aoi_temporal_analysis_api():
    payload = {
        "aoi_geojson": {
            "type": "Polygon",
            "coordinates": [[[85.58, 21.84], [85.59, 21.84], [85.59, 21.85], [85.58, 21.85], [85.58, 21.84]]]
        },
        "t1_observation": {
            "mission": "Sentinel-2",
            "product_id": "S2A_TEST_T1",
            "acquisition_date": "2024-02-10T05:00:00Z",
            "mean_ndvi": 0.68,
            "mean_bsi": -0.12,
            "sar_vv_mean": -14.5
        },
        "t2_observation": {
            "mission": "Sentinel-2",
            "product_id": "S2B_TEST_T2",
            "acquisition_date": "2026-08-14T05:00:00Z",
            "mean_ndvi": 0.15,
            "mean_bsi": 0.52,
            "sar_vv_mean": -7.8
        },
        "buffer_distance_m": 500.0,
        "sensitivity": 0.8
    }
    resp = client.post("/api/satellite/analyze", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "risk_score" in data
    assert "changed_area_ha" in data
    assert "provenance" in data
    assert "disclaimer" in data
    assert data["risk_score"] > 0
