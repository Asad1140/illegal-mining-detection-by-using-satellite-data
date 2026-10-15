import os
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class RiskWeights(BaseModel):
    disturbance_weight: float = 25.0
    temporal_weight: float = 20.0
    outside_lease_weight: float = 20.0
    vegetation_loss_weight: float = 10.0
    sar_anomaly_weight: float = 10.0
    historical_expansion_weight: float = 10.0
    terrain_context_weight: float = 5.0

class RiskThresholds(BaseModel):
    low_max: float = 24.0
    medium_max: float = 49.0
    high_max: float = 74.0
    critical_min: float = 75.0

class Settings(BaseModel):
    PROJECT_NAME: str = "Illegal Mining Detection by Using Satellite Data"
    VERSION: str = "2.0.0"
    API_V1_STR: str = "/api"
    DESCRIPTION: str = "AI-Powered Satellite Mining Surveillance, Change Detection & Early-Warning System"
    
    # Environment & Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./illegal_mining_detection.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "illegal-mining-detection-secret-key-development-mode-2026")
    
    # Mode Configuration: REAL_DATA_MODE vs DEMO_MODE
    # Default to REAL_DATA_MODE when Copernicus credentials exist or by default for live Earth observation
    REAL_DATA_MODE: bool = os.getenv("REAL_DATA_MODE", "true").lower() in ("true", "1", "yes")
    DEMO_MODE: bool = os.getenv("DEMO_MODE", "false").lower() in ("true", "1", "yes")
    
    # GIS Surveillance Configuration
    DEFAULT_BUFFER_DISTANCE_METERS: float = 500.0
    MAX_AOI_AREA_KM2: float = 2500.0  # Safeguard for large-scale queries
    
    # Copernicus Data Space Ecosystem (CDSE) Credentials
    COPERNICUS_CLIENT_ID: str = os.getenv("COPERNICUS_CLIENT_ID", "")
    COPERNICUS_CLIENT_SECRET: str = os.getenv("COPERNICUS_CLIENT_SECRET", "")
    CDSE_USERNAME: str = os.getenv("CDSE_USERNAME", "")
    CDSE_PASSWORD: str = os.getenv("CDSE_PASSWORD", "")
    
    # Sentinel Hub & CDSE Endpoints
    SENTINEL_HUB_CLIENT_ID: str = os.getenv("SENTINEL_HUB_CLIENT_ID", "")
    SENTINEL_HUB_CLIENT_SECRET: str = os.getenv("SENTINEL_HUB_CLIENT_SECRET", "")
    
    CDSE_AUTH_URL: str = os.getenv(
        "CDSE_AUTH_URL",
        "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
    )
    CDSE_CATALOG_URL: str = os.getenv(
        "CDSE_CATALOG_URL",
        "https://catalogue.dataspace.copernicus.eu/odata/v1/Products"
    )
    CDSE_STAC_URL: str = os.getenv(
        "CDSE_STAC_URL",
        "https://stac.dataspace.copernicus.eu/v1"
    )
    
    # Satellite Preprocessing & Quality Thresholds
    S2_MAX_CLOUD_COVER: float = 30.0
    MIN_USABLE_PIXEL_PERCENT: float = 70.0
    
    # AI Engine Modes
    MODEL_STATUS: str = "Baseline Statistical & Spectral Change Engine (Model-Ready)"
    
    # Risk Engine Configuration
    RISK_WEIGHTS: RiskWeights = RiskWeights()
    RISK_THRESHOLDS: RiskThresholds = RiskThresholds()

    # Mandatory Legal & Scientific Disclaimer
    DISCLAIMER: str = (
        "Illegal Mining Detection by Using Satellite Data is an AI-assisted monitoring and decision-support system. "
        "Satellite and AI outputs indicate potential land-use or mining-related disturbance and "
        "should be independently verified. The system does not make legal determinations of illegal mining."
    )

settings = Settings()
