export type UserRole = 'ADMIN' | 'ANALYST' | 'FIELD_OFFICER' | 'VIEWER';

export interface UserProfile {
  id: string;
  username: string;
  full_name: string;
  email: string;
  role: UserRole;
  department: string;
}

export type RiskLevel = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';

export type AlertStatus =
  | 'PENDING'
  | 'UNDER_REVIEW'
  | 'FIELD_VERIFICATION'
  | 'VERIFIED'
  | 'FALSE_POSITIVE'
  | 'REJECTED'
  | 'CLOSED';

export interface RiskBreakdown {
  disturbance_score: number;
  temporal_persistence_score: number;
  outside_lease_score: number;
  vegetation_loss_score: number;
  sar_anomaly_score: number;
  historical_expansion_score: number;
  terrain_context_score: number;
  total_score: number;
  risk_category: RiskLevel;
  explanation_bullets: string[];
}

export interface VerificationRecord {
  id: string;
  alert_id: string;
  verified_by: string;
  officer_role: string;
  status: AlertStatus;
  comments: string;
  gps_coordinates?: string;
  evidence_notes?: string;
  photo_urls: string[];
  timestamp: string;
}

export interface Alert {
  id: string;
  title: string;
  lease_id?: string;
  state: string;
  district: string;
  location_name: string;
  latitude: number;
  longitude: number;
  risk_score: number;
  priority: RiskLevel;
  disturbed_area_ha: number;
  lease_status: string;
  distance_from_lease_m: number;
  first_detected: string;
  last_detected: string;
  status: AlertStatus;
  confidence: number;
  explanation_summary: string;
  assigned_officer: string;
  geometry?: any;
  risk_factors?: RiskBreakdown;
  verifications?: VerificationRecord[];
  created_at?: string;
  updated_at?: string;
}

export interface MiningLease {
  id: string;
  name: string;
  state: string;
  district: string;
  mineral: string;
  area_hectares: number;
  status: string;
  lessee_name: string;
  grant_date?: string;
  expiry_date?: string;
  center_lat: number;
  center_lng: number;
  active_alerts_count: number;
  geometry?: any;
  surveillance_buffer_geojson?: any;
}

export interface GlobalMiningSite {
  id: string;
  name: string;
  country: string;
  country_code: string;
  region: string;
  mineral: string;
  center_lat: number;
  center_lng: number;
  zoom: number;
  source: string;
  source_url: string;
  data_type: 'OFFICIAL_LEASE' | 'MINING_FOOTPRINT';
  has_authoritative_lease: boolean;
  operator: string;
  estimated_area_ha: number;
}

export interface RealSatelliteObservationItem {
  product_id: string;
  product_name: string;
  mission: string;
  sensor_type: string;
  processing_level: string;
  acquisition_date: string;
  cloud_cover?: number;
  footprint?: any;
  polarisation_channels?: string;
  orbit_number?: number;
  orbit_direction?: string;
  quicklook_url?: string;
  content_length_bytes?: number;
  data_source: string;
}

export interface SatelliteSearchResponse {
  observations: RealSatelliteObservationItem[];
  total_found: number;
  data_source: string;
  query_aoi?: any;
  cloud_filter_applied: number;
}

export interface AOIAnalyzeResponse {
  analysis_id: string;
  risk_score: number;
  risk_category: string;
  changed_area_ha: number;
  change_percentage: number;
  confidence_score: number;
  relationship: string;
  distance_from_lease_meters: number;
  is_inside_lease: boolean;
  is_within_buffer: boolean;
  authoritative_lease_available: boolean;
  spectral_deltas: Record<string, any>;
  sar_roughness_delta_db: number;
  sar_anomaly_detected: boolean;
  class_areas_ha: Record<string, number>;
  alternative_explanations: string[];
  explanation_bullets: string[];
  evidence_summary: string;
  provenance: Record<string, any>;
  disclaimer: string;
}

export interface GeocodeResultItem {
  display_name: string;
  lat: number;
  lon: number;
  type?: string;
  class?: string;
  bbox?: number[];
  geojson?: any;
}

export interface SatelliteObservation {
  id: string;
  platform: string;
  sensor_type: string;
  region: string;
  acquisition_date: string;
  year: number;
  cloud_coverage: number;
  cloud_masked: boolean;
  mean_ndvi: number;
  mean_ndwi: number;
  mean_ndbi: number;
  mean_bsi: number;
  sar_vv_mean: number;
  sar_vh_mean: number;
  status?: string;
  disturbed_area_ha?: number;
  band_values?: Record<string, number>;
}

export interface DashboardStats {
  total_monitored_areas: number;
  active_alerts: number;
  high_risk_alerts: number;
  potential_disturbed_area_ha: number;
  verified_cases: number;
  pending_verification: number;
  risk_distribution: {
    LOW: number;
    MEDIUM: number;
    HIGH: number;
    CRITICAL: number;
  };
  status_distribution: Record<string, number>;
  district_summaries: Array<{
    district: string;
    state: string;
    mineral: string;
    active_alerts: number;
    critical: number;
    disturbed_ha: number;
    avg_risk: number;
  }>;
  disturbance_trend: Array<{
    year: string;
    area_ha: number;
    rate_pct: string;
  }>;
  alerts_over_time: Array<{
    month: string;
    alerts: number;
    high_risk: number;
  }>;
}

export interface DataSourceItem {
  id: string;
  name: string;
  source_type: string;
  provider: string;
  purpose: string;
  resolution: string;
  update_frequency: string;
  status: string;
  is_live: boolean;
  last_sync: string;
}

export interface PreprocessingStep {
  step: string;
  status: string;
  icon: string;
  details: string;
}

export interface AIModelStatus {
  module: string;
  active_model: string;
  model_type: string;
  status: string;
  input_shape: string;
  inference_latency_ms: number;
  f1_score?: string;
  mIoU?: string;
  explainability?: string;
  direction_accuracy?: string;
  supported_alternatives: string[];
}
