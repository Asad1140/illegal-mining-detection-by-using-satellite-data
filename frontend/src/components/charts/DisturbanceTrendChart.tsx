import React from 'react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from 'recharts';

interface DisturbanceTrendProps {
  data: Array<{ year: string; area_ha: number; rate_pct: string }>;
}

export const DisturbanceTrendChart: React.FC<DisturbanceTrendProps> = ({ data }) => {
  return (
    <div className="bg-white rounded-xl p-4 border border-slate-200 shadow-sm flex flex-col h-full">
      <div className="flex items-center justify-between mb-2">
        <div>
          <h4 className="text-sm font-bold text-slate-800">Land Disturbance Trajectory (2022 - 2026)</h4>
          <p className="text-xs text-slate-400">Cumulative surface disturbance area across monitored sectors</p>
        </div>
        <span className="text-xs font-bold text-red-600 bg-red-50 px-2 py-0.5 rounded border border-red-200">
          +184.6 ha Total
        </span>
      </div>
      <div className="h-56 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 10, right: 10, left: -15, bottom: 0 }}>
            <defs>
              <linearGradient id="areaGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#ef4444" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#ef4444" stopOpacity={0.0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
            <XAxis dataKey="year" tick={{ fontSize: 11, fill: '#64748b' }} />
            <YAxis tick={{ fontSize: 11, fill: '#64748b' }} unit=" ha" />
            <Tooltip
              contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', color: '#fff' }}
              itemStyle={{ color: '#fff', fontSize: '12px' }}
              formatter={(val: any) => [`${val} ha`, 'Disturbed Area']}
            />
            <Area
              type="monotone"
              dataKey="area_ha"
              stroke="#ef4444"
              strokeWidth={2.5}
              fillOpacity={1}
              fill="url(#areaGradient)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
