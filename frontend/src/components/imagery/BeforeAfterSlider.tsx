import React, { useState } from 'react';
import { Calendar, Eye, Layers } from 'lucide-react';

interface BeforeAfterSliderProps {
  beforeLabel?: string;
  afterLabel?: string;
  beforeDate?: string;
  afterDate?: string;
  sensor?: string;
}

export const BeforeAfterSlider: React.FC<BeforeAfterSliderProps> = ({
  beforeLabel = 'Baseline Observation',
  afterLabel = 'Current Surveillance Acquisition',
  beforeDate = '2022-03-12',
  afterDate = '2026-08-18',
  sensor = 'Sentinel-2 L2A (10m True Color & NIR Composite)'
}) => {
  const [sliderPosition, setSliderPosition] = useState<number>(50);

  return (
    <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm">
      {/* Header Info */}
      <div className="p-3 bg-slate-900 text-white flex flex-wrap items-center justify-between gap-2 text-xs border-b border-slate-800">
        <div className="flex items-center gap-2">
          <Layers className="w-4 h-4 text-blue-400" />
          <span className="font-bold">Temporal Dual-Stream Comparison Slider</span>
        </div>
        <div className="text-slate-400 font-mono text-[11px]">
          Sensor: <span className="text-slate-200">{sensor}</span>
        </div>
      </div>

      {/* Interactive Split-Screen Image Area */}
      <div className="relative h-72 sm:h-88 md:h-96 w-full select-none overflow-hidden bg-slate-950">
        {/* Baseline (Before) Background View */}
        <div
          className="absolute inset-0 w-full h-full flex flex-col justify-between p-4"
          style={{
            backgroundImage: `radial-gradient(circle at 40% 40%, #1e3a8a 0%, #064e3b 40%, #022c22 80%)`
          }}
        >
          {/* Synthetic Landscape Visualization Elements (Baseline Pre-mining) */}
          <div className="absolute inset-0 opacity-80 pointer-events-none">
            <svg className="w-full h-full opacity-60">
              <pattern id="forestPattern" width="40" height="40" patternUnits="userSpaceOnUse">
                <circle cx="20" cy="20" r="14" fill="#047857" opacity="0.7" />
                <circle cx="10" cy="10" r="8" fill="#065f46" opacity="0.6" />
                <circle cx="30" cy="30" r="10" fill="#10b981" opacity="0.4" />
              </pattern>
              <rect width="100%" height="100%" fill="url(#forestPattern)" />
              <path d="M 0 180 Q 150 140 300 200 T 600 160" stroke="#0284c7" strokeWidth="6" fill="none" opacity="0.8" />
            </svg>
          </div>
          <div className="relative z-10 self-start bg-slate-900/90 text-white px-2.5 py-1 rounded-md text-xs font-semibold border border-slate-700 shadow-md">
            <div className="text-[10px] text-emerald-400 uppercase tracking-wider">{beforeLabel}</div>
            <div className="flex items-center gap-1.5 font-mono">
              <Calendar className="w-3.5 h-3.5 text-slate-400" />
              <span>{beforeDate}</span>
            </div>
          </div>
          <div className="relative z-10 self-start bg-emerald-900/80 text-emerald-200 px-2 py-0.5 rounded text-[11px] font-semibold">
            Canopy NDVI: 0.68 (Dense Forest)
          </div>
        </div>

        {/* Current (After) Foreground Clipped View */}
        <div
          className="absolute inset-0 w-full h-full flex flex-col justify-between p-4 overflow-hidden"
          style={{
            clipPath: `polygon(${sliderPosition}% 0, 100% 0, 100% 100%, ${sliderPosition}% 100%)`,
            backgroundImage: `radial-gradient(circle at 60% 50%, #7f1d1d 0%, #450a0a 35%, #1c1917 80%)`
          }}
        >
          {/* Synthetic Excavated Pit & Waste Dump Overlay */}
          <div className="absolute inset-0 opacity-90 pointer-events-none">
            <svg className="w-full h-full">
              <ellipse cx="65%" cy="50%" rx="18%" ry="24%" fill="#b91c1c" opacity="0.75" stroke="#ef4444" strokeWidth="3" />
              <ellipse cx="65%" cy="50%" rx="10%" ry="14%" fill="#7f1d1d" opacity="0.9" />
              <ellipse cx="85%" cy="35%" rx="12%" ry="16%" fill="#ea580c" opacity="0.7" stroke="#f97316" strokeWidth="2" strokeDasharray="4,4" />
              {/* Haul road */}
              <path d="M 400 320 Q 520 220 620 250" stroke="#78716c" strokeWidth="8" fill="none" opacity="0.9" />
            </svg>
          </div>
          <div className="relative z-10 self-end bg-slate-900/90 text-white px-2.5 py-1 rounded-md text-xs font-semibold border border-slate-700 shadow-md">
            <div className="text-[10px] text-red-400 uppercase tracking-wider">{afterLabel}</div>
            <div className="flex items-center gap-1.5 font-mono">
              <Calendar className="w-3.5 h-3.5 text-slate-400" />
              <span>{afterDate}</span>
            </div>
          </div>
          <div className="relative z-10 self-end bg-red-900/90 text-red-200 px-2 py-0.5 rounded text-[11px] font-semibold flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-red-500 animate-ping"></span>
            Excavation NDVI: 0.14 | BSI: +0.52 (14.2 ha)
          </div>
        </div>

        {/* Vertical Divider Bar */}
        <div
          className="absolute top-0 bottom-0 w-1 bg-white shadow-[0_0_12px_rgba(255,255,255,0.9)] z-20 pointer-events-none"
          style={{ left: `${sliderPosition}%` }}
        >
          <div className="absolute top-1/2 -translate-y-1/2 -translate-x-1/2 w-8 h-8 rounded-full bg-white text-slate-900 shadow-xl flex items-center justify-center font-bold text-xs border-2 border-blue-600">
            &#8596;
          </div>
        </div>

        {/* Range Input controller */}
        <input
          type="range"
          min="0"
          max="100"
          value={sliderPosition}
          onChange={(e) => setSliderPosition(Number(e.target.value))}
          aria-label="Temporal Dual-Stream Comparison Slider"
          className="absolute inset-0 w-full h-full opacity-0 cursor-ew-resize z-30"
        />
      </div>

      {/* Bottom Slider Bar Controls */}
      <div className="p-3 bg-slate-50 flex items-center justify-between text-xs text-slate-600 border-t border-slate-200">
        <div className="flex items-center gap-2 font-medium">
          <Eye className="w-4 h-4 text-slate-500" />
          <span>Drag slider or click image to scrub between Baseline and Breach state</span>
        </div>
        <div className="font-mono text-xs font-semibold text-blue-600">
          Split Position: {sliderPosition}%
        </div>
      </div>
    </div>
  );
};
