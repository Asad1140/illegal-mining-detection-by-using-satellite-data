import React, { useState } from 'react';
import { Activity, Trees, Flame, Droplets, Radio, Info } from 'lucide-react';

export const SpectralIndexViewer: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'NDVI' | 'BSI' | 'NDWI' | 'NDBI' | 'SAR'>('NDVI');

  const indices = {
    NDVI: {
      name: 'Normalized Difference Vegetation Index',
      formula: '(B8 - B4) / (B8 + B4)',
      baseline: 0.68,
      current: 0.14,
      delta: -0.54,
      status: 'CRITICAL CANOPY LOSS (-79.4%)',
      color: 'text-red-600 bg-red-50 border-red-200',
      description: 'Quantifies photosynthetic vegetation biomass. Rapid drop from 0.68 to 0.14 confirms clear-felling and topsoil removal over 14.2 ha.',
      icon: Trees
    },
    BSI: {
      name: 'Bare Soil Index',
      formula: '((B11 + B4) - (B8 + B2)) / ((B11 + B4) + (B8 + B2))',
      baseline: -0.22,
      current: +0.52,
      delta: +0.74,
      status: 'HIGH BARE SOIL EXPOSURE (+52%)',
      color: 'text-amber-700 bg-amber-50 border-amber-200',
      description: 'Discriminates exposed soil and excavated quarry surfaces from surrounding vegetation and water bodies.',
      icon: Flame
    },
    NDWI: {
      name: 'Normalized Difference Water Index',
      formula: '(B3 - B8) / (B3 + B8)',
      baseline: -0.12,
      current: -0.34,
      delta: -0.22,
      status: 'WATERSHED DRAINAGE ALTERATION',
      color: 'text-blue-700 bg-blue-50 border-blue-200',
      description: 'Detects surface water content and water body turbid runoffs resulting from mining spoil runoff.',
      icon: Droplets
    },
    NDBI: {
      name: 'Normalized Difference Built-up Index',
      formula: '(B11 - B8) / (B11 + B8)',
      baseline: -0.32,
      current: +0.44,
      delta: +0.76,
      status: 'HAULAGE INFRASTRUCTURE DETECTED',
      color: 'text-purple-700 bg-purple-50 border-purple-200',
      description: 'Highlights artificial hard surfaces, unpaved mineral transport roads, and crushing platforms.',
      icon: Activity
    },
    SAR: {
      name: 'Sentinel-1 SAR C-Band Backscatter (VV/VH)',
      formula: '10 * log10(Sigma0_VV / Sigma0_VH)',
      baseline: -14.8,
      current: -8.1,
      delta: +6.7,
      status: 'RADAR ANOMALY CONFIRMED (+6.7 dB)',
      color: 'text-indigo-700 bg-indigo-50 border-indigo-200',
      description: 'Synthetic Aperture Radar penetration detects abrupt geometric roughness changes and pit slope cleavage even through cloud cover.',
      icon: Radio
    }
  };

  const curr = indices[activeTab];
  const Icon = curr.icon;

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-4">
      {/* Tabs */}
      <div className="flex flex-wrap gap-1.5 border-b border-slate-200 pb-3 mb-4">
        {(Object.keys(indices) as Array<keyof typeof indices>).map((key) => {
          const item = indices[key];
          const ItemIcon = item.icon;
          const isActive = activeTab === key;
          return (
            <button
              key={key}
              onClick={() => setActiveTab(key)}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition ${
                isActive
                  ? 'bg-blue-600 text-white shadow-sm'
                  : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
              }`}
            >
              <ItemIcon className="w-3.5 h-3.5" />
              <span>{key}</span>
            </button>
          );
        })}
      </div>

      {/* Active Tab Content */}
      <div className="space-y-4">
        <div className="flex flex-wrap items-start justify-between gap-2">
          <div>
            <h4 className="text-sm font-bold text-slate-900 flex items-center gap-2">
              <Icon className="w-4 h-4 text-blue-600" />
              <span>{curr.name} ({activeTab})</span>
            </h4>
            <span className="font-mono text-xs text-slate-500 bg-slate-100 px-2 py-0.5 rounded inline-block mt-1">
              Formula: {curr.formula}
            </span>
          </div>
          <span className={`text-xs font-bold px-2.5 py-1 rounded-md border ${curr.color}`}>
            {curr.status}
          </span>
        </div>

        {/* 3 Metric Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div className="bg-slate-50 p-3 rounded-lg border border-slate-200">
            <span className="text-[10px] uppercase font-bold text-slate-400">Baseline (2022)</span>
            <div className="text-lg font-mono font-bold text-slate-800">{curr.baseline}</div>
          </div>
          <div className="bg-slate-50 p-3 rounded-lg border border-slate-200">
            <span className="text-[10px] uppercase font-bold text-slate-400">Current (2026)</span>
            <div className="text-lg font-mono font-bold text-slate-800">{curr.current}</div>
          </div>
          <div className="bg-slate-50 p-3 rounded-lg border border-slate-200">
            <span className="text-[10px] uppercase font-bold text-slate-400">Spectral Delta</span>
            <div className={`text-lg font-mono font-bold ${curr.delta < 0 && activeTab === 'NDVI' ? 'text-red-600' : 'text-amber-600'}`}>
              {curr.delta > 0 ? `+${curr.delta}` : curr.delta}
            </div>
          </div>
        </div>

        <p className="text-xs text-slate-600 leading-relaxed bg-slate-50 p-2.5 rounded-lg border border-slate-200">
          <Info className="w-3.5 h-3.5 inline text-blue-600 mr-1.5" />
          {curr.description}
        </p>
      </div>
    </div>
  );
};
