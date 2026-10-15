import React, { useState, useEffect } from 'react';
import { useApp } from '../context/AppContext';
import { apiClient } from '../api/client';
import {
  FileText,
  Printer,
  ShieldAlert,
  MapPin,
  Calendar,
  Layers,
  ArrowLeft,
  CheckCircle2
} from 'lucide-react';

export const ReportViewPage: React.FC = () => {
  const { activeAlertId, setCurrentPage } = useApp();
  const [report, setReport] = useState<any | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    if (!activeAlertId) return;
    setLoading(true);
    apiClient
      .getAlertReportData(activeAlertId)
      .then((data) => {
        setReport(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error('Failed to load report:', err);
        setLoading(false);
      });
  }, [activeAlertId]);

  if (loading || !report) {
    return (
      <div className="flex items-center justify-center p-12 text-slate-500">
        <div className="w-6 h-6 border-2 border-blue-600 border-t-transparent rounded-full animate-spin mr-3"></div>
        <span className="text-sm font-semibold">Generating Executive Report Dossier...</span>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-4xl mx-auto pb-16">
      {/* Top Action Bar */}
      <div className="flex items-center justify-between gap-3 print:hidden">
        <button
          onClick={() => setCurrentPage('alert-details')}
          className="flex items-center gap-1.5 text-xs font-bold text-slate-600 hover:text-slate-900 bg-white px-3 py-1.5 rounded-lg border border-slate-200 shadow-xs transition"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Back to Alert Dossier</span>
        </button>

        <button
          onClick={() => window.print()}
          className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-xs font-bold shadow transition"
        >
          <Printer className="w-4 h-4" />
          <span>Print / Export PDF Dossier</span>
        </button>
      </div>

      {/* Printable Report Document Paper */}
      <div className="bg-white rounded-xl border border-slate-300 shadow-md p-8 md:p-12 space-y-6 text-slate-800 font-sans print:border-none print:shadow-none print:p-0">
        {/* Document Header */}
        <div className="border-b-2 border-slate-900 pb-4 flex items-start justify-between">
          <div>
            <div className="text-[10px] font-bold uppercase tracking-widest text-slate-500">
              GOVERNMENT SURVEILLANCE & REMOTE SENSING CELL
            </div>
            <h1 className="text-xl md:text-2xl font-black tracking-tight text-slate-950 mt-1">
              Illegal Mining Detection by Using Satellite Data
            </h1>
            <div className="text-xs font-bold text-red-700 uppercase tracking-wider mt-0.5">
              {report.report_title}
            </div>
          </div>
          <div className="text-right text-xs font-mono">
            <div className="font-bold text-slate-900">{report.report_id}</div>
            <div className="text-slate-500 text-[11px]">Generated: {report.generated_at}</div>
            <div className="text-[10px] font-bold text-red-600 uppercase mt-1">
              {report.classification}
            </div>
          </div>
        </div>

        {/* Mandatory Disclaimer Box */}
        <div className="p-3 bg-amber-50 border-l-4 border-amber-600 text-[11px] text-amber-950 leading-relaxed font-medium">
          <strong>LEGAL & SCIENTIFIC NOTICE:</strong> {report.disclaimer}
        </div>

        {/* Section 1: Alert Summary */}
        <div className="space-y-2">
          <h2 className="text-xs font-bold uppercase tracking-wider text-slate-900 border-b border-slate-200 pb-1">
            1. Anomaly Identification & Status
          </h2>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs bg-slate-50 p-3 rounded-lg border border-slate-200">
            <div>
              <span className="text-slate-500 font-medium block">Alert Reference:</span>
              <span className="font-mono font-bold text-slate-900">{report.alert_header.alert_id}</span>
            </div>
            <div>
              <span className="text-slate-500 font-medium block">Risk Score:</span>
              <span className="font-mono font-extrabold text-red-600 text-sm">{report.alert_header.risk_score}</span>
            </div>
            <div>
              <span className="text-slate-500 font-medium block">Priority Level:</span>
              <span className="font-bold text-red-700">{report.alert_header.priority}</span>
            </div>
            <div>
              <span className="text-slate-500 font-medium block">Current Status:</span>
              <span className="font-bold text-slate-800">{report.alert_header.status}</span>
            </div>
          </div>
        </div>

        {/* Section 2: Geographic & Cadastral Boundary Analysis */}
        <div className="space-y-2">
          <h2 className="text-xs font-bold uppercase tracking-wider text-slate-900 border-b border-slate-200 pb-1">
            2. Geographic & Cadastral Boundary Intersection
          </h2>
          <table className="w-full text-xs border border-slate-200 divide-y divide-slate-200">
            <tbody className="divide-y divide-slate-200">
              <tr className="bg-slate-50">
                <td className="p-2 font-semibold text-slate-600 w-1/3">Administrative Sector</td>
                <td className="p-2 font-bold text-slate-900">{report.geographic_location.district}, {report.geographic_location.state}</td>
              </tr>
              <tr>
                <td className="p-2 font-semibold text-slate-600">Site Coordinates</td>
                <td className="p-2 font-mono">{report.geographic_location.latitude}, {report.geographic_location.longitude}</td>
              </tr>
              <tr className="bg-slate-50">
                <td className="p-2 font-semibold text-slate-600">Total Disturbed Surface Area</td>
                <td className="p-2 font-mono font-bold text-slate-900">{report.geographic_location.disturbed_area_ha}</td>
              </tr>
              <tr>
                <td className="p-2 font-semibold text-slate-600">Nearest Registered Lease</td>
                <td className="p-2 font-medium">{report.geographic_location.nearest_lease_id} ({report.geographic_location.lease_name})</td>
              </tr>
              <tr className="bg-slate-50">
                <td className="p-2 font-semibold text-slate-600">Boundary Relationship</td>
                <td className="p-2 font-bold text-red-700">{report.geographic_location.lease_relationship} ({report.geographic_location.distance_from_boundary})</td>
              </tr>
            </tbody>
          </table>
        </div>

        {/* Section 3: Satellite Multi-Sensor Evidence */}
        <div className="space-y-2">
          <h2 className="text-xs font-bold uppercase tracking-wider text-slate-900 border-b border-slate-200 pb-1">
            3. Satellite Multi-Sensor Observations (2022 - 2026)
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs bg-slate-50 p-3 rounded-lg border border-slate-200">
            <div>
              <span className="text-slate-500 font-medium block">Optical Vegetation Drop:</span>
              <span className="font-bold text-rose-700">{report.satellite_evidence.vegetation_loss}</span>
            </div>
            <div>
              <span className="text-slate-500 font-medium block">Bare Soil Expansion:</span>
              <span className="font-bold text-amber-800">{report.satellite_evidence.bare_soil_increase}</span>
            </div>
            <div>
              <span className="text-slate-500 font-medium block">SAR Radar Anomaly:</span>
              <span className="font-bold text-indigo-700">{report.satellite_evidence.radar_backscatter_anomaly}</span>
            </div>
          </div>
        </div>

        {/* Section 4: AI Disturbance Semantic Segmentation */}
        <div className="space-y-2">
          <h2 className="text-xs font-bold uppercase tracking-wider text-slate-900 border-b border-slate-200 pb-1">
            4. AI Disturbance Semantic Classification & Predictive Forecast
          </h2>
          <div className="grid grid-cols-2 gap-2 text-xs">
            {report.ai_and_gis_evidence.segmentation_classes.map((cls: any, i: number) => (
              <div key={i} className="p-2 bg-slate-50 border border-slate-200 rounded flex justify-between font-medium">
                <span>{cls.class}:</span>
                <span className="font-mono font-bold text-slate-900">{cls.area_ha}</span>
              </div>
            ))}
          </div>
          <div className="p-2.5 bg-blue-50 border border-blue-200 rounded text-xs text-blue-900 italic">
            <strong>Predictive Trajectory:</strong> {report.ai_and_gis_evidence.predictive_expansion_forecast}
          </div>
        </div>

        {/* Section 5: Verification & Action Directive */}
        <div className="space-y-2">
          <h2 className="text-xs font-bold uppercase tracking-wider text-slate-900 border-b border-slate-200 pb-1">
            5. Human-in-the-Loop Ground Verification & Directive
          </h2>
          <div className="space-y-2 text-xs">
            <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
              <div className="font-bold text-slate-800 mb-1">Recommended Enforcement Action:</div>
              <p className="text-slate-700">{report.recommended_action}</p>
            </div>
            <div className="text-slate-600">
              <strong>Assigned Officer:</strong> {report.assigned_officer}
            </div>
          </div>
        </div>

        {/* Signature Box */}
        <div className="pt-8 border-t border-slate-300 flex justify-between items-end text-xs text-slate-600">
          <div>
            <div>System Seal: <strong>ILLEGAL MINING DETECTION BY USING SATELLITE DATA</strong></div>
            <div className="text-[10px] text-slate-400">Cryptographic Hash: SHA256-IMD90421-2026</div>
          </div>
          <div className="text-center">
            <div className="border-b border-slate-400 w-48 mb-1"></div>
            <div>Authorized Officer Signature</div>
          </div>
        </div>
      </div>
    </div>
  );
};
