import React, { useState } from 'react';
import {
  Network,
  Satellite,
  Sliders,
  GitCompare,
  Layers,
  MapPin,
  ShieldAlert,
  FileText,
  UserCheck,
  CheckCircle2,
  ArrowRight,
  Code2
} from 'lucide-react';

export const SystemArchitecturePage: React.FC = () => {
  const [activeStage, setActiveStage] = useState<number>(1);

  const stages = [
    {
      id: 1,
      title: '1. Multi-Sensor Ingestion',
      icon: Satellite,
      tech: 'Sentinel-2 (Optical 10m), Sentinel-1 (SAR C-Band), Landsat 8/9',
      summary: 'Automated acquisition of multispectral and radar imagery across monitored mining sectors in India.',
      details: [
        'Optical bands: B2 (Blue), B3 (Green), B4 (Red), B8 (NIR), B11 (SWIR 1), B12 (SWIR 2)',
        'Radar backscatter polarizations: VV (Co-pol) and VH (Cross-pol)',
        'Temporal frequency: 5-day revisit for Sentinel-2, 6-12 days for Sentinel-1',
        'Configurable adapter architecture: Copernicus Open Access Hub & Google Earth Engine APIs'
      ]
    },
    {
      id: 2,
      title: '2. Preprocessing & Masking',
      icon: Sliders,
      tech: 'OpenCV, Rasterio, NumPy, SCL Cloud Filter',
      summary: 'Radiometric calibration, cloud & shadow filtering, coordinate re-projection to WGS84, and spectral index computation.',
      details: [
        'Scene Classification Layer (SCL) masks out cloud and shadow pixels (< 5% cloud tolerance)',
        'Band radiometric calibration and spatial grid harmonization to 10m resolution',
        'Mathematical generation of physical indices: NDVI (Canopy), BSI (Bare Soil), NDWI (Water), NDBI (Roads)',
        'SAR radar speckle filtering and logarithmic backscatter conversion (dB)'
      ]
    },
    {
      id: 3,
      title: '3. Temporal Change Detection',
      icon: GitCompare,
      tech: 'PyTorch, Siamese Dual-Stream CNN / Temporal Transformer',
      summary: 'Infers surface land disturbance magnitude and probability between baseline observation T1 and surveillance acquisition T2.',
      details: [
        'Dual-stream feature extraction using Siamese ResNet-34 backbone',
        'Multi-temporal self-attention across 5-year observation trajectory (2022-2026)',
        'Computes change probability matrix, percentage disturbance, and affected hectares',
        'Deterministic spectral fallback ensures continuous operation without GPU cluster'
      ]
    },
    {
      id: 4,
      title: '4. Disturbance Segmentation',
      icon: Layers,
      tech: 'U-Net, SegFormer-B3, Scikit-Image',
      summary: 'Semantic segmentation of detected disturbance into 12 distinct land-cover and mining feature classes.',
      details: [
        'Target Classes: 7: Active Mining Pit, 8: Overburden Dump, 9: Stockpile, 11: Forest Clearance, 3: Bare Land, 5: Roads',
        'Calculates exact sub-hectare surface breakdown for each disturbance classification',
        'Generates vector polygon contours for GIS integration'
      ]
    },
    {
      id: 5,
      title: '5. GIS Boundary Intersection',
      icon: MapPin,
      tech: 'GeoPandas, Shapely, PostGIS, Leaflet',
      summary: 'Spatial topology analysis intersecting detected disturbance polygons against official mining leases and 500m surveillance buffers.',
      details: [
        'Exact distance calculation in meters from nearest registered mining lease perimeter',
        'Statutory 500-meter surveillance buffer containment evaluation',
        'Classification: INSIDE AUTHORIZED LEASE, WITHIN 500M BUFFER, or OUTSIDE LEASE & BUFFER',
        'Strict adherence to neutral terminology: Potential Unauthorized Mining Activity'
      ]
    },
    {
      id: 6,
      title: '6. Explainable Risk Engine',
      icon: ShieldAlert,
      tech: 'Configurable 7-Factor Weighted Engine (0-100)',
      summary: 'Synthesizes physical disturbance, temporal persistence, boundary violation, and radar anomalies into a normalized 0-100 risk score.',
      details: [
        'Factor Weights: Disturbance Area (25 pts), Persistence (20 pts), Outside Lease (20 pts), Vegetation Loss (10 pts), SAR (10 pts), Expansion (10 pts), Terrain (5 pts)',
        'Risk Thresholds: Low (0-24), Medium (25-49), High (50-74), Critical (75-100)',
        'Feature contribution decomposition for transparent auditability'
      ]
    },
    {
      id: 7,
      title: '7. Explainable Alert Dossier',
      icon: FileText,
      tech: 'FastAPI, ReportLab, React, Recharts',
      summary: 'Generates comprehensive surveillance evidence dossiers including before/after satellite sliders, spectral curves, and printable reports.',
      details: [
        'Interactive split-screen temporal comparison slider',
        'Clear evidence summary and recommended inspection priority',
        'Downloadable executive report containing mandatory scientific & legal disclaimers'
      ]
    },
    {
      id: 8,
      title: '8. Human-in-the-Loop & Feedback',
      icon: UserCheck,
      tech: 'Field Officer Workflow, SQLite/PostgreSQL, Active Learning',
      summary: 'Authorized field officers validate ground truth, log DGPS coordinates, and store verification feedback to continuously retrain AI models.',
      details: [
        'Enforcement lifecycle statuses: Pending, Under Review, Field Verification, Verified, False Positive',
        'Immutable chronological inspection audit trail',
        'Officer feedback loop stored in training database for next-generation model fine-tuning'
      ]
    }
  ];

  const current = stages.find((s) => s.id === activeStage) || stages[0];
  const CurrentIcon = current.icon;

  return (
    <div className="space-y-6 pb-16">
      {/* Header */}
      <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-blue-50 text-blue-600 rounded-lg">
            <Network className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-extrabold text-slate-900">
              Illegal Mining Detection by Using Satellite Data — End-to-End System Architecture
            </h2>
            <p className="text-xs text-slate-500">
              8-Stage integrated surveillance pipeline from raw satellite data ingestion to human-in-the-loop decision support.
            </p>
          </div>
        </div>
      </div>

      {/* 8-Stage Interactive Process Pipeline */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-4 space-y-3">
        <span className="text-xs font-bold uppercase tracking-wider text-slate-500 block">
          Select Pipeline Stage to Inspect Specifications:
        </span>
        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-2">
          {stages.map((stage) => {
            const Icon = stage.icon;
            const isSelected = stage.id === activeStage;
            return (
              <button
                key={stage.id}
                onClick={() => setActiveStage(stage.id)}
                className={`p-2.5 rounded-xl border text-center transition flex flex-col items-center gap-1.5 ${
                  isSelected
                    ? 'bg-blue-600 text-white border-blue-600 shadow-md ring-2 ring-blue-300'
                    : 'bg-slate-50 hover:bg-slate-100 border-slate-200 text-slate-700'
                }`}
              >
                <Icon className={`w-5 h-5 ${isSelected ? 'text-white' : 'text-blue-600'}`} />
                <span className="text-[11px] font-bold leading-tight line-clamp-2">
                  {stage.title}
                </span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Active Stage Deep Dive */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-5 space-y-4">
        <div className="flex flex-wrap items-start justify-between gap-3 pb-3 border-b border-slate-200">
          <div className="flex items-center gap-3">
            <div className="p-3 bg-blue-50 text-blue-600 rounded-xl">
              <CurrentIcon className="w-6 h-6" />
            </div>
            <div>
              <h3 className="text-base font-extrabold text-slate-900">{current.title}</h3>
              <div className="text-xs font-mono font-semibold text-blue-600 mt-0.5">
                Core Stack: {current.tech}
              </div>
            </div>
          </div>
          <span className="text-xs font-bold text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-md border border-emerald-200">
            Pipeline Stage {current.id} of 8
          </span>
        </div>

        <p className="text-sm font-semibold text-slate-800 leading-relaxed bg-slate-50 p-3 rounded-lg border border-slate-200">
          {current.summary}
        </p>

        <div className="space-y-2">
          <span className="text-xs font-bold uppercase tracking-wider text-slate-500 block">
            Technical Implementation Details:
          </span>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
            {current.details.map((detail, idx) => (
              <div
                key={idx}
                className="flex items-start gap-2 text-xs text-slate-700 bg-slate-50 p-2.5 rounded-lg border border-slate-200"
              >
                <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                <span>{detail}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
