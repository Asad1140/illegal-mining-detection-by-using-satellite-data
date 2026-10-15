import React, { useState, useEffect } from 'react';
import { useApp } from '../context/AppContext';
import { apiClient } from '../api/client';
import { Alert } from '../types';
import { RiskBadge } from '../components/common/RiskBadge';
import { StatusBadge } from '../components/common/StatusBadge';
import {
  AlertOctagon,
  Search,
  Filter,
  ArrowUpDown,
  Download,
  Flame,
  FileSpreadsheet
} from 'lucide-react';

export const AlertsPage: React.FC = () => {
  const { selectedRegion, navigateToAlert } = useApp();
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  // Filters
  const [filterPriority, setFilterPriority] = useState<string>('ALL');
  const [filterStatus, setFilterStatus] = useState<string>('ALL');
  const [sortBy, setSortBy] = useState<string>('risk_score');
  const [searchTerm, setSearchTerm] = useState<string>('');

  useEffect(() => {
    setLoading(true);
    apiClient
      .getAlerts({
        district: selectedRegion === 'ALL' ? undefined : selectedRegion,
        priority: filterPriority,
        status: filterStatus,
        sort_by: sortBy
      })
      .then((data) => {
        setAlerts(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error('Failed to load alerts:', err);
        setLoading(false);
      });
  }, [selectedRegion, filterPriority, filterStatus, sortBy]);

  const filteredAlerts = alerts.filter(
    (a) =>
      a.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
      a.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      a.location_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      a.assigned_officer.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const exportCSV = () => {
    const headers = ['Alert ID', 'Title', 'District', 'Risk Score', 'Priority', 'Area (ha)', 'Lease Status', 'Distance (m)', 'Status', 'Last Detected'];
    const rows = filteredAlerts.map(a => [
      a.id,
      `"${a.title}"`,
      a.district,
      a.risk_score,
      a.priority,
      a.disturbed_area_ha,
      `"${a.lease_status}"`,
      a.distance_from_lease_m,
      a.status,
      a.last_detected
    ]);
    const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows.map(e => e.join(','))].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `imd_alerts_${selectedRegion}_${Date.now()}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-red-50 text-red-600 rounded-lg">
            <AlertOctagon className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-extrabold text-slate-900 flex items-center gap-2">
              <span>Potential Unauthorized Mining Surveillance Alerts</span>
              <span className="text-xs font-bold text-red-700 bg-red-50 px-2 py-0.5 rounded border border-red-200">
                {filteredAlerts.length} Active Records
              </span>
            </h2>
            <p className="text-xs text-slate-500">
              Explainable multi-sensor early warning alerts requiring human field verification.
            </p>
          </div>
        </div>

        <button
          onClick={exportCSV}
          className="flex items-center gap-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 px-3 py-1.5 rounded-lg text-xs font-bold transition border border-slate-300 shadow-xs"
        >
          <FileSpreadsheet className="w-3.5 h-3.5 text-emerald-600" />
          <span>Export CSV Dossier</span>
        </button>
      </div>

      {/* Filter & Search Bar */}
      <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm flex flex-wrap items-center justify-between gap-3 text-xs">
        <div className="flex flex-wrap items-center gap-2.5">
          {/* Search */}
          <div className="relative w-64">
            <Search className="w-3.5 h-3.5 absolute left-2.5 top-2.5 text-slate-400" />
            <input
              type="text"
              placeholder="Search alert, officer, site..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full bg-slate-50 border border-slate-200 rounded-lg pl-8 pr-3 py-1.5 text-xs text-slate-800 focus:outline-none focus:border-blue-500"
            />
          </div>

          {/* Priority filter */}
          <div className="flex items-center gap-1.5 bg-slate-50 px-2.5 py-1.5 rounded-lg border border-slate-200">
            <Filter className="w-3.5 h-3.5 text-slate-400" />
            <span className="text-slate-500 font-medium">Risk:</span>
            <select
              value={filterPriority}
              onChange={(e) => setFilterPriority(e.target.value)}
              className="bg-transparent font-semibold text-slate-800 focus:outline-none cursor-pointer"
            >
              <option value="ALL">All Levels</option>
              <option value="CRITICAL">Critical (&gt;= 75)</option>
              <option value="HIGH">High (50-74)</option>
              <option value="MEDIUM">Medium (25-49)</option>
              <option value="LOW">Low (0-24)</option>
            </select>
          </div>

          {/* Status filter */}
          <div className="flex items-center gap-1.5 bg-slate-50 px-2.5 py-1.5 rounded-lg border border-slate-200">
            <span className="text-slate-500 font-medium">Status:</span>
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
              <option value="FALSE_POSITIVE">False Positive</option>
            </select>
          </div>
        </div>

        {/* Sort by */}
        <div className="flex items-center gap-1.5 bg-slate-50 px-2.5 py-1.5 rounded-lg border border-slate-200">
          <ArrowUpDown className="w-3.5 h-3.5 text-slate-400" />
          <span className="text-slate-500 font-medium">Sort:</span>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="bg-transparent font-semibold text-slate-800 focus:outline-none cursor-pointer"
          >
            <option value="risk_score">Highest Risk Score</option>
            <option value="disturbed_area_ha">Largest Disturbed Area</option>
            <option value="last_detected">Newest Observation</option>
          </select>
        </div>
      </div>

      {/* Alerts Table */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-700">
            <thead className="bg-slate-100/70 text-slate-600 font-bold uppercase tracking-wider border-b border-slate-200">
              <tr>
                <th className="p-3.5">Alert ID</th>
                <th className="p-3.5">Title & Site Location</th>
                <th className="p-3.5">Risk Score</th>
                <th className="p-3.5">Disturbed Area</th>
                <th className="p-3.5">Lease Relationship</th>
                <th className="p-3.5">Distance</th>
                <th className="p-3.5">Last Detected</th>
                <th className="p-3.5">Status</th>
                <th className="p-3.5">Assigned Officer</th>
                <th className="p-3.5 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200">
              {filteredAlerts.map((alert) => (
                <tr key={alert.id} className="hover:bg-slate-50/80 transition">
                  <td className="p-3.5 font-mono font-bold text-slate-900">{alert.id}</td>
                  <td className="p-3.5 max-w-xs">
                    <div className="font-semibold text-slate-900">{alert.title}</div>
                    <div className="text-[11px] text-slate-400">
                      {alert.district}, {alert.state} &bull; {alert.location_name}
                    </div>
                  </td>
                  <td className="p-3.5">
                    <RiskBadge level={alert.priority} score={alert.risk_score} />
                  </td>
                  <td className="p-3.5 font-mono font-bold text-slate-900">{alert.disturbed_area_ha} ha</td>
                  <td className="p-3.5">
                    <span
                      className={`font-semibold text-[11px] ${
                        alert.lease_status.includes('Outside')
                          ? 'text-red-700 font-bold'
                          : alert.lease_status.includes('Buffer')
                          ? 'text-amber-700 font-bold'
                          : 'text-emerald-700 font-bold'
                      }`}
                    >
                      {alert.lease_status}
                    </span>
                  </td>
                  <td className="p-3.5 font-mono">{alert.distance_from_lease_m} m</td>
                  <td className="p-3.5 font-mono text-slate-600">{alert.last_detected}</td>
                  <td className="p-3.5">
                    <StatusBadge status={alert.status} />
                  </td>
                  <td className="p-3.5 text-slate-600 font-medium">{alert.assigned_officer}</td>
                  <td className="p-3.5 text-right">
                    <button
                      onClick={() => navigateToAlert(alert.id)}
                      className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1.5 rounded-lg text-xs font-bold shadow-xs transition"
                    >
                      View Dossier
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
