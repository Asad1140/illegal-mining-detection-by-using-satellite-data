import React, { useState, useEffect } from 'react';
import { useApp } from '../context/AppContext';
import { apiClient } from '../api/client';
import { MiningLease } from '../types';
import {
  Building2,
  Search,
  Filter,
  MapPin,
  Calendar,
  ExternalLink,
  ShieldCheck,
  Map as MapIcon
} from 'lucide-react';

export const MiningLeasesPage: React.FC = () => {
  const { selectedRegion, setCurrentPage } = useApp();
  const [leases, setLeases] = useState<MiningLease[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [selectedMineral, setSelectedMineral] = useState<string>('ALL');

  useEffect(() => {
    setLoading(true);
    apiClient
      .getMiningLeases({
        district: selectedRegion === 'ALL' ? undefined : selectedRegion,
        mineral: selectedMineral
      })
      .then((data) => {
        setLeases(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error('Failed to load mining leases:', err);
        setLoading(false);
      });
  }, [selectedRegion, selectedMineral]);

  const filteredLeases = leases.filter(
    (l) =>
      l.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
      l.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      l.lessee_name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-4 pb-16">
      {/* Header */}
      <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-blue-50 text-blue-600 rounded-lg">
            <Building2 className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-extrabold text-slate-900 flex items-center gap-2">
              <span>Official Mining Lease Cadastre & Surveillance Registry</span>
              <span className="text-xs font-bold text-blue-700 bg-blue-50 px-2 py-0.5 rounded border border-blue-200">
                {filteredLeases.length} Registered Blocks
              </span>
            </h2>
            <p className="text-xs text-slate-500">
              State Directorate of Mines & Geology authoritative cadastral boundaries and statutory 500m buffer buffers.
            </p>
          </div>
        </div>

        <button
          onClick={() => setCurrentPage('risk-map')}
          className="flex items-center gap-1.5 bg-blue-600 hover:bg-blue-700 text-white px-3.5 py-1.5 rounded-lg text-xs font-bold transition shadow-xs"
        >
          <MapIcon className="w-3.5 h-3.5" />
          <span>View All on GIS Map</span>
        </button>
      </div>

      {/* Filter Bar */}
      <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm flex flex-wrap items-center justify-between gap-3 text-xs">
        <div className="flex flex-wrap items-center gap-2.5">
          <div className="relative w-64">
            <Search className="w-3.5 h-3.5 absolute left-2.5 top-2.5 text-slate-400" />
            <input
              type="text"
              placeholder="Search lease ID, name, lessee..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full bg-slate-50 border border-slate-200 rounded-lg pl-8 pr-3 py-1.5 text-xs text-slate-800 focus:outline-none focus:border-blue-500"
            />
          </div>

          <div className="flex items-center gap-1.5 bg-slate-50 px-2.5 py-1.5 rounded-lg border border-slate-200">
            <Filter className="w-3.5 h-3.5 text-slate-400" />
            <span className="text-slate-500 font-medium">Mineral:</span>
            <select
              value={selectedMineral}
              onChange={(e) => setSelectedMineral(e.target.value)}
              className="bg-transparent font-semibold text-slate-800 focus:outline-none cursor-pointer"
            >
              <option value="ALL">All Minerals</option>
              <option value="Iron Ore">Iron Ore</option>
              <option value="Chromite">Chromite</option>
              <option value="Coal">Coal</option>
            </select>
          </div>
        </div>

        <span className="text-xs text-slate-400 font-mono">
          Cadastre Standard: WGS84 / EPSG:4326
        </span>
      </div>

      {/* Leases Table */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-700">
            <thead className="bg-slate-100/70 text-slate-600 font-bold uppercase tracking-wider border-b border-slate-200">
              <tr>
                <th className="p-3.5">Lease ID</th>
                <th className="p-3.5">Mine Block & Lessee Name</th>
                <th className="p-3.5">State & District</th>
                <th className="p-3.5">Mineral</th>
                <th className="p-3.5">Approved Area</th>
                <th className="p-3.5">Tenure Validity</th>
                <th className="p-3.5">Status</th>
                <th className="p-3.5">Active Alerts</th>
                <th className="p-3.5 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200">
              {filteredLeases.map((lease) => (
                <tr key={lease.id} className="hover:bg-slate-50/80 transition">
                  <td className="p-3.5 font-mono font-bold text-blue-700">{lease.id}</td>
                  <td className="p-3.5">
                    <div className="font-bold text-slate-900">{lease.name}</div>
                    <div className="text-[11px] text-slate-500">{lease.lessee_name}</div>
                  </td>
                  <td className="p-3.5 font-medium">
                    {lease.district}, {lease.state}
                  </td>
                  <td className="p-3.5 font-semibold text-slate-800">{lease.mineral}</td>
                  <td className="p-3.5 font-mono font-bold">{lease.area_hectares} ha</td>
                  <td className="p-3.5 text-[11px] font-mono text-slate-500">
                    {lease.grant_date} &rarr; {lease.expiry_date}
                  </td>
                  <td className="p-3.5">
                    <span className="inline-flex items-center gap-1 text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded text-[11px] font-bold">
                      <ShieldCheck className="w-3 h-3" />
                      {lease.status}
                    </span>
                  </td>
                  <td className="p-3.5 font-mono font-bold">
                    {lease.active_alerts_count > 0 ? (
                      <span className="text-red-600 bg-red-50 border border-red-200 px-2 py-0.5 rounded">
                        {lease.active_alerts_count} Flagged
                      </span>
                    ) : (
                      <span className="text-slate-400">0</span>
                    )}
                  </td>
                  <td className="p-3.5 text-right">
                    <button
                      onClick={() => setCurrentPage('risk-map')}
                      className="bg-slate-100 hover:bg-slate-200 text-slate-800 px-2.5 py-1 rounded text-xs font-semibold border border-slate-300 transition"
                    >
                      Zoom on Map
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
