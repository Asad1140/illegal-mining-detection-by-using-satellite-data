import React, { useState, useEffect } from 'react';
import { useApp } from '../context/AppContext';
import { apiClient } from '../api/client';
import { Alert, VerificationRecord } from '../types';
import { RiskBadge } from '../components/common/RiskBadge';
import { StatusBadge } from '../components/common/StatusBadge';
import { BeforeAfterSlider } from '../components/imagery/BeforeAfterSlider';
import { SpectralIndexViewer } from '../components/imagery/SpectralIndexViewer';
import { FeatureContributionBar } from '../components/charts/FeatureContributionBar';
import {
  ShieldAlert,
  MapPin,
  Calendar,
  Layers,
  CheckCircle2,
  AlertTriangle,
  Clock,
  ArrowLeft,
  FileText,
  UserCheck,
  Send,
  Navigation,
  ExternalLink,
  Cpu,
  Info
} from 'lucide-react';

export const AlertDetailsPage: React.FC = () => {
  const { activeAlertId, setCurrentPage } = useApp();
  const [alert, setAlert] = useState<Alert | null>(null);
  const [verifications, setVerifications] = useState<VerificationRecord[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  // Field Verification Form State
  const [newStatus, setNewStatus] = useState<string>('VERIFIED');
  const [comments, setComments] = useState<string>('');
  const [gpsMatch, setGpsMatch] = useState<string>('21.8523, 85.5932');
  const [evidenceNotes, setEvidenceNotes] = useState<string>('Boundary survey confirmed opencast excavation beyond Lease ML-KE-01 pillar.');
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [feedbackSuccess, setFeedbackSuccess] = useState<boolean>(false);

  useEffect(() => {
    if (!activeAlertId) return;
    setLoading(true);
    apiClient
      .getAlertById(activeAlertId)
      .then((data) => {
        setAlert(data);
        return apiClient.getVerificationHistory(activeAlertId);
      })
      .then((records) => {
        setVerifications(records);
        setLoading(false);
      })
      .catch((err) => {
        console.error('Failed to load alert details:', err);
        setLoading(false);
      });
  }, [activeAlertId]);

  const handleSubmitVerification = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!alert) return;
    setIsSubmitting(true);
    try {
      const rec = await apiClient.submitVerification({
        alert_id: alert.id,
        status: newStatus,
        comments: comments || `Field officer conducted ground validation for Alert ${alert.id}. Status updated to ${newStatus}.`,
        gps_coordinates: gpsMatch,
        evidence_notes: evidenceNotes
      });
      setVerifications([rec, ...verifications]);
      setAlert({ ...alert, status: newStatus as any });
      setFeedbackSuccess(true);
      setTimeout(() => setFeedbackSuccess(false), 4000);
      setComments('');
    } catch (err) {
      console.error('Error submitting verification:', err);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (loading || !alert) {
    return (
      <div className="flex items-center justify-center p-12 text-slate-500">
        <div className="w-6 h-6 border-2 border-blue-600 border-t-transparent rounded-full animate-spin mr-3"></div>
        <span className="text-sm font-semibold">Loading Alert Dossier & Multi-Sensor Evidence...</span>
      </div>
    );
  }

  return (
    <div className="space-y-6 pb-16">
      {/* Top Breadcrumb & Navigation */}
      <div className="flex flex-wrap items-center justify-between gap-3">
        <button
          onClick={() => setCurrentPage('alerts')}
          className="flex items-center gap-1.5 text-xs font-bold text-slate-600 hover:text-slate-900 bg-white px-3 py-1.5 rounded-lg border border-slate-200 shadow-xs transition"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Back to Alerts List</span>
        </button>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setCurrentPage('reports')}
            className="flex items-center gap-1.5 bg-slate-900 hover:bg-slate-800 text-white px-3.5 py-1.5 rounded-lg text-xs font-bold transition shadow-xs"
          >
            <FileText className="w-3.5 h-3.5 text-blue-400" />
            <span>Generate Executive Report</span>
          </button>
        </div>
      </div>

      {/* A. Alert Header Card */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-5 space-y-4">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="font-mono text-sm font-extrabold text-blue-600 bg-blue-50 px-2 py-0.5 rounded border border-blue-200">
                {alert.id}
              </span>
              <span className="text-xs font-bold text-slate-400">&bull;</span>
              <span className="text-xs font-semibold text-slate-500">
                Detected: {alert.first_detected} &rarr; {alert.last_detected}
              </span>
              <span className="text-xs font-bold text-slate-400">&bull;</span>
              <span className="text-xs font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                Confidence: {Math.round(alert.confidence * 100)}%
              </span>
            </div>
            <h1 className="text-xl font-extrabold text-slate-900">{alert.title}</h1>
            <p className="text-xs text-slate-500 flex items-center gap-1.5">
              <MapPin className="w-3.5 h-3.5 text-red-500" />
              <span>{alert.district}, {alert.state} &bull; {alert.location_name} (Lat: {alert.latitude}, Lng: {alert.longitude})</span>
            </p>
          </div>

          <div className="flex flex-col items-end gap-2">
            <RiskBadge level={alert.priority} score={alert.risk_score} />
            <StatusBadge status={alert.status} />
          </div>
        </div>

        {/* Spatial & Physical Attributes Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-3 border-t border-slate-100 text-xs">
          <div className="bg-slate-50 p-2.5 rounded-lg border border-slate-200">
            <span className="text-[10px] uppercase font-bold text-slate-400">Disturbed Area</span>
            <div className="font-mono text-base font-extrabold text-slate-900">{alert.disturbed_area_ha} ha</div>
          </div>
          <div className="bg-slate-50 p-2.5 rounded-lg border border-slate-200">
            <span className="text-[10px] uppercase font-bold text-slate-400">Lease Relationship</span>
            <div className="font-bold text-red-700 text-xs mt-0.5">{alert.lease_status}</div>
          </div>
          <div className="bg-slate-50 p-2.5 rounded-lg border border-slate-200">
            <span className="text-[10px] uppercase font-bold text-slate-400">Distance from Lease</span>
            <div className="font-mono text-base font-extrabold text-slate-900">{alert.distance_from_lease_m} m</div>
          </div>
          <div className="bg-slate-50 p-2.5 rounded-lg border border-slate-200">
            <span className="text-[10px] uppercase font-bold text-slate-400">Assigned Enforcement Officer</span>
            <div className="font-semibold text-slate-800 truncate mt-0.5">{alert.assigned_officer}</div>
          </div>
        </div>
      </div>

      {/* Satellite Evidence Section: Split-Screen Slider + Spectral Index Viewer */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        <div>
          <h3 className="text-sm font-bold text-slate-800 mb-2 flex items-center gap-2">
            <Layers className="w-4 h-4 text-blue-600" />
            <span>Satellite Temporal Observation (2022 vs 2026)</span>
          </h3>
          <BeforeAfterSlider />
        </div>
        <div>
          <h3 className="text-sm font-bold text-slate-800 mb-2 flex items-center gap-2">
            <Cpu className="w-4 h-4 text-blue-600" />
            <span>Multispectral Indices & Radar Anomaly</span>
          </h3>
          <SpectralIndexViewer />
        </div>
      </div>

      {/* AI Disturbance Semantic Segmentation (12 Classes) + Risk Explainability */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        {/* Left: AI 12-Class Segmentation */}
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-4 space-y-3">
          <div className="flex items-center justify-between pb-2 border-b border-slate-100">
            <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
              <Layers className="w-4 h-4 text-purple-600" />
              <span>AI Disturbance Multi-Class Segmentation</span>
            </h3>
            <span className="text-[11px] font-bold text-purple-700 bg-purple-50 px-2 py-0.5 rounded border border-purple-200">
              U-Net / SegFormer Model
            </span>
          </div>

          <p className="text-xs text-slate-500">
            Surface land-cover classification across the 14.2 ha anomaly footprint:
          </p>

          <div className="space-y-2 text-xs">
            <div className="flex justify-between items-center bg-red-50 p-2 rounded border border-red-200">
              <span className="font-semibold text-red-900 flex items-center gap-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-red-600"></span> Active Extraction Mining Pit (Class 7)
              </span>
              <span className="font-mono font-bold text-red-950">5.47 ha (38.5%)</span>
            </div>

            <div className="flex justify-between items-center bg-amber-50 p-2 rounded border border-amber-200">
              <span className="font-semibold text-amber-900 flex items-center gap-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-orange-500"></span> Overburden Dump & Waste Spoil (Class 8)
              </span>
              <span className="font-mono font-bold text-amber-950">3.44 ha (24.2%)</span>
            </div>

            <div className="flex justify-between items-center bg-rose-50 p-2 rounded border border-rose-200">
              <span className="font-semibold text-rose-900 flex items-center gap-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-rose-600"></span> Forest Canopy Clearance (Class 11)
              </span>
              <span className="font-mono font-bold text-rose-950">2.39 ha (16.8%)</span>
            </div>

            <div className="flex justify-between items-center bg-yellow-50 p-2 rounded border border-yellow-200">
              <span className="font-semibold text-yellow-900 flex items-center gap-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-yellow-600"></span> Exposed Bare Land (Class 3)
              </span>
              <span className="font-mono font-bold text-yellow-950">1.49 ha (10.5%)</span>
            </div>

            <div className="flex justify-between items-center bg-slate-50 p-2 rounded border border-slate-200">
              <span className="font-semibold text-slate-800 flex items-center gap-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-slate-500"></span> Haulage Road & Infrastructure (Class 5)
              </span>
              <span className="font-mono font-bold text-slate-900">0.74 ha (5.2%)</span>
            </div>
          </div>
        </div>

        {/* Right: Explainable AI Risk Score Breakdown */}
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-4 space-y-3">
          <div className="flex items-center justify-between pb-2 border-b border-slate-100">
            <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
              <ShieldAlert className="w-4 h-4 text-red-600" />
              <span>Explainable AI Risk Factor Decomposition</span>
            </h3>
            <span className="font-mono font-extrabold text-sm text-red-600">
              {alert.risk_score}/100 Risk
            </span>
          </div>

          {alert.risk_factors && <FeatureContributionBar factors={alert.risk_factors} />}

          {/* Evidence Summary Text */}
          <div className="p-3 bg-slate-50 rounded-lg border border-slate-200 text-xs text-slate-700 space-y-1.5">
            <div className="font-bold text-slate-900 flex items-center gap-1.5">
              <Info className="w-3.5 h-3.5 text-blue-600" />
              <span>Evidence Summary & Rationale</span>
            </div>
            <p className="leading-relaxed">{alert.explanation_summary}</p>
          </div>
        </div>
      </div>

      {/* Human-in-the-Loop Field Verification & Audit History Section */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-5 space-y-4">
        <div className="flex items-center justify-between pb-3 border-b border-slate-200">
          <div>
            <h3 className="text-base font-extrabold text-slate-900 flex items-center gap-2">
              <UserCheck className="w-5 h-5 text-blue-600" />
              <span>Human-in-the-Loop Field Verification & Enforcement Action</span>
            </h3>
            <p className="text-xs text-slate-500">
              Authorized ground validation workflow by District Mining Officer. Stored feedback trains future model cycles.
            </p>
          </div>
          {feedbackSuccess && (
            <span className="text-xs font-bold text-emerald-700 bg-emerald-50 border border-emerald-300 px-3 py-1 rounded-lg flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              Verification Record Successfully Saved!
            </span>
          )}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
          {/* Submission Form */}
          <form onSubmit={handleSubmitVerification} className="lg:col-span-1 space-y-3 bg-slate-50 p-4 rounded-xl border border-slate-200 text-xs">
            <div className="font-bold text-slate-900">Record Field Inspection Finding</div>

            <div>
              <label className="block font-semibold text-slate-700 mb-1">Enforcement Decision / Status</label>
              <select
                value={newStatus}
                onChange={(e) => setNewStatus(e.target.value)}
                className="w-full bg-white border border-slate-300 rounded-lg p-2 font-semibold text-slate-900 focus:outline-none focus:border-blue-500"
              >
                <option value="VERIFIED">Ground Verified (Encroachment Confirmed)</option>
                <option value="FIELD_VERIFICATION">Field Inspection In Progress</option>
                <option value="UNDER_REVIEW">Under Technical Review</option>
                <option value="FALSE_POSITIVE">False Positive (Permitted Activity)</option>
                <option value="REJECTED">Rejected (No Disturbance Found)</option>
              </select>
            </div>

            <div>
              <label className="block font-semibold text-slate-700 mb-1">GPS Ground Coordinates</label>
              <input
                type="text"
                value={gpsMatch}
                onChange={(e) => setGpsMatch(e.target.value)}
                className="w-full bg-white border border-slate-300 rounded-lg p-2 font-mono text-slate-900"
                placeholder="21.8523, 85.5932"
              />
            </div>

            <div>
              <label className="block font-semibold text-slate-700 mb-1">Officer Inspection Notes</label>
              <textarea
                value={comments}
                onChange={(e) => setComments(e.target.value)}
                rows={3}
                className="w-full bg-white border border-slate-300 rounded-lg p-2 text-slate-900"
                placeholder="Enter physical inspection findings, boundary pillar marks, machinery count..."
              />
            </div>

            <button
              type="submit"
              disabled={isSubmitting}
              className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-bold py-2 px-3 rounded-lg shadow-sm flex items-center justify-center gap-2 transition"
            >
              <Send className="w-3.5 h-3.5" />
              <span>{isSubmitting ? 'Saving Inspection...' : 'Submit Verification & Update Alert'}</span>
            </button>
          </form>

          {/* Chronological Audit Trail */}
          <div className="lg:col-span-2 space-y-2.5">
            <div className="font-bold text-xs text-slate-700 uppercase tracking-wider">
              Enforcement Audit Trail ({verifications.length} Entries)
            </div>

            <div className="space-y-2.5 max-h-72 overflow-y-auto pr-1 custom-scrollbar">
              {verifications.map((v, idx) => (
                <div key={v.id || idx} className="p-3 bg-white rounded-lg border border-slate-200 shadow-xs space-y-1.5 text-xs">
                  <div className="flex items-center justify-between">
                    <span className="font-semibold text-slate-900">{v.verified_by}</span>
                    <StatusBadge status={v.status} />
                  </div>
                  <p className="text-slate-600 italic">"{v.comments}"</p>
                  <div className="flex flex-wrap items-center justify-between text-[11px] text-slate-400 pt-1 border-t border-slate-100">
                    <span>GPS: {v.gps_coordinates || '21.8523, 85.5932'}</span>
                    <span>{new Date(v.timestamp).toLocaleString()}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
