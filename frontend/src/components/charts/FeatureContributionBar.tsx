import React from 'react';
import { RiskBreakdown } from '../../types';

interface FeatureContributionBarProps {
  factors: RiskBreakdown;
}

export const FeatureContributionBar: React.FC<FeatureContributionBarProps> = ({ factors }) => {
  const items = [
    { label: 'Surface Mining Disturbance (Area)', score: factors.disturbance_score, max: 25, color: 'bg-red-500' },
    { label: 'Temporal Multi-Date Persistence', score: factors.temporal_persistence_score, max: 20, color: 'bg-orange-500' },
    { label: 'Spatial Boundary / Outside Lease', score: factors.outside_lease_score, max: 20, color: 'bg-amber-500' },
    { label: 'Vegetation Canopy Loss (NDVI Drop)', score: factors.vegetation_loss_score, max: 10, color: 'bg-emerald-500' },
    { label: 'SAR Radar Backscatter Anomaly', score: factors.sar_anomaly_score, max: 10, color: 'bg-blue-500' },
    { label: 'Historical YoY Expansion Vector', score: factors.historical_expansion_score, max: 10, color: 'bg-purple-500' },
    { label: 'Terrain & Watershed Vulnerability', score: factors.terrain_context_score, max: 5, color: 'bg-teal-500' },
  ];

  return (
    <div className="space-y-3">
      {items.map((item, idx) => {
        const pct = Math.min(100, Math.round((item.score / item.max) * 100));
        return (
          <div key={idx} className="space-y-1">
            <div className="flex justify-between text-xs font-semibold text-slate-700">
              <span>{item.label}</span>
              <span className="font-mono text-slate-900">
                {item.score} / {item.max} pts ({pct}%)
              </span>
            </div>
            <div className="w-full bg-slate-100 rounded-full h-2 overflow-hidden border border-slate-200">
              <div
                className={`h-full rounded-full ${item.color} transition-all duration-500`}
                style={{ width: `${pct}%` }}
              ></div>
            </div>
          </div>
        );
      })}
    </div>
  );
};
