import React, { useState, useEffect } from 'react';
import { useApp } from '../context/AppContext';
import { apiClient } from '../api/client';
import { RiskBadge } from '../components/common/RiskBadge';
import { StatusBadge } from '../components/common/StatusBadge';
import {
  CheckSquare,
  Search,
  Filter,
  UserCheck,
  MapPin,
  Send,
  Camera,
  CheckCircle2,
  AlertOctagon,
  Clock
} from 'lucide-react';

export const FieldVerificationPage: React.FC = () => {
  const { navigateToAlert } = useApp();
  const [queue, setQueue] = useState<any[]>([]);
  const [filterStatus, setFilterStatus] = useState<string>('ALL');
  const [loading, setLoading] = useState<boolean>(true);
  const [activeAlert, setActiveAlert] = useState<any | null>(null);

  // Form State
  const [formStatus, setFormStatus] = useState<string>('VERIFIED');
  const [comments, setComments] = useState<string>('');
  const [gps, setGps] = useState<string>('21.8523, 85.5932');
  const [notes, setNotes] = useState<string>('Boundary survey confirmed opencast excavation beyond Lease ML-KE-01 pillar.');
  const [submitting, setSubmitting] = useState<boolean>(false);
  const [success, setSuccess] = useState<boolean>(false);

  const loadQueue = () => {
    setLoading(true);
    apiClient
      .getVerificationQueue(filterStatus)
      .then((data) => {
        setQueue(data);
        if (data.length > 0 && !activeAlert) {
          setActiveAlert(data[0]);
        }
        setLoading(false);
      })
      .catch((err) => {
        console.error('Failed to load queue:', err);
        setLoading(false);
      });
  };

  useEffect(() => {
    loadQueue();
  }, [filterStatus]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!activeAlert) return;
    setSubmitting(true);
    try {
      await apiClient.submitVerification({
        alert_id: activeAlert.alert_id,
        status: formStatus,
        comments: comments || `Field Officer marked Alert ${activeAlert.alert_id} as ${formStatus}.`,
        gps_coordinates: gps,
        evidence_notes: notes
      });
      setSuccess(true);
      setTimeout(() => setSuccess(false), 3500);
      setComments('');
      loadQueue();
    } catch (err) {
      console.error('Verification submit error:', err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="space-y-6 pb-16">
      {/* Header */}
      <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-blue-50 text-blue-600 rounded-lg">
            <CheckSquare className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-extrabold text-slate-900 flex items-center gap-2">
              <span>Human-in-the-Loop Ground Verification Portal</span>
              <span className="text-xs font-bold text-amber-700 bg-amber-50 px-2 py-0.5 rounded border border-amber-200">
                {queue.length} Cases in Queue
              </span>
            </h2>
            <p className="text-xs text-slate-500">
              Field Officer decision workflow, GPS coordinate verification, and feedback loop for continuous model improvement.
            </p>
          </div>
        </div>

        {/* Filter */}
        <div className="flex items-center gap-2 bg-slate-50 px-3 py-1.5 rounded-lg border border-slate-200 text-xs">
          <Filter className="w-3.5 h-3.5 text-slate-400" />
          <span className="font-semibold text-slate-700">Filter Queue:</span>
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="bg-transparent font-semibold text-slate-800 focus:outline-none cursor-pointer"
          >
            <option value="ALL">All Statuses</option>
            <option value="PENDING">Pending Verification</option>
            <option value="FIELD_VERIFICATION">Field Verification Active</option>
            <option value="UNDER_REVIEW">Under Review</option>
            <option value="VERIFIED">Ground Verified</option>
          </select>
        </div>
      </div>

      {/* Main Verification Workflow Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        {/* Left: Queue List (1 col) */}
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-4 space-y-3">
          <div className="flex items-center justify-between pb-2 border-b border-slate-100">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500">
              Surveillance Queue
            </h3>
            <span className="text-[11px] font-mono text-slate-400">Sort: Priority Risk</span>
          </div>

          <div className="space-y-2 max-h-[580px] overflow-y-auto pr-1 custom-scrollbar">
            {queue.map((item) => {
              const isSelected = activeAlert?.alert_id === item.alert_id;
              return (
                <div
                  key={item.alert_id}
                  onClick={() => setActiveAlert(item)}
                  className={`p-3 rounded-lg border cursor-pointer transition space-y-1.5 ${
                    isSelected
                      ? 'bg-blue-50/80 border-blue-500 shadow-xs'
                      : 'bg-white hover:bg-slate-50 border-slate-200'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="font-mono font-bold text-xs text-slate-900">{item.alert_id}</span>
                    <RiskBadge level={item.priority} score={item.risk_score} showScore={true} />
                  </div>
                  <div className="text-xs font-semibold text-slate-800 line-clamp-1">{item.title}</div>
                  <div className="flex items-center justify-between text-[11px] text-slate-500">
                    <span>{item.district}, {item.state}</span>
                    <StatusBadge status={item.status} />
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right: Active Case Ground Inspection Form (2 cols) */}
        {activeAlert ? (
          <div className="lg:col-span-2 bg-white rounded-xl border border-slate-200 shadow-sm p-5 space-y-5">
            <div className="flex flex-wrap items-start justify-between gap-3 pb-3 border-b border-slate-200">
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-mono font-extrabold text-sm text-blue-600 bg-blue-50 px-2 py-0.5 rounded border border-blue-200">
                    {activeAlert.alert_id}
                  </span>
                  <StatusBadge status={activeAlert.status} />
                </div>
                <h3 className="text-base font-bold text-slate-900 mt-1">{activeAlert.title}</h3>
                <p className="text-xs text-slate-500 flex items-center gap-1.5 mt-0.5">
                  <MapPin className="w-3.5 h-3.5 text-red-500" />
                  <span>{activeAlert.district}, {activeAlert.state} &bull; Area: {activeAlert.disturbed_area_ha} ha &bull; {activeAlert.lease_status}</span>
                </p>
              </div>

              <button
                onClick={() => navigateToAlert(activeAlert.alert_id)}
                className="text-xs font-bold text-blue-600 hover:text-blue-700 bg-blue-50 px-3 py-1.5 rounded-lg border border-blue-200 transition"
              >
                Open Full Evidence Dossier &rarr;
              </button>
            </div>

            {success && (
              <div className="p-3 bg-emerald-50 border border-emerald-300 rounded-lg text-emerald-800 text-xs font-bold flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                Ground verification finding recorded successfully! Model feedback stored.
              </div>
            )}

            {/* Inspection Form */}
            <form onSubmit={handleSubmit} className="space-y-4 text-xs">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block font-bold text-slate-700 mb-1">
                    Officer Ground Decision Status
                  </label>
                  <select
                    value={formStatus}
                    onChange={(e) => setFormStatus(e.target.value)}
                    className="w-full bg-slate-50 border border-slate-300 rounded-lg p-2.5 font-semibold text-slate-900 focus:outline-none focus:border-blue-500"
                  >
                    <option value="VERIFIED">Ground Verified (Encroachment Confirmed)</option>
                    <option value="FIELD_VERIFICATION">Field Inspection In Progress</option>
                    <option value="UNDER_REVIEW">Under Technical Review</option>
                    <option value="FALSE_POSITIVE">False Positive (Permitted Area)</option>
                    <option value="REJECTED">Rejected (No Physical Disturbance)</option>
                  </select>
                </div>

                <div>
                  <label className="block font-bold text-slate-700 mb-1">
                    Handheld DGPS Ground Coordinates
                  </label>
                  <input
                    type="text"
                    value={gps}
                    onChange={(e) => setGps(e.target.value)}
                    className="w-full bg-slate-50 border border-slate-300 rounded-lg p-2.5 font-mono text-slate-900"
                    placeholder="21.8523, 85.5932"
                  />
                </div>
              </div>

              <div>
                <label className="block font-bold text-slate-700 mb-1">
                  Enforcement Field Notes & Evidence Summary
                </label>
                <textarea
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  rows={3}
                  className="w-full bg-slate-50 border border-slate-300 rounded-lg p-2.5 text-slate-900"
                  placeholder="Record boundary pillar numbers, presence of earthmoving machinery, depth of pit..."
                />
              </div>

              <div>
                <label className="block font-bold text-slate-700 mb-1">
                  Officer Inspection Comments & Recommendations
                </label>
                <textarea
                  value={comments}
                  onChange={(e) => setComments(e.target.value)}
                  rows={2}
                  className="w-full bg-slate-50 border border-slate-300 rounded-lg p-2.5 text-slate-900"
                  placeholder="Enter official action recommendation (e.g., notice under MMDR Act)..."
                />
              </div>

              <div className="bg-slate-50 p-3 rounded-lg border border-slate-200 flex items-center justify-between">
                <div className="flex items-center gap-2 text-slate-600">
                  <Camera className="w-4 h-4 text-slate-500" />
                  <span className="font-semibold">Geotagged Photo Evidence:</span>
                  <span className="text-slate-400">1 inspection photo attached (Demo Simulation)</span>
                </div>
                <span className="text-[11px] font-bold text-emerald-700 bg-emerald-100 px-2 py-0.5 rounded">
                  GPS Attached
                </span>
              </div>

              <button
                type="submit"
                disabled={submitting}
                className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-bold py-2.5 px-4 rounded-lg shadow-sm flex items-center justify-center gap-2 text-sm transition"
              >
                <Send className="w-4 h-4" />
                <span>{submitting ? 'Submitting Ground Record...' : 'Submit Verification & Update Alert Lifecycle'}</span>
              </button>
            </form>
          </div>
        ) : (
          <div className="lg:col-span-2 bg-white rounded-xl border border-slate-200 p-12 text-center text-slate-500">
            Select a case from the queue to start field verification.
          </div>
        )}
      </div>
    </div>
  );
};
