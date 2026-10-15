import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';

interface DistrictAlertsBarChartProps {
  data: Array<{
    district: string;
    state: string;
    mineral: string;
    active_alerts: number;
    critical: number;
    disturbed_ha: number;
    avg_risk: number;
  }>;
}

export const DistrictAlertsBarChart: React.FC<DistrictAlertsBarChartProps> = ({ data }) => {
  return (
    <div className="bg-white rounded-xl p-4 border border-slate-200 shadow-sm flex flex-col h-full">
      <div className="flex items-center justify-between mb-2">
        <h4 className="text-sm font-bold text-slate-800">Mining Disturbance by Sector</h4>
        <span className="text-xs text-slate-400">4 Active Indian Mining Hubs</span>
      </div>
      <div className="h-56 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 10, right: 10, left: -15, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
            <XAxis dataKey="district" tick={{ fontSize: 11, fill: '#64748b' }} />
            <YAxis tick={{ fontSize: 11, fill: '#64748b' }} />
            <Tooltip
              contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', color: '#fff' }}
              itemStyle={{ color: '#fff', fontSize: '12px' }}
            />
            <Legend
              verticalAlign="bottom"
              height={36}
              formatter={(value) => <span className="text-xs font-medium text-slate-600">{value}</span>}
            />
            <Bar dataKey="active_alerts" name="Active Alerts" fill="#3b82f6" radius={[4, 4, 0, 0]} />
            <Bar dataKey="critical" name="Critical Risk" fill="#ef4444" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
