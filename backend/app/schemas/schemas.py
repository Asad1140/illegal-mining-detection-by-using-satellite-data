from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

# Auth Schemas
class UserResponse(BaseModel):
    id: str
    username: str
    full_name: str
    email: str
    role: str
    department: str

class SwitchRoleRequest(BaseModel):
    role: str

# Verification Schemas
class VerificationCreate(BaseModel):
    alert_id: str
    status: str # VERIFIED, FALSE_POSITIVE, REJECTED, UNDER_REVIEW, FIELD_VERIFICATION
    comments: str
    gps_coordinates: Optional[str] = None
    evidence_notes: Optional[str] = None
    photo_urls: Optional[List[str]] = []

class VerificationResponse(BaseModel):
    id: str
    alert_id: str
    verified_by: str
    officer_role: str
    status: str
    comments: str
    gps_coordinates: Optional[str] = None
    evidence_notes: Optional[str] = None
    photo_urls: List[str] = []
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)

# Risk Breakdown Schema
class RiskFactorBreakdown(BaseModel):
    disturbance_score: float
    temporal_persistence_score: float
    outside_lease_score: float
    vegetation_loss_score: float
    sar_anomaly_score: float
    historical_expansion_score: float
    terrain_context_score: float
    total_score: float
    risk_category: str # LOW, MEDIUM, HIGH, CRITICAL
    explanation_bullets: List[str]

# Alert Schemas
class AlertSummary(BaseModel):
    id: str
    title: str
    lease_id: Optional[str] = None
    state: str
    district: str
    location_name: str
    latitude: float
    longitude: float
    risk_score: float
    priority: str
    disturbed_area_ha: float
    lease_status: str
    distance_from_lease_m: float
    first_detected: str
    last_detected: str
    status: str
    confidence: float
    explanation_summary: str
    assigned_officer: str

    model_config = ConfigDict(from_attributes=True)

class AlertDetail(AlertSummary):
    geometry: Dict[str, Any]
    risk_factors: RiskFactorBreakdown
    verifications: List[VerificationResponse] = []
    created_at: datetime
    updated_at: datetime

# Mining Lease & Cadastre Schemas
class MiningLeaseSummary(BaseModel):
    id: str
    name: str
    state: str
    district: str
    mineral: str
    area_hectares: float
    status: str
    lessee_name: str
    grant_date: Optional[str] = None
    expiry_date: Optional[str] = None
    center_lat: float
    center_lng: float
    active_alerts_count: int = 0

    model_config = ConfigDict(from_attributes=True)

class MiningLeaseDetail(MiningLeaseSummary):
    geometry: Dict[str, Any]
    surveillance_buffer_geojson: Optional[Dict[str, Any]] = None

# Global Mining Inventory Schema
class GlobalMiningSite(BaseModel):
    id: str
    name: str
    country: str
    country_code: str
    region: str
    mineral: str
    center_lat: float
    center_lng: float
    zoom: int = 13
    source: str
    source_url: str
    data_type: str # OFFICIAL_LEASE or MINING_FOOTPRINT
    has_authoritative_lease: bool
    operator: str
    estimated_area_ha: float

# Legacy / Timeline Satellite Schema
class SatelliteObservationItem(BaseModel):
    id: str
    platform: str
    sensor_type: str
    region: str
    acquisition_date: str
    year: int
    cloud_coverage: float
    cloud_masked: bool
    mean_ndvi: float
    mean_ndwi: float
    mean_ndbi: float
    mean_bsi: float
    sar_vv_mean: float
    sar_vh_mean: float
    thumbnail_url: Optional[str] = None
    metadata_json: Dict[str, Any] = {}

    model_config = ConfigDict(from_attributes=True)

# Real Copernicus Satellite Schemas
class SatelliteSearchRequest(BaseModel):
    aoi_geojson: Optional[Dict[str, Any]] = None
    bbox: Optional[List[float]] = None
    point: Optional[List[float]] = None
    start_date: str = "2024-01-01"
    end_date: str = "2026-08-25"
    sensors: List[str] = ["sentinel-2", "sentinel-1"]
    max_cloud_cover: float = 30.0
    limit: int = 20

