import React from 'react';
import { useApp } from '../../context/AppContext';
import { Shield, Satellite, Globe, UserCheck, Info, MapPin, CheckCircle2, Sparkles } from 'lucide-react';
import { UserRole } from '../../types';

export const Header: React.FC = () => {
  const {
    selectedRegion,
    setSelectedRegion,
    currentRole,
    setCurrentRole,
    setDisclaimerOpen,
    isRealDataMode,
    setIsRealDataMode
  } = useApp();

  const regions = [
    { name: 'Keonjhar', state: 'India', mineral: 'Iron Ore' },
    { name: 'Bellary', state: 'India', mineral: 'Iron Ore' },
    { name: 'Sukinda', state: 'India', mineral: 'Chromite' },
    { name: 'Singrauli', state: 'India', mineral: 'Coal' }
  ];

  const roles: { role: UserRole; label: string }[] = [
    { role: 'ADMIN', label: 'Admin (Full Access)' },
    { role: 'ANALYST', label: 'GIS Analyst (Analyze)' },
    { role: 'FIELD_OFFICER', label: 'Field Officer (Verify)' },
    { role: 'VIEWER', label: 'Auditor (Read-Only)' }
  ];

  return (
    <header className="bg-slate-900 border-b border-slate-800 text-white sticky top-0 z-40 shadow-md">
      <div className="px-4 py-2.5 flex items-center justify-between gap-4">
        {/* Logo & Mode Indicator */}
        <div className="flex items-center gap-3">
          <div className="bg-blue-600 p-2 rounded-lg text-white shadow-inner flex items-center justify-center">
            <Shield className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-extrabold tracking-wider text-base md:text-lg text-white flex items-center gap-1.5">
                <span className="hidden sm:inline">Illegal Mining Detection</span>
                <span className="sm:hidden">IMD System</span>
              </span>
              
              {/* Prominent Application Mode Switcher Badge */}
              <button
                onClick={() => setIsRealDataMode(!isRealDataMode)}
                title="Click to toggle between Live Copernicus Satellite Data and Demo Mode"
                className={`flex items-center gap-1.5 px-2.5 py-0.5 text-[10px] font-bold uppercase tracking-wider rounded-md border transition cursor-pointer ${
                  isRealDataMode
                    ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40 hover:bg-emerald-500/30'
                    : 'bg-amber-500/20 text-amber-300 border-amber-500/40 hover:bg-amber-500/30'
                }`}
              >
                <span className={`w-1.5 h-1.5 rounded-full animate-pulse ${isRealDataMode ? 'bg-emerald-400' : 'bg-amber-400'}`} />
                <span>{isRealDataMode ? 'REAL SATELLITE DATA' : 'DEMO MODE'}</span>
                <span className="text-[9px] opacity-70 underline ml-0.5">toggle</span>
              </button>
            </div>
            <p className="text-xs text-slate-400 font-medium hidden sm:block">
              by Using Satellite Data
            </p>
          </div>
        </div>

        {/* Center: Global/Region Selector */}
        <div className="flex items-center gap-2 bg-slate-800/80 px-3 py-1.5 rounded-lg border border-slate-700">
          <Globe className="w-4 h-4 text-blue-400 shrink-0" />
          <span className="text-xs text-slate-400 hidden lg:inline">Sector Preset:</span>
          <select
            value={selectedRegion}
            onChange={(e) => setSelectedRegion(e.target.value)}
            aria-label="Monitored Sector"
            className="bg-transparent text-sm font-semibold text-white focus:outline-none cursor-pointer"
          >
            {regions.map((r) => (
              <option key={r.name} value={r.name} className="bg-slate-900 text-white">
                {r.name}, {r.state} ({r.mineral})
              </option>
            ))}
          </select>
        </div>

        {/* Right: Role Switcher & Disclaimer */}
        <div className="flex items-center gap-3">
          {/* User Role Switcher */}
          <div className="flex items-center gap-2 bg-slate-800/80 px-2.5 py-1.5 rounded-lg border border-slate-700">
            <UserCheck className="w-4 h-4 text-emerald-400 shrink-0" />
            <select
              value={currentRole}
              onChange={(e) => setCurrentRole(e.target.value as UserRole)}
              aria-label="User Role"
              className="bg-transparent text-xs font-semibold text-slate-200 focus:outline-none cursor-pointer"
            >
              {roles.map((r) => (
                <option key={r.role} value={r.role} className="bg-slate-900 text-white">
                  {r.label}
                </option>
              ))}
            </select>
          </div>

          {/* Legal Disclaimer Button */}
          <button
            onClick={() => setDisclaimerOpen(true)}
            className="flex items-center gap-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white px-2.5 py-1.5 rounded-lg text-xs font-medium border border-slate-700 transition"
            title="Read Legal & Scientific Decision-Support Disclaimer"
          >
            <Info className="w-3.5 h-3.5 text-amber-400" />
            <span className="hidden md:inline">Legal Notice</span>
          </button>
        </div>
      </div>
    </header>
  );
};
