import pytest
from app.ai.risk_engine import risk_engine

def test_risk_engine_flagship_high_risk():
    factors = {
        "disturbed_area_ha": 14.2,
        "is_persistent": True,
        "lease_status": "Outside registered lease",
        "distance_from_lease_m": 180.0,
        "vegetation_loss_pct": 78.5,
        "sar_anomaly_detected": True,
        "growth_rate_pct": 18.3,
        "near_vulnerable_ecosystem": True
    }
    result = risk_engine.calculate_risk(factors)
    assert result["total_score"] >= 75.0
    assert result["risk_category"] == "CRITICAL"
    assert len(result["explanation_bullets"]) == 7
    assert "factor_scores" in result

def test_risk_engine_low_risk():
    factors = {
        "disturbed_area_ha": 1.2,
        "is_persistent": False,
        "lease_status": "Inside Authorized Lease",
        "distance_from_lease_m": 0.0,
        "vegetation_loss_pct": 10.0,
        "sar_anomaly_detected": False,
        "growth_rate_pct": 0.0,
        "near_vulnerable_ecosystem": False
    }
    result = risk_engine.calculate_risk(factors)
    assert result["total_score"] < 40.0
    assert result["risk_category"] in ["LOW", "MEDIUM"]