class RealSatelliteObservationItem(BaseModel):
    product_id: str
    product_name: str
    mission: str
    sensor_type: str
    processing_level: str
    acquisition_date: str
    cloud_cover: Optional[float] = None
    footprint: Optional[Dict[str, Any]] = None
    polarisation_channels: Optional[str] = None
    orbit_number: Optional[int] = None
    orbit_direction: Optional[str] = None
    quicklook_url: Optional[str] = None
    content_length_bytes: Optional[int] = None
    data_source: str = "Copernicus Data Space Ecosystem (CDSE)"

class SatelliteSearchResponse(BaseModel):
    observations: List[RealSatelliteObservationItem]
    total_found: int
    data_source: str
    query_aoi: Optional[Dict[str, Any]] = None
    cloud_filter_applied: float

class AOIAnalyzeRequest(BaseModel):
    aoi_geojson: Dict[str, Any]
    t1_observation: Dict[str, Any]
    t2_observation: Dict[str, Any]
    buffer_distance_m: float = 500.0
    sensitivity: float = 0.75

class AOIAnalyzeResponse(BaseModel):
    analysis_id: str
    risk_score: float
    risk_category: str
    changed_area_ha: float
    change_percentage: float
    confidence_score: float
    relationship: str
    distance_from_lease_meters: float
    is_inside_lease: bool
    is_within_buffer: bool
    authoritative_lease_available: bool
    spectral_deltas: Dict[str, Any]
    sar_roughness_delta_db: float
    sar_anomaly_detected: bool
    class_areas_ha: Dict[str, float]
    alternative_explanations: List[str]
    explanation_bullets: List[str]
    evidence_summary: str
    provenance: Dict[str, Any]
    disclaimer: str

# Geocoding Schemas
class GeocodeSearchRequest(BaseModel):
    query: str
    limit: int = 5

class GeocodeResultItem(BaseModel):
    display_name: str
    lat: float
    lon: float
    type: Optional[str] = None
    class_name: Optional[str] = Field(default=None, alias="class")
    bbox: Optional[List[float]] = None
    geojson: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(populate_by_name=True)

# Dashboard KPIs
class DashboardStats(BaseModel):
    total_monitored_areas: int
    active_alerts: int
    high_risk_alerts: int
    potential_disturbed_area_ha: float
    verified_cases: int
    pending_verification: int
    risk_distribution: Dict[str, int]
    status_distribution: Dict[str, int]
    district_summaries: List[Dict[str, Any]]
    disturbance_trend: List[Dict[str, Any]]
    alerts_over_time: List[Dict[str, Any]]
    data_mode: str = "REAL_COPERNICUS"
    satellite_sources_count: int = 4

# Legacy & Preset Analysis Request / Response
class AnalyzeRequest(BaseModel):
    region: str
    start_year: int = 2022
    end_year: int = 2026
    algorithm: str = "Spectral Difference & Siamese Baseline"
    sensitivity: float = 0.75

class ChangeAnalysisResult(BaseModel):
    analysis_id: str
    region: str
    model_name: str
    model_status: str
    first_detected_date: str
    latest_detected_date: str
    change_percentage: float
    changed_area_hectares: float
    change_confidence: float
    vegetation_loss_percentage: float
    sar_backscatter_delta_db: float
    spectral_indices: Dict[str, Any]
    segmentation_classes: Dict[str, float]
    predicted_expansion: Dict[str, Any]
    change_geojson: Dict[str, Any]
    disclaimer: str

# Settings Update
class SettingsUpdate(BaseModel):
    disturbance_weight: Optional[float] = None
    temporal_weight: Optional[float] = None
    outside_lease_weight: Optional[float] = None
    vegetation_loss_weight: Optional[float] = None
    sar_anomaly_weight: Optional[float] = None
    historical_expansion_weight: Optional[float] = None
    terrain_context_weight: Optional[float] = None
    buffer_distance_m: Optional[float] = None
    satellite_provider: Optional[str] = None
    gee_project_id: Optional[str] = None
    nasa_api_key: Optional[str] = None
    copernicus_client_id: Optional[str] = None
    copernicus_client_secret: Optional[str] = None
    real_data_mode: Optional[bool] = None
