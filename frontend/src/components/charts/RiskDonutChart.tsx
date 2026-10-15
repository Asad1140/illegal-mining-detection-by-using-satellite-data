import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';

interface RiskDonutProps {
  distribution: {
    LOW: number;
    MEDIUM: number;
    HIGH: number;
    CRITICAL: number;
  };
}

export const RiskDonutChart: React.FC<RiskDonutProps> = ({ distribution }) => {
  const data = [
    { name: 'Low Risk (0-24)', value: distribution.LOW, color: '#10b981' },
    { name: 'Medium Risk (25-49)', value: distribution.MEDIUM, color: '#eab308' },
    { name: 'High Risk (50-74)', value: distribution.HIGH, color: '#f97316' },
    { name: 'Critical Risk (75-100)', value: distribution.CRITICAL, color: '#ef4444' }
  ];

  const total = data.reduce((acc, curr) => acc + curr.value, 0);

  return (
    <div className="bg-white rounded-xl p-4 border border-slate-200 shadow-sm flex flex-col h-full">
      <div className="flex items-center justify-between mb-2">
        <h4 className="text-sm font-bold text-slate-800">Risk Level Distribution</h4>
        <span className="text-xs font-semibold text-slate-400">Total: {total}</span>
      </div>
      <div className="h-56 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              innerRadius={55}
              outerRadius={78}
              paddingAngle={4}
              dataKey="value"
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip
              contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', color: '#fff' }}
              itemStyle={{ color: '#fff', fontSize: '12px' }}
            />
            <Legend
              verticalAlign="bottom"
              height={36}
              formatter={(value) => <span className="text-xs font-medium text-slate-600">{value}</span>}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
