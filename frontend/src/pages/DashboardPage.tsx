import React, { useEffect, useState } from 'react';
import { useApp } from '../context/AppContext';
import { apiClient } from '../api/client';
import { DashboardStats, Alert } from '../types';
import { StatCard } from '../components/common/StatCard';
import { RiskBadge } from '../components/common/RiskBadge';
import { StatusBadge } from '../components/common/StatusBadge';
import { RiskDonutChart } from '../components/charts/RiskDonutChart';
import { DisturbanceTrendChart } from '../components/charts/DisturbanceTrendChart';
import { DistrictAlertsBarChart } from '../components/charts/DistrictAlertsBarChart';
import { GisMap } from '../components/map/GisMap';
import {
  MapPin,
  AlertTriangle,
  Flame,
  CheckCircle2,
  Clock,
  Layers,
  ArrowUpRight,
  ShieldCheck,
  Radio,
  FileText
} from 'lucide-react';

export const DashboardPage: React.FC = () => {
  const { selectedRegion, navigateToAlert, setCurrentPage } = useApp();
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [recentAlerts, setRecentAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    setLoading(true);
    Promise.all([
      apiClient.getDashboardStats(selectedRegion),
      apiClient.getAlerts({ district: selectedRegion, sort_by: 'risk_score' })
    ])
      .then(([statsData, alertsData]) => {
        setStats(statsData);
        setRecentAlerts(alertsData.slice(0, 5));
        setLoading(false);
      })
      .catch((err) => {
        console.error('Failed to load dashboard data:', err);
        setLoading(false);
      });
  }, [selectedRegion]);

  return (
    <div className="space-y-6 pb-12">
      {/* Top Banner Notice */}
      <div className="bg-gradient-to-r from-slate-900 via-blue-950 to-slate-900 border border-slate-800 rounded-xl p-4 text-white shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-3">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2 py-0.5 rounded bg-blue-500/20 text-blue-300 font-bold text-[11px] uppercase tracking-wider border border-blue-500/40">
              Surveillance Grid: {selectedRegion} Sector
            </span>
            <span className="text-xs text-slate-400">Sentinel-2 & Sentinel-1 Active Ingestion</span>
          </div>
          <h2 className="text-lg md:text-xl font-extrabold tracking-tight mt-1 text-white">
            Operational Mining Surveillance & Early-Warning Dashboard
          </h2>
        </div>
        <div className="flex items-center gap-2 shrink-0">
          <button
            onClick={() => setCurrentPage('risk-map')}
            className="flex items-center gap-1.5 bg-blue-600 hover:bg-blue-700 text-white px-3.5 py-1.5 rounded-lg text-xs font-bold transition shadow"
          >
            <Radio className="w-3.5 h-3.5" />
            <span>Open Full-Screen GIS Map</span>
          </button>
        </div>
      </div>

      {/* 6 Core Top KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        <StatCard
          title="Monitored Areas"
          value={stats?.total_monitored_areas || 128}
          subtitle="4 Major Mining Hubs"
          icon={MapPin}
          iconColor="text-blue-600 bg-blue-50"
        />
        <StatCard
          title="Active Alerts"
          value={stats?.active_alerts || 24}
          subtitle="Unresolved Anomaly Zones"
          icon={AlertTriangle}
          iconColor="text-amber-600 bg-amber-50"
          trend="+3 New"
          trendPositive={false}
        />
        <StatCard
          title="High Risk (>=75)"
          value={stats?.high_risk_alerts || 8}
          subtitle="Requires Priority Patrol"
          icon={Flame}
          iconColor="text-red-600 bg-red-50"
        />
        <StatCard
          title="Disturbed Area"
          value={`${stats?.potential_disturbed_area_ha || 184.6} ha`}
          subtitle="Cumulative Expansion"
          icon={Layers}
          iconColor="text-orange-600 bg-orange-50"
        />
        <StatCard
          title="Ground Verified"
          value={stats?.verified_cases || 11}
          subtitle="Officer Inspected Cases"
          icon={CheckCircle2}
          iconColor="text-emerald-600 bg-emerald-50"
          trend="45.8%"
          trendPositive={true}
        />
        <StatCard
          title="Pending Verification"
          value={stats?.pending_verification || 13}
          subtitle="In Review Queue"
          icon={Clock}
          iconColor="text-purple-600 bg-purple-50"
        />
      </div>

      {/* Embedded Live GIS Radar Map */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-4 space-y-3">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-blue-600" />
              <span>Interactive Surveillance Map ({selectedRegion} Sector)</span>
            </h3>
            <p className="text-xs text-slate-500">
              Live vector overlays: Registered Mining Leases, 500m Surveillance Buffer, and Detected Disturbances.
            </p>
          </div>
          <button
            onClick={() => setCurrentPage('risk-map')}
            className="text-xs font-bold text-blue-600 hover:text-blue-700 flex items-center gap-1"
          >
            <span>Full-Screen GIS Command</span>
            <ArrowUpRight className="w-3.5 h-3.5" />
          </button>
        </div>
        <GisMap fullScreen={false} />
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {stats && <RiskDonutChart distribution={stats.risk_distribution} />}
        {stats && <DisturbanceTrendChart data={stats.disturbance_trend} />}
        {stats && <DistrictAlertsBarChart data={stats.district_summaries} />}
      </div>

      {/* Flagged Potential Unauthorized Activity Alert Table */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="p-4 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
          <div>
            <h3 className="text-sm font-bold text-slate-900">
              Recent Priority Alerts ({selectedRegion} Sector)
            </h3>
            <p className="text-xs text-slate-500">
              Explainable AI risk scoring requiring mandatory human field verification.
            </p>
          </div>
          <button
            onClick={() => setCurrentPage('alerts')}
            className="text-xs font-bold text-blue-600 hover:text-blue-700 flex items-center gap-1"
          >
            <span>View All Alerts (24)</span>
            <ArrowUpRight className="w-3.5 h-3.5" />
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-700">
            <thead className="bg-slate-100/70 text-slate-600 font-bold uppercase tracking-wider border-b border-slate-200">
              <tr>
                <th className="p-3">Alert ID</th>
                <th className="p-3">Location & Sector</th>
                <th className="p-3">Risk Score</th>
                <th className="p-3">Disturbed Area</th>
                <th className="p-3">Lease Relationship</th>
                <th className="p-3">Distance</th>
                <th className="p-3">Status</th>
                <th className="p-3 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200">
              {recentAlerts.map((alert) => (
                <tr key={alert.id} className="hover:bg-slate-50/80 transition">
                  <td className="p-3 font-mono font-bold text-slate-900">{alert.id}</td>
                  <td className="p-3">
                    <div className="font-semibold text-slate-800">{alert.title}</div>
                    <div className="text-[11px] text-slate-400">{alert.location_name}</div>
                  </td>
                  <td className="p-3">
                    <RiskBadge level={alert.priority} score={alert.risk_score} />
                  </td>
                  <td className="p-3 font-mono font-semibold">{alert.disturbed_area_ha} ha</td>
                  <td className="p-3">
                    <span
                      className={`font-semibold text-[11px] ${
                        alert.lease_status.includes('Outside')
                          ? 'text-red-700 font-bold'
                          : alert.lease_status.includes('Buffer')
                          ? 'text-amber-700'
                          : 'text-emerald-700'
                      }`}
                    >
                      {alert.lease_status}
                    </span>
                  </td>
                  <td className="p-3 font-mono">{alert.distance_from_lease_m} m</td>
                  <td className="p-3">
                    <StatusBadge status={alert.status} />
                  </td>
                  <td className="p-3 text-right">
                    <button
                      onClick={() => navigateToAlert(alert.id)}
                      className="bg-blue-600 hover:bg-blue-700 text-white px-2.5 py-1 rounded text-xs font-semibold shadow-sm transition"
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
