from fastapi import APIRouter
from typing import Dict, Any
from app.core.config import settings
from app.schemas.schemas import SettingsUpdate
from app.services.satellite.copernicus_auth import copernicus_auth
from app.services.satellite.cdse_catalog import cdse_catalog

router = APIRouter(prefix="/settings", tags=["System Settings & Configurations"])

@router.get("")
def get_system_settings():
    """Returns current active settings, risk factor weights, threshold brackets, and satellite adapter state."""
    return {
        "project_name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "real_data_mode": settings.REAL_DATA_MODE,
        "demo_mode": settings.DEMO_MODE,
        "model_status": settings.MODEL_STATUS,
        "buffer_distance_meters": settings.DEFAULT_BUFFER_DISTANCE_METERS,
        "risk_weights": {
            "disturbance_weight": settings.RISK_WEIGHTS.disturbance_weight,
            "temporal_weight": settings.RISK_WEIGHTS.temporal_weight,
            "outside_lease_weight": settings.RISK_WEIGHTS.outside_lease_weight,
            "vegetation_loss_weight": settings.RISK_WEIGHTS.vegetation_loss_weight,
            "sar_anomaly_weight": settings.RISK_WEIGHTS.sar_anomaly_weight,
            "historical_expansion_weight": settings.RISK_WEIGHTS.historical_expansion_weight,
            "terrain_context_weight": settings.RISK_WEIGHTS.terrain_context_weight,
            "total_max_score": 100.0
        },
        "risk_thresholds": {
            "low_max": settings.RISK_THRESHOLDS.low_max,
            "medium_max": settings.RISK_THRESHOLDS.medium_max,
            "high_max": settings.RISK_THRESHOLDS.high_max,
            "critical_min": settings.RISK_THRESHOLDS.critical_min
        },
        "satellite_adapters": {
            "satellite_provider": "COPERNICUS_DATA_SPACE_ECOSYSTEM",
            "copernicus_auth_configured": copernicus_auth.has_cdse_credentials,
            "cdse_catalog_url": settings.CDSE_CATALOG_URL,
            "sentinelhub_configured": copernicus_auth.has_sentinelhub_credentials,
            "gee_project_id": settings.GEE_PROJECT_ID or "NOT_CONFIGURED",
            "nasa_api_key_configured": bool(settings.NASA_API_KEY)
        },
        "disclaimer": settings.DISCLAIMER
    }

@router.post("/update")
def update_system_settings(payload: SettingsUpdate):
    """Updates configurable weights, buffer radius, and satellite credentials."""
    if payload.disturbance_weight is not None:
        settings.RISK_WEIGHTS.disturbance_weight = payload.disturbance_weight
    if payload.temporal_weight is not None:
        settings.RISK_WEIGHTS.temporal_weight = payload.temporal_weight
    if payload.outside_lease_weight is not None:
        settings.RISK_WEIGHTS.outside_lease_weight = payload.outside_lease_weight
    if payload.vegetation_loss_weight is not None:
        settings.RISK_WEIGHTS.vegetation_loss_weight = payload.vegetation_loss_weight
    if payload.sar_anomaly_weight is not None:
        settings.RISK_WEIGHTS.sar_anomaly_weight = payload.sar_anomaly_weight
    if payload.historical_expansion_weight is not None:
        settings.RISK_WEIGHTS.historical_expansion_weight = payload.historical_expansion_weight
    if payload.terrain_context_weight is not None:
        settings.RISK_WEIGHTS.terrain_context_weight = payload.terrain_context_weight

    if payload.buffer_distance_m is not None:
        settings.DEFAULT_BUFFER_DISTANCE_METERS = payload.buffer_distance_m
    if payload.copernicus_client_id is not None:
        settings.COPERNICUS_CLIENT_ID = payload.copernicus_client_id
    if payload.copernicus_client_secret is not None:
        settings.COPERNICUS_CLIENT_SECRET = payload.copernicus_client_secret
    if payload.real_data_mode is not None:
        settings.REAL_DATA_MODE = payload.real_data_mode
        settings.DEMO_MODE = not payload.real_data_mode

    return {
        "status": "SUCCESS",
        "message": "Settings updated successfully",
        "real_data_mode": settings.REAL_DATA_MODE,
        "active_weights": settings.RISK_WEIGHTS.model_dump(),
        "buffer_distance_meters": settings.DEFAULT_BUFFER_DISTANCE_METERS
    }

@router.post("/test-copernicus")
async def test_copernicus_connection():
    """Tests live connectivity to the Copernicus Data Space Catalogue API."""
    try:
        results = await cdse_catalog.search_satellite_scenes(
            point=(85.58, 21.84),
            start_date="2024-01-01",
            end_date="2026-08-25",
            sensors=["sentinel-2"],
            limit=2
        )
        return {
            "status": "CONNECTED",
            "message": "Successfully connected to Copernicus Data Space Ecosystem (CDSE) Catalogue API.",
            "test_query_location": "Keonjhar, Odisha (85.58°E, 21.84°N)",
            "live_products_found": len(results),
            "latest_product_name": results[0].product_name if results else None,
            "latest_acquisition_date": results[0].acquisition_date if results else None
        }
    except Exception as e:
        return {
            "status": "ERROR",
            "message": f"Failed to query Copernicus Catalogue API: {str(e)}"
        }
