import React from 'react';
import { useApp } from '../../context/AppContext';
import {
  LayoutDashboard,
  Map,
  AlertOctagon,
  Satellite,
  Building2,
  GitCompare,
  Cpu,
  CheckSquare,
  FileText,
  Database,
  Network,
  Settings
} from 'lucide-react';

interface NavItem {
  id: string;
  label: string;
  icon: React.ComponentType<{ className?: string }>;
  badge?: string;
  badgeColor?: string;
}

export const Sidebar: React.FC = () => {
  const { currentPage, setCurrentPage } = useApp();

  const navItems: NavItem[] = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'risk-map', label: 'Risk Map', icon: Map, badge: 'LIVE GIS', badgeColor: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40' },
    { id: 'alerts', label: 'Alerts', icon: AlertOctagon, badge: '24', badgeColor: 'bg-red-500/20 text-red-300 border-red-500/40' },
    { id: 'satellite-analysis', label: 'Satellite Timeline', icon: Satellite },
    { id: 'mining-leases', label: 'Mining Leases', icon: Building2 },
    { id: 'change-detection', label: 'Change Detection', icon: GitCompare },
    { id: 'ai-models', label: 'AI Models', icon: Cpu, badge: 'Proto', badgeColor: 'bg-purple-500/20 text-purple-300 border-purple-500/40' },
    { id: 'field-verification', label: 'Field Verification', icon: CheckSquare, badge: 'Queue (13)', badgeColor: 'bg-amber-500/20 text-amber-300 border-amber-500/40' },
    { id: 'reports', label: 'Reports', icon: FileText },
    { id: 'data-sources', label: 'Data Sources', icon: Database },
    { id: 'system-architecture', label: 'System Architecture', icon: Network },
    { id: 'settings', label: 'Settings', icon: Settings }
  ];

  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 text-slate-300 flex flex-col shrink-0 h-[calc(100vh-53px)] sticky top-[53px]">
      <div className="p-3 text-[11px] font-bold text-slate-400 uppercase tracking-wider px-4">
        Surveillance Navigation
      </div>
      <nav className="flex-1 px-2 space-y-1 overflow-y-auto custom-scrollbar">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = currentPage === item.id || (currentPage === 'alert-details' && item.id === 'alerts');
          return (
            <button
              key={item.id}
              onClick={() => setCurrentPage(item.id)}
              className={`w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-sm font-medium transition ${
                isActive
                  ? 'bg-blue-600 text-white font-semibold shadow-sm'
                  : 'hover:bg-slate-800 text-slate-300 hover:text-white'
              }`}
            >
              <div className="flex items-center gap-3">
                <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-slate-400'}`} />
                <span>{item.label}</span>
              </div>
              {item.badge && (
                <span
                  className={`text-[10px] font-bold px-1.5 py-0.5 rounded border ${
                    isActive ? 'bg-white/20 text-white border-white/40' : item.badgeColor
                  }`}
                >
                  {item.badge}
                </span>
              )}
            </button>
          );
        })}
      </nav>

      {/* Bottom info panel */}
      <div className="p-3 m-2 bg-slate-800/60 border border-slate-700/60 rounded-lg text-xs">
        <div className="text-slate-400 font-semibold mb-1 flex items-center justify-between">
          <span>System Status</span>
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
        </div>
        <div className="text-[11px] text-slate-400">
          Engine: <span className="text-slate-200 font-medium">FastAPI + GIS</span>
        </div>
        <div className="text-[11px] text-slate-400">
          Feed: <span className="text-amber-300 font-medium">Demo Multi-Sensor</span>
        </div>
      </div>
    </aside>
  );
};
