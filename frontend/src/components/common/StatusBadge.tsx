import React from 'react';
import { AlertStatus } from '../../types';

interface StatusBadgeProps {
  status: AlertStatus | string;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status }) => {
  const norm = (status || 'PENDING').toUpperCase();

  const configs: Record<string, { bg: string; text: string; border: string; label: string }> = {
    PENDING: {
      bg: 'bg-amber-50',
      text: 'text-amber-700',
      border: 'border-amber-200',
      label: 'Pending Verification'
    },
    UNDER_REVIEW: {
      bg: 'bg-blue-50',
      text: 'text-blue-700',
      border: 'border-blue-200',
      label: 'Under Review'
    },
    FIELD_VERIFICATION: {
      bg: 'bg-purple-50',
      text: 'text-purple-700',
      border: 'border-purple-200',
      label: 'Field Inspection Active'
    },
    VERIFIED: {
      bg: 'bg-emerald-50',
      text: 'text-emerald-700',
      border: 'border-emerald-200',
      label: 'Ground Verified'
    },
    FALSE_POSITIVE: {
      bg: 'bg-slate-100',
      text: 'text-slate-700',
      border: 'border-slate-300',
      label: 'False Positive'
    },
    REJECTED: {
      bg: 'bg-red-50',
      text: 'text-red-700',
      border: 'border-red-200',
      label: 'Rejected'
    },
    CLOSED: {
      bg: 'bg-gray-100',
      text: 'text-gray-700',
      border: 'border-gray-300',
      label: 'Case Closed'
    }
  };

  const current = configs[norm] || {
    bg: 'bg-slate-50',
    text: 'text-slate-700',
    border: 'border-slate-200',
    label: norm
  };

  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded text-xs font-semibold border ${current.bg} ${current.text} ${current.border}`}
    >
      {current.label}
    </span>
  );
};
