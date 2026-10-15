import React from 'react';
import { useApp } from '../../context/AppContext';
import { ShieldAlert, X, CheckCircle } from 'lucide-react';

export const DisclaimerModal: React.FC = () => {
  const { disclaimerOpen, setDisclaimerOpen } = useApp();

  if (!disclaimerOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-xl shadow-2xl max-w-2xl w-full border border-slate-200 overflow-hidden animate-in fade-in zoom-in-95 duration-150">
        {/* Header */}
        <div className="bg-slate-900 text-white px-6 py-4 flex items-center justify-between border-b border-slate-800">
          <div className="flex items-center gap-2.5">
            <ShieldAlert className="w-5 h-5 text-amber-400" />
            <h3 className="font-bold text-base">Legal & Scientific Decision-Support Disclaimer</h3>
          </div>
          <button
            onClick={() => setDisclaimerOpen(false)}
            aria-label="Close modal"
            className="text-slate-400 hover:text-white transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-4 text-sm text-slate-700 leading-relaxed">
          <div className="p-3.5 bg-amber-50 border-l-4 border-amber-500 rounded-r text-amber-900 text-xs font-semibold">
            NOTICE: This application is a prototype software developed for academic research and decision-support simulation.
          </div>

          <p className="font-semibold text-slate-900">
            Illegal Mining Detection by Using Satellite Data: AI-Powered Satellite Mining Surveillance, Change Detection & Early-Warning System
          </p>

          <p>
            1. <strong>Decision Support Only:</strong> The purpose of Illegal Mining Detection by Using Satellite Data is <em>not</em> to legally declare that a mining activity is illegal. The system flags <strong>Potential Unauthorized Mining Activity</strong> and generates explainable risk scores to optimize human field inspection workflows.
          </p>

          <p>
            2. <strong>Mandatory Field Verification:</strong> All satellite spectral indices (NDVI, BSI, NDWI), SAR backscatter variations, and AI disturbance segmentation masks are subject to atmospheric distortions, cloud filtering variations, and sensor resolution limits. <strong>On-site ground verification by authorized enforcement officers is mandatory</strong> before initiating statutory enforcement actions.
          </p>

          <p>
            3. <strong>Data & Model Attribution:</strong> Current observations represent demonstration and prototype simulation data based on real-world Indian mining sectors (Keonjhar, Bellary, Sukinda, Singrauli). Model benchmarks represent experimental baselines.
          </p>

          <div className="border-t border-slate-200 pt-3 text-xs text-slate-500">
            Directive reference: <em>Indian Bureau of Mines (IBM) & Directorate of Mines and Geology (DMG) Environmental Surveillance Guidelines</em>.
          </div>
        </div>

        {/* Footer */}
        <div className="bg-slate-50 px-6 py-3.5 border-t border-slate-200 flex justify-end">
          <button
            onClick={() => setDisclaimerOpen(false)}
            className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-semibold shadow transition"
          >
            <CheckCircle className="w-4 h-4" />
            I Understand & Acknowledge
          </button>
        </div>
      </div>
    </div>
  );
};
