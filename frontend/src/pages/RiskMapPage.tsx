import React, { useState, useEffect } from 'react';
import { useApp } from '../context/AppContext';
import { apiClient } from '../api/client';
import { Alert } from '../types';
import { GisMap } from '../components/map/GisMap';
import { RiskBadge } from '../components/common/RiskBadge';
import { StatusBadge } from '../components/common/StatusBadge';
import {
  Map as MapIcon,
  Shield,
  Layers,
  AlertTriangle,
  Flame,
  Search,
  ExternalLink,
  Info
} from 'lucide-react';

export const RiskMapPage: React.FC = () => {
  const { selectedRegion, navigateToAlert } = useApp();
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [searchTerm, setSearchTerm] = useState<string>('');

  useEffect(() => {
    apiClient.getAlerts({ district: selectedRegion }).then(setAlerts).catch(console.error);
  }, [selectedRegion]);

  const filteredAlerts = alerts.filter(
    (a) =>
      a.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
      a.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      a.location_name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-4">
      {/* Top Map Action Bar */}
      <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-2.5">
          <div className="p-2 bg-blue-50 text-blue-600 rounded-lg">
            <MapIcon className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base font-extrabold text-slate-900 flex items-center gap-2">
              <span>Full-Screen GIS Surveillance Command Center</span>
              <span className="text-xs font-bold text-blue-600 bg-blue-50 px-2 py-0.5 rounded border border-blue-200">
                {selectedRegion} Sector
              </span>
            </h2>
            <p className="text-xs text-slate-500">
              Interactive multi-layer spatial intersection (Lease boundaries, 500m statutory buffers, AI disturbance polygons).
            </p>
          </div>
        </div>

        {/* Legend */}
        <div className="flex items-center gap-2 text-xs font-semibold bg-slate-50 px-3 py-1.5 rounded-lg border border-slate-200">
          <span className="text-slate-500 text-[11px] uppercase">Risk Legend:</span>
          <span className="flex items-center gap-1 text-emerald-700"><span className="w-2.5 h-2.5 rounded-full bg-emerald-500"></span> Low</span>
          <span className="flex items-center gap-1 text-amber-700"><span className="w-2.5 h-2.5 rounded-full bg-amber-500"></span> Med</span>
          <span className="flex items-center gap-1 text-orange-700"><span className="w-2.5 h-2.5 rounded-full bg-orange-500"></span> High</span>
          <span className="flex items-center gap-1 text-red-700"><span className="w-2.5 h-2.5 rounded-full bg-red-600"></span> Critical</span>
        </div>
      </div>

      {/* Main Grid: Left GIS Map, Right Active Risk Zones Drawer */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-4">
        {/* Full-Screen GIS Map View (3 cols) */}
        <div className="lg:col-span-3">
          <GisMap fullScreen={true} />
        </div>

        {/* Right Active Risk Zones Drawer (1 col) */}
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-4 flex flex-col h-[calc(100vh-125px)]">
          <div className="pb-3 border-b border-slate-200 space-y-2">
            <div className="flex items-center justify-between">
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 flex items-center gap-1.5">
                <Flame className="w-4 h-4 text-red-600" />
                <span>Sector Anomalies ({filteredAlerts.length})</span>
              </h3>
            </div>
            {/* Search */}
            <div className="relative">
              <Search className="w-3.5 h-3.5 absolute left-2.5 top-2.5 text-slate-400" />
              <input
                type="text"
                placeholder="Filter anomalies..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full bg-slate-50 border border-slate-200 rounded-lg pl-8 pr-3 py-1.5 text-xs text-slate-800 focus:outline-none focus:border-blue-500"
              />
            </div>
          </div>

          {/* List */}
          <div className="flex-1 overflow-y-auto space-y-2.5 pt-3 custom-scrollbar pr-1">
            {filteredAlerts.map((alert) => (
              <div
                key={alert.id}
                onClick={() => navigateToAlert(alert.id)}
                className="p-3 rounded-lg border border-slate-200 hover:border-blue-400 hover:bg-blue-50/40 cursor-pointer transition space-y-2 shadow-xs"
              >
                <div className="flex items-center justify-between">
                  <span className="font-mono font-extrabold text-xs text-slate-900">{alert.id}</span>
                  <RiskBadge level={alert.priority} score={alert.risk_score} showScore={true} />
                </div>
                <div className="text-xs font-semibold text-slate-800 line-clamp-1">{alert.title}</div>
                <div className="grid grid-cols-2 gap-1 text-[11px] text-slate-500 font-medium">
                  <div>Area: <span className="text-slate-800 font-mono font-bold">{alert.disturbed_area_ha} ha</span></div>
                  <div>Dist: <span className="text-slate-800 font-mono font-bold">{alert.distance_from_lease_m} m</span></div>
                </div>
                <div className="flex items-center justify-between text-[10px] text-slate-500 border-t border-slate-100 pt-1.5">
                  <span className="text-red-700 font-semibold">{alert.lease_status}</span>
                  <span className="text-blue-600 font-bold flex items-center gap-0.5">
                    Dossier &rarr;
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
