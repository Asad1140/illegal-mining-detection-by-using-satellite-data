import React from 'react';
import { RiskLevel } from '../../types';

interface RiskBadgeProps {
  level: RiskLevel | string;
  score?: number;
  showScore?: boolean;
}

export const RiskBadge: React.FC<RiskBadgeProps> = ({ level, score, showScore = true }) => {
  const normLevel = (level || 'LOW').toUpperCase();

  const config = {
    LOW: {
      bg: 'bg-emerald-50 text-emerald-800 border-emerald-300',
      dot: 'bg-emerald-500',
      label: 'LOW RISK'
    },
    MEDIUM: {
      bg: 'bg-amber-50 text-amber-800 border-amber-300',
      dot: 'bg-amber-500',
      label: 'MEDIUM RISK'
    },
    HIGH: {
      bg: 'bg-orange-50 text-orange-800 border-orange-300',
      dot: 'bg-orange-500',
      label: 'HIGH RISK'
    },
    CRITICAL: {
      bg: 'bg-red-50 text-red-800 border-red-300 animate-pulse',
      dot: 'bg-red-600',
      label: 'CRITICAL RISK'
    }
  }[normLevel] || {
    bg: 'bg-slate-50 text-slate-800 border-slate-300',
    dot: 'bg-slate-500',
    label: normLevel
  };

  return (
    <span
      className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-bold border ${config.bg}`}
    >
      <span className={`w-2 h-2 rounded-full ${config.dot}`}></span>
      <span>{config.label}</span>
      {showScore && score !== undefined && (
        <span className="ml-1 px-1.5 py-0.2 bg-black/10 rounded font-mono text-[11px]">
          {score}/100
        </span>
      )}
    </span>
  );
};
