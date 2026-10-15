import React, { useState, useEffect } from 'react';
import { apiClient } from '../api/client';
import { useApp } from '../context/AppContext';
import {
  Settings as SettingsIcon,
  Sliders,
  Shield,
  Satellite,
  Save,
  RotateCcw,
  CheckCircle2,
  AlertTriangle,
  Info,
  Radio,
  Sparkles,
  Key,
  Globe
} from 'lucide-react';

export const SettingsPage: React.FC = () => {
  const { isRealDataMode, setIsRealDataMode } = useApp();

  const [weights, setWeights] = useState({
    disturbance_weight: 25,
    temporal_weight: 20,
    outside_lease_weight: 20,
    vegetation_loss_weight: 10,
    sar_anomaly_weight: 10,
    historical_expansion_weight: 10,
    terrain_context_weight: 5
  });

  const [bufferDistance, setBufferDistance] = useState<number>(500);
  const [copernicusClientId, setCopernicusClientId] = useState<string>('');
  const [copernicusClientSecret, setCopernicusClientSecret] = useState<string>('');
  const [testResult, setTestResult] = useState<any>(null);
  const [testingConnection, setTestingConnection] = useState<boolean>(false);
  const [savedSuccess, setSavedSuccess] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    apiClient.getSettings().then((data) => {
      if (data.risk_weights) {
        setWeights({
          disturbance_weight: data.risk_weights.disturbance_weight,
          temporal_weight: data.risk_weights.temporal_weight,
          outside_lease_weight: data.risk_weights.outside_lease_weight,
          vegetation_loss_weight: data.risk_weights.vegetation_loss_weight,
          sar_anomaly_weight: data.risk_weights.sar_anomaly_weight,
          historical_expansion_weight: data.risk_weights.historical_expansion_weight,
          terrain_context_weight: data.risk_weights.terrain_context_weight
        });
      }
      if (data.buffer_distance_meters) {
        setBufferDistance(data.buffer_distance_meters);
      }
      setLoading(false);
    }).catch(console.error);
  }, []);

  const totalScore = Object.values(weights).reduce((a, b) => a + b, 0);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await apiClient.updateSettings({
        ...weights,
        buffer_distance_m: bufferDistance,
        copernicus_client_id: copernicusClientId,
        copernicus_client_secret: copernicusClientSecret,
        real_data_mode: isRealDataMode
      });
      setSavedSuccess(true);
      setTimeout(() => setSavedSuccess(false), 3500);
    } catch (err) {
      console.error('Error saving settings:', err);
    }
  };

  const handleTestCopernicus = async () => {
    setTestingConnection(true);
    setTestResult(null);
    try {
      const res = await apiClient.testCopernicusConnection();
      setTestResult(res);
    } catch (err: any) {
      setTestResult({ status: 'ERROR', message: err.message || 'Connection failed' });
    } finally {
      setTestingConnection(false);
    }
  };

  const handleReset = () => {
    setWeights({
      disturbance_weight: 25,
      temporal_weight: 20,
      outside_lease_weight: 20,
      vegetation_loss_weight: 10,
      sar_anomaly_weight: 10,
      historical_expansion_weight: 10,
      terrain_context_weight: 5
    });
    setBufferDistance(500);
  };

  return (
    <div className="space-y-6 pb-16">
      {/* Header */}
      <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-blue-50 text-blue-600 rounded-lg">
            <SettingsIcon className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-extrabold text-slate-900 flex items-center gap-2">
              <span>System Settings & Copernicus API Calibration</span>
            </h2>
            <p className="text-xs text-slate-500">
              Configure Copernicus Data Space credentials, 7-factor explainable risk weights, and surveillance buffer parameters.
            </p>
          </div>
        </div>

        {savedSuccess && (
          <div className="flex items-center gap-1.5 text-xs font-bold text-emerald-700 bg-emerald-50 border border-emerald-300 px-3 py-1.5 rounded-lg shadow-xs">
            <CheckCircle2 className="w-4 h-4 text-emerald-600" />
            <span>Settings Successfully Saved!</span>
          </div>
        )}
      </div>

      <form onSubmit={handleSave} className="space-y-6">
        {/* Section 1: Application Mode Selection */}
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-5 space-y-3">
          <div className="flex items-center justify-between pb-2 border-b border-slate-200">
            <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
              <Globe className="w-4 h-4 text-blue-600" />
              <span>Primary Surveillance Mode</span>
            </h3>
            <span className={`text-xs font-bold font-mono px-2.5 py-0.5 rounded-full border ${
              isRealDataMode ? 'bg-emerald-50 text-emerald-700 border-emerald-300' : 'bg-amber-50 text-amber-700 border-amber-300'
            }`}>
              {isRealDataMode ? 'REAL SATELLITE DATA' : 'DEMO MODE'}
            </span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
            <div
              onClick={() => setIsRealDataMode(true)}
              className={`p-4 rounded-xl border transition cursor-pointer ${
                isRealDataMode
                  ? 'border-emerald-600 bg-emerald-50/40 ring-2 ring-emerald-300'
                  : 'border-slate-200 bg-slate-50 hover:bg-slate-100'
              }`}
            >
              <div className="flex items-center gap-2 font-bold text-slate-900 mb-1">
                <span className="w-2 h-2 rounded-full bg-emerald-500" />
                <span>Real Copernicus Satellite Data Mode</span>
              </div>
              <p className="text-slate-500 leading-relaxed">
                Connects live to the official Copernicus Data Space Ecosystem (CDSE) STAC & Catalogue APIs. Disables mock generation and uses real Sentinel observations.
              </p>
            </div>

            <div
              onClick={() => setIsRealDataMode(false)}
              className={`p-4 rounded-xl border transition cursor-pointer ${
                !isRealDataMode
                  ? 'border-amber-600 bg-amber-50/40 ring-2 ring-amber-300'
                  : 'border-slate-200 bg-slate-50 hover:bg-slate-100'
              }`}
            >
              <div className="flex items-center gap-2 font-bold text-slate-900 mb-1">
                <span className="w-2 h-2 rounded-full bg-amber-500" />
                <span>Demonstration Simulation Mode</span>
              </div>
              <p className="text-slate-500 leading-relaxed">
                Loads pre-seeded multi-year mining time-series and cadastral leases for offline presentations and academic showcases.
              </p>
            </div>
          </div>
        </div>

        {/* Section 2: Copernicus API Credentials & Live Test */}
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-5 space-y-4 text-xs">
          <div className="flex flex-wrap items-center justify-between gap-2 pb-2 border-b border-slate-200">
            <div>
              <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                <Key className="w-4 h-4 text-blue-600" />
                <span>Copernicus Data Space Ecosystem (CDSE) API Credentials</span>
              </h3>
              <p className="text-slate-500 text-xs">
                Backend-only authentication. Client secrets are never exposed to the browser.
              </p>
            </div>

            <button
              type="button"
              onClick={handleTestCopernicus}
              disabled={testingConnection}
              className="flex items-center gap-1.5 bg-slate-900 hover:bg-slate-800 text-white font-bold px-3 py-1.5 rounded-lg transition"
            >
              {testingConnection ? (
                <div className="w-3 h-3 border-2 border-white border-t-transparent rounded-full animate-spin" />
              ) : (
                <Satellite className="w-3.5 h-3.5" />
              )}
              <span>Test Live Copernicus Connection</span>
            </button>
          </div>

          {testResult && (
            <div className={`p-3 rounded-lg border text-xs ${
              testResult.status === 'CONNECTED'
                ? 'bg-emerald-50 border-emerald-300 text-emerald-900'
                : 'bg-red-50 border-red-300 text-red-900'
            }`}>
              <div className="font-bold mb-0.5">{testResult.message}</div>
              {testResult.latest_product_name && (
                <div className="font-mono text-[11px] text-slate-600 mt-1">
                  <strong>Latest CDSE Product:</strong> {testResult.latest_product_name} ({testResult.latest_acquisition_date?.slice(0, 10)})
                </div>
              )}
            </div>
          )}

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block font-bold text-slate-700 mb-1">COPERNICUS_CLIENT_ID (Optional)</label>
              <input
                type="text"
                placeholder="Enter CDSE OAuth2 Client ID..."
                value={copernicusClientId}
                onChange={(e) => setCopernicusClientId(e.target.value)}
                className="w-full bg-slate-50 border border-slate-300 rounded-lg p-2 font-mono text-slate-900"
              />
            </div>

            <div>
              <label className="block font-bold text-slate-700 mb-1">COPERNICUS_CLIENT_SECRET (Optional)</label>
              <input
                type="password"
                placeholder="Enter CDSE OAuth2 Client Secret..."
                value={copernicusClientSecret}
                onChange={(e) => setCopernicusClientSecret(e.target.value)}
                className="w-full bg-slate-50 border border-slate-300 rounded-lg p-2 font-mono text-slate-900"
              />
            </div>
          </div>
        </div>

        {/* Section 3: 7-Factor Risk Weight Sliders */}
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-5 space-y-4">
          <div className="flex flex-wrap items-center justify-between gap-2 pb-3 border-b border-slate-200">
            <div>
              <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                <Sliders className="w-4 h-4 text-blue-600" />
                <span>7-Factor Explainable Risk Scoring Model Weights</span>
              </h3>
              <p className="text-xs text-slate-500">
                Adjust factor weight distribution for the 0-100 normalized risk score.
              </p>
            </div>
            <div className={`px-3 py-1 rounded-lg text-xs font-mono font-bold border ${totalScore === 100 ? 'bg-emerald-50 text-emerald-700 border-emerald-300' : 'bg-amber-50 text-amber-700 border-amber-300'}`}>
              Total Weight: {totalScore} / 100 pts
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
            <div className="bg-slate-50 p-3 rounded-lg border border-slate-200 space-y-2">
              <div className="flex justify-between font-bold text-slate-800">
                <span>1. Surface Disturbance Area Weight</span>
                <span className="font-mono text-blue-600">{weights.disturbance_weight} pts</span>
              </div>
              <input
                type="range"
                min="10"
                max="40"
                value={weights.disturbance_weight}
                onChange={(e) => setWeights({ ...weights, disturbance_weight: parseFloat(e.target.value) })}
                className="w-full accent-blue-600"
              />
            </div>

            <div className="bg-slate-50 p-3 rounded-lg border border-slate-200 space-y-2">
              <div className="flex justify-between font-bold text-slate-800">
                <span>2. Multi-Date Temporal Persistence</span>
                <span className="font-mono text-blue-600">{weights.temporal_weight} pts</span>
              </div>
              <input
                type="range"
                min="10"
                max="30"
                value={weights.temporal_weight}
                onChange={(e) => setWeights({ ...weights, temporal_weight: parseFloat(e.target.value) })}
                className="w-full accent-blue-600"
              />
            </div>

            <div className="bg-slate-50 p-3 rounded-lg border border-slate-200 space-y-2">
              <div className="flex justify-between font-bold text-slate-800">
                <span>3. Outside Registered Lease Penalty</span>
                <span className="font-mono text-blue-600">{weights.outside_lease_weight} pts</span>
              </div>
              <input
                type="range"
                min="10"
                max="35"
                value={weights.outside_lease_weight}
                onChange={(e) => setWeights({ ...weights, outside_lease_weight: parseFloat(e.target.value) })}
                className="w-full accent-blue-600"
              />
            </div>

            <div className="bg-slate-50 p-3 rounded-lg border border-slate-200 space-y-2">
              <div className="flex justify-between font-bold text-slate-800">
                <span>4. Vegetation Canopy Loss (NDVI Drop)</span>
                <span className="font-mono text-blue-600">{weights.vegetation_loss_weight} pts</span>
              </div>
              <input
                type="range"
                min="5"
                max="20"
                value={weights.vegetation_loss_weight}
                onChange={(e) => setWeights({ ...weights, vegetation_loss_weight: parseFloat(e.target.value) })}
                className="w-full accent-blue-600"
              />
            </div>

            <div className="bg-slate-50 p-3 rounded-lg border border-slate-200 space-y-2">
              <div className="flex justify-between font-bold text-slate-800">
                <span>5. SAR Radar Anomaly (Roughness Delta)</span>
                <span className="font-mono text-blue-600">{weights.sar_anomaly_weight} pts</span>
              </div>
              <input
                type="range"
                min="5"
                max="20"
                value={weights.sar_anomaly_weight}
                onChange={(e) => setWeights({ ...weights, sar_anomaly_weight: parseFloat(e.target.value) })}
                className="w-full accent-blue-600"
              />
            </div>

            <div className="bg-slate-50 p-3 rounded-lg border border-slate-200 space-y-2">
              <div className="flex justify-between font-bold text-slate-800">
                <span>6. Historical YoY Expansion Vector</span>
                <span className="font-mono text-blue-600">{weights.historical_expansion_weight} pts</span>
              </div>
              <input
                type="range"
                min="5"
                max="20"
                value={weights.historical_expansion_weight}
                onChange={(e) => setWeights({ ...weights, historical_expansion_weight: parseFloat(e.target.value) })}
                className="w-full accent-blue-600"
              />
            </div>
          </div>
        </div>

        {/* Section 4: Configured Surveillance Buffer Distance */}
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-5 space-y-3 text-xs">
          <div className="flex items-center justify-between pb-2 border-b border-slate-200">
            <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
              <Shield className="w-4 h-4 text-amber-500" />
              <span>Configured Cadastral Surveillance Buffer Distance</span>
            </h3>
            <span className="font-mono font-bold text-blue-700 bg-blue-50 border border-blue-200 px-2 py-0.5 rounded">
              {bufferDistance} meters
            </span>
          </div>

          <div className="space-y-2">
            <label className="font-semibold text-slate-700 block">
              Default Perimeter Buffer for Registered Mining Leases:
            </label>
            <input
              type="range"
              min="100"
              max="2000"
              step="50"
              value={bufferDistance}
              onChange={(e) => setBufferDistance(parseInt(e.target.value))}
              className="w-full accent-amber-600"
            />
            <div className="flex justify-between text-[11px] text-slate-400 font-mono">
              <span>100 m</span>
              <span>500 m (Statutory Default)</span>
              <span>2000 m (Extended Basin)</span>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center justify-end gap-3 pt-2">
          <button
            type="button"
            onClick={handleReset}
            className="flex items-center gap-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 px-4 py-2 rounded-lg text-xs font-bold transition border border-slate-300"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Reset Defaults</span>
          </button>
          <button
            type="submit"
            className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-5 rounded-lg text-xs shadow transition"
          >
            <Save className="w-4 h-4" />
            <span>Save Configuration</span>
          </button>
        </div>
      </form>
    </div>
  );
};
