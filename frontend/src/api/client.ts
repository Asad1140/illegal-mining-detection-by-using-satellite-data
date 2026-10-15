import {
  Alert,
  MiningLease,
  DashboardStats,
  SatelliteObservation,
  DataSourceItem,
  AIModelStatus,
  VerificationRecord,
  GlobalMiningSite,
  SatelliteSearchResponse,
  AOIAnalyzeResponse,
  GeocodeResultItem
} from '../types';

const API_BASE = '/api';

export const apiClient = {
  // Auth
  async getCurrentUser(role: string = 'ADMIN') {
    const res = await fetch(`${API_BASE}/auth/me?role=${role}`);
    return res.json();
  },

  async getAvailableRoles() {
    const res = await fetch(`${API_BASE}/auth/roles`);
    return res.json();
  },

  // Dashboard
  async getDashboardStats(region: string = 'ALL'): Promise<DashboardStats> {
    const res = await fetch(`${API_BASE}/dashboard/stats?region=${region}`);
    return res.json();
  },

  // Alerts
  async getAlerts(params: {
    district?: string;
    priority?: string;
    status?: string;
    min_risk?: number;
    sort_by?: string;
  } = {}): Promise<Alert[]> {
    const query = new URLSearchParams();
    if (params.district && params.district !== 'ALL') query.append('district', params.district);
    if (params.priority && params.priority !== 'ALL') query.append('priority', params.priority);
    if (params.status && params.status !== 'ALL') query.append('status', params.status);
    if (params.min_risk !== undefined) query.append('min_risk', params.min_risk.toString());
    if (params.sort_by) query.append('sort_by', params.sort_by);

    const res = await fetch(`${API_BASE}/alerts?${query.toString()}`);
    return res.json();
  },

  async getAlertById(id: string): Promise<Alert> {
    const res = await fetch(`${API_BASE}/alerts/${id}`);
    if (!res.ok) throw new Error(`Alert ${id} not found`);
    return res.json();
  },

  // Mining Leases & GIS
  async getMiningLeases(params: { district?: string; mineral?: string } = {}): Promise<MiningLease[]> {
    const query = new URLSearchParams();
    if (params.district && params.district !== 'ALL') query.append('district', params.district);
    if (params.mineral && params.mineral !== 'ALL') query.append('mineral', params.mineral);

    const res = await fetch(`${API_BASE}/mines/leases?${query.toString()}`);
    return res.json();
  },

  async getLeaseById(id: string): Promise<MiningLease> {
    const res = await fetch(`${API_BASE}/mines/leases/${id}`);
    return res.json();
  },

  async getRegionGisLayers(region: string) {
    const res = await fetch(`${API_BASE}/mines/gis/layers/${region}`);
    return res.json();
  },

  // Global Mining Inventory
  async getGlobalMiningSites(country?: string, mineral?: string): Promise<GlobalMiningSite[]> {
    const query = new URLSearchParams();
    if (country && country !== 'ALL') query.append('country', country);
    if (mineral && mineral !== 'ALL') query.append('mineral', mineral);
    const res = await fetch(`${API_BASE}/mining-sites?${query.toString()}`);
    return res.json();
  },

  async getGlobalMiningSiteById(id: string): Promise<GlobalMiningSite> {
    const res = await fetch(`${API_BASE}/mining-sites/${id}`);
    return res.json();
  },

  // Real Copernicus Satellite Search & Temporal Analysis
  async searchSatelliteCatalog(payload: {
    aoi_geojson?: any;
    bbox?: number[];
    point?: number[];
    start_date?: string;
    end_date?: string;
    sensors?: string[];
    max_cloud_cover?: number;
    limit?: number;
  }): Promise<SatelliteSearchResponse> {
    const res = await fetch(`${API_BASE}/satellite/search`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Copernicus Satellite Catalog Search Failed');
    }
    return res.json();
  },

  async analyzeAOITemporalChange(payload: {
    aoi_geojson: any;
    t1_observation: any;
    t2_observation: any;
    buffer_distance_m?: number;
    sensitivity?: number;
  }): Promise<AOIAnalyzeResponse> {
    const res = await fetch(`${API_BASE}/satellite/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Temporal Change Analysis Failed');
    }
    return res.json();
  },

  // Worldwide Geocoding Search
  async geocodeSearch(query: string, limit: number = 5): Promise<GeocodeResultItem[]> {
    const res = await fetch(`${API_BASE}/geocode/search`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, limit }),
    });
    return res.json();
  },

  // Legacy Satellite Timeline
  async getSatelliteTimeline(region: string): Promise<SatelliteObservation[]> {
    const res = await fetch(`${API_BASE}/satellite/timeline/${region}`);
    return res.json();
  },

  async getPreprocessingStatus() {
    const res = await fetch(`${API_BASE}/satellite/preprocessing/status`);
    return res.json();
  },

  async getDataSources(): Promise<DataSourceItem[]> {
    const res = await fetch(`${API_BASE}/satellite/sources`);
    return res.json();
  },

  // AI Inference & Models
  async runAiAnalysis(payload: {
    region: string;
    algorithm?: string;
    sensitivity?: number;
  }) {
    const res = await fetch(`${API_BASE}/ai/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return res.json();
  },

  async getAiModelsStatus(): Promise<AIModelStatus[]> {
    const res = await fetch(`${API_BASE}/ai/models/status`);
    return res.json();
  },

  // Verification
  async getVerificationQueue(status: string = 'ALL') {
    const res = await fetch(`${API_BASE}/verification/queue?status=${status}`);
    return res.json();
  },

  async submitVerification(payload: {
    alert_id: string;
    status: string;
    comments: string;
    gps_coordinates?: string;
    evidence_notes?: string;
    photo_urls?: string[];
  }): Promise<VerificationRecord> {
    const res = await fetch(`${API_BASE}/verification/submit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return res.json();
  },

  async getVerificationHistory(alertId: string): Promise<VerificationRecord[]> {
    const res = await fetch(`${API_BASE}/verification/history/${alertId}`);
    return res.json();
  },

  // Settings
  async getSettings() {
    const res = await fetch(`${API_BASE}/settings`);
    return res.json();
  },

  async updateSettings(payload: any) {
    const res = await fetch(`${API_BASE}/settings/update`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return res.json();
  },

  async testCopernicusConnection() {
    const res = await fetch(`${API_BASE}/settings/test-copernicus`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    });
    return res.json();
  },

  // Report
  async getAlertReportData(alertId: string) {
    const res = await fetch(`${API_BASE}/reports/alert/${alertId}`);
    return res.json();
  }
};
