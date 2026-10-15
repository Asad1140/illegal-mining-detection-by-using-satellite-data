import React, { useState, useEffect } from 'react';
import { useApp } from '../context/AppContext';
import { apiClient } from '../api/client';
import {
  SatelliteObservation,
  PreprocessingStep,
  RealSatelliteObservationItem
} from '../types';
import {
  Satellite,
  Layers,
  Calendar,
  CloudSun,
  Radio,
  CheckCircle2,
  Sliders,
  Info,
  Search,
  ArrowRight,
  GitCompare,
  Sparkles,
  AlertTriangle,
  FileCode
} from 'lucide-react';

export const SatelliteTimelinePage: React.FC = () => {
  const { selectedRegion, isRealDataMode, setCurrentPage, activeAOI } = useApp();

  // Real Copernicus Catalog State
  const [realObservations, setRealObservations] = useState<RealSatelliteObservationItem[]>([]);
  const [isSearchingReal, setIsSearchingReal] = useState<boolean>(false);
  const [searchError, setSearchError] = useState<string | null>(null);
  const [sensors, setSensors] = useState<string[]>(['sentinel-2', 'sentinel-1']);
  const [startDate, setStartDate] = useState<string>('2024-01-01');
  const [endDate, setEndDate] = useState<string>('2026-08-25');
  const [maxCloudCover, setMaxCloudCover] = useState<number>(30.0);
  const [selectedObsIds, setSelectedObsIds] = useState<string[]>([]);

  // Demo Fallback State
  const [timeline, setTimeline] = useState<SatelliteObservation[]>([]);
  const [selectedYear, setSelectedYear] = useState<number>(2026);
  const [preprocessingSteps, setPreprocessingSteps] = useState<PreprocessingStep[]>([]);
  const [cloudMaskActive, setCloudMaskActive] = useState<boolean>(true);
  const [loadingDemo, setLoadingDemo] = useState<boolean>(true);

  // Search real Copernicus data
  const handleFetchRealSatelliteData = async () => {
    setIsSearchingReal(true);
    setSearchError(null);
    try {
      const resp = await apiClient.searchSatelliteCatalog({
        aoi_geojson: activeAOI,
        point: [85.58, 21.84], // Default to center of sector
        start_date: startDate,
        end_date: endDate,
        sensors: sensors,
        max_cloud_cover: maxCloudCover,
        limit: 15
      });
      setRealObservations(resp.observations);
      if (resp.observations.length >= 2) {
        setSelectedObsIds([resp.observations[resp.observations.length - 1].product_id, resp.observations[0].product_id]);
      }
    } catch (err: any) {
      setSearchError(err.message || 'Failed to connect to Copernicus Data Space Ecosystem');
    } finally {
      setIsSearchingReal(false);
    }
  };

  useEffect(() => {
    if (isRealDataMode) {
      handleFetchRealSatelliteData();
    } else {
      setLoadingDemo(true);
      Promise.all([
        apiClient.getSatelliteTimeline(selectedRegion),
        apiClient.getPreprocessingStatus()
      ])
        .then(([timelineData, prepData]) => {
          setTimeline(timelineData);
          setPreprocessingSteps(prepData.steps);
          setLoadingDemo(false);
        })
        .catch(console.error);
    }
  }, [selectedRegion, isRealDataMode]);

  const toggleSensor = (sensorName: string) => {
    if (sensors.includes(sensorName)) {
      if (sensors.length > 1) setSensors(sensors.filter((s) => s !== sensorName));
    } else {
      setSensors([...sensors, sensorName]);
    }
  };

  const toggleObsSelection = (id: string) => {
    if (selectedObsIds.includes(id)) {
      setSelectedObsIds(selectedObsIds.filter((x) => x !== id));
    } else {
      if (selectedObsIds.length >= 2) {
        setSelectedObsIds([selectedObsIds[1], id]);
      } else {
        setSelectedObsIds([...selectedObsIds, id]);
      }
    }
  };

  const handleLaunchCompare = () => {
    setCurrentPage('change-detection');
  };

  const currentObs = timeline.find((o) => o.year === selectedYear) || timeline[timeline.length - 1];

  return (
    <div className="space-y-6 pb-16">
      {/* Top Header */}
      <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-blue-50 text-blue-600 rounded-lg">
            <Satellite className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-extrabold text-slate-900 flex items-center gap-2">
              <span>Multi-Sensor Satellite Timeline & Observations</span>
              <span className={`text-xs font-bold px-2 py-0.5 rounded border ${
                isRealDataMode ? 'bg-emerald-50 text-emerald-700 border-emerald-300' : 'bg-amber-50 text-amber-700 border-amber-300'
              }`}>
                {isRealDataMode ? 'REAL COPERNICUS DATA' : 'DEMO DATA'}
              </span>
            </h2>
            <p className="text-xs text-slate-500">
              {isRealDataMode
                ? 'Directly querying official Copernicus Data Space Ecosystem (CDSE) STAC & Catalogue APIs.'
                : 'Prototype Simulation & Demonstration Dataset (2022-2026).'}
            </p>
          </div>
        </div>

        {isRealDataMode && selectedObsIds.length === 2 && (
          <button
            onClick={handleLaunchCompare}
            className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-xs font-bold shadow-md transition"
          >
            <GitCompare className="w-4 h-4" />
            <span>Compare Selected (T1 vs T2) &rarr;</span>
          </button>
        )}
      </div>

      {/* REAL DATA MODE VIEW */}
      {isRealDataMode ? (
        <div className="space-y-6">
          {/* Query Filter Bar */}
          <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-4 space-y-4">
            <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-3">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center gap-1.5">
                <Sliders className="w-4 h-4 text-blue-600" />
                <span>Copernicus Catalog Query Filters</span>
              </span>
              <button
                onClick={handleFetchRealSatelliteData}
                disabled={isSearchingReal}
                className="flex items-center gap-1.5 bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold px-3 py-1.5 rounded-lg shadow-xs transition"
              >
                {isSearchingReal ? <div className="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin" /> : <Search className="w-3.5 h-3.5" />}
                <span>Refresh Live Search</span>
              </button>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 text-xs">
              {/* Sensors toggle */}
              <div>
                <label className="font-semibold text-slate-700 block mb-1.5">Missions & Sensors:</label>
                <div className="flex gap-2">
                  <button
                    type="button"
                    onClick={() => toggleSensor('sentinel-2')}
                    className={`px-2.5 py-1.5 rounded-lg font-bold border transition ${
                      sensors.includes('sentinel-2')
                        ? 'bg-blue-50 text-blue-700 border-blue-300'
                        : 'bg-slate-50 text-slate-400 border-slate-200'
                    }`}
                  >
                    Sentinel-2 (MSI)
                  </button>
                  <button
                    type="button"
                    onClick={() => toggleSensor('sentinel-1')}
                    className={`px-2.5 py-1.5 rounded-lg font-bold border transition ${
                      sensors.includes('sentinel-1')
                        ? 'bg-indigo-50 text-indigo-700 border-indigo-300'
                        : 'bg-slate-50 text-slate-400 border-slate-200'
                    }`}
                  >
                    Sentinel-1 (SAR)
                  </button>
                </div>
              </div>

              {/* Date Range */}
              <div>
                <label className="font-semibold text-slate-700 block mb-1.5">Acquisition Start Date:</label>
                <input
                  type="date"
                  value={startDate}
                  onChange={(e) => setStartDate(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded-lg p-1.5 text-xs text-slate-800 font-mono"
                />
              </div>

              <div>
                <label className="font-semibold text-slate-700 block mb-1.5">Acquisition End Date:</label>
                <input
                  type="date"
                  value={endDate}
                  onChange={(e) => setEndDate(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded-lg p-1.5 text-xs text-slate-800 font-mono"
                />
              </div>

              {/* Max Cloud Cover Slider */}
              <div>
                <div className="flex justify-between font-semibold text-slate-700 mb-1">
                  <span>Max Cloud Cover:</span>
                  <span className="font-mono text-blue-600 font-bold">{maxCloudCover}%</span>
                </div>
                <input
                  type="range"
                  min="5"
                  max="100"
                  step="5"
                  value={maxCloudCover}
                  onChange={(e) => setMaxCloudCover(parseFloat(e.target.value))}
                  className="w-full accent-blue-600"
                />
              </div>
            </div>
          </div>

          {/* Search Error Notice */}
          {searchError && (
            <div className="p-4 bg-red-50 border border-red-200 rounded-xl text-red-700 text-xs flex items-start gap-2.5">
              <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5" />
              <div>
                <div className="font-bold">Satellite Ingestion Notice</div>
                <div>{searchError}</div>
              </div>
            </div>
          )}

          {/* Real Observations Cards Grid */}
          <div className="space-y-3">
            <div className="flex justify-between items-center text-xs">
              <span className="font-bold text-slate-700 uppercase tracking-wider">
                Copernicus Data Space Ecosystem Observations ({realObservations.length} Found)
              </span>
              <span className="text-slate-500 font-medium">Select any 2 observations to execute change detection</span>
            </div>

            {isSearchingReal ? (
              <div className="p-12 text-center text-slate-400 bg-white rounded-xl border border-slate-200">
                <div className="w-6 h-6 border-2 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-2" />
                <span className="text-xs font-semibold">Querying live Copernicus Catalogue APIs...</span>
              </div>
            ) : realObservations.length === 0 ? (
              <div className="p-8 text-center text-slate-500 bg-white rounded-xl border border-slate-200 text-xs">
                No Sentinel observations found for the selected parameters. Try expanding the date range or increasing max cloud cover.
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {realObservations.map((obs) => {
                  const isSelected = selectedObsIds.includes(obs.product_id);
                  const isOptical = obs.mission === 'Sentinel-2';

                  return (
                    <div
                      key={obs.product_id}
                      onClick={() => toggleObsSelection(obs.product_id)}
                      className={`bg-white rounded-xl border p-4 transition cursor-pointer relative shadow-xs hover:shadow-md ${
                        isSelected
                          ? 'border-blue-600 ring-2 ring-blue-400 bg-blue-50/20'
                          : 'border-slate-200 hover:border-slate-300'
                      }`}
                    >
                      {/* Top Header */}
                      <div className="flex items-start justify-between gap-2 mb-2">
                        <div className="flex items-center gap-2">
                          <div className={`p-1.5 rounded-lg ${isOptical ? 'bg-blue-100 text-blue-700' : 'bg-indigo-100 text-indigo-700'}`}>
                            {isOptical ? <Satellite className="w-4 h-4" /> : <Radio className="w-4 h-4" />}
                          </div>
                          <div>
                            <span className="font-extrabold text-xs text-slate-900 block">{obs.mission}</span>
                            <span className="text-[10px] text-slate-400 font-medium">{obs.processing_level}</span>
                          </div>
                        </div>

                        <span className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded-full ${
                          isSelected ? 'bg-blue-600 text-white' : 'bg-slate-100 text-slate-600'
                        }`}>
                          {isSelected ? 'SELECTED' : 'SELECT'}
                        </span>
                      </div>

                      {/* Product Details */}
                      <div className="space-y-1.5 text-xs text-slate-600">
                        <div className="flex justify-between">
                          <span className="text-slate-400">Acquired:</span>
                          <span className="font-mono font-bold text-slate-800">{obs.acquisition_date.replace('T', ' ').slice(0, 19)} UTC</span>
                        </div>

                        {isOptical ? (
                          <div className="flex justify-between">
                            <span className="text-slate-400">Cloud Cover:</span>
                            <span className={`font-mono font-bold ${(obs.cloud_cover || 0) > 30 ? 'text-amber-600' : 'text-emerald-600'}`}>
                              {obs.cloud_cover !== undefined ? `${obs.cloud_cover}%` : 'N/A'}
                            </span>
                          </div>
                        ) : (
                          <div className="flex justify-between">
                            <span className="text-slate-400">Polarizations:</span>
                            <span className="font-mono font-bold text-indigo-700">{obs.polarisation_channels || 'VV+VH'}</span>
                          </div>
                        )}

                        <div className="pt-2 border-t border-slate-100 text-[10px] text-slate-400">
                          <span className="block truncate font-mono" title={obs.product_name}>
                            <strong>Product:</strong> {obs.product_name}
                          </span>
                          <span className="block truncate font-mono text-[9px] text-slate-400">
                            UUID: {obs.product_id}
                          </span>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </div>
      ) : (
        /* DEMO MODE VIEW */
        <div className="space-y-6">
          <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-4 space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-500">
                Demo Multi-Temporal Acquisition Series (2022 - 2026)
              </span>
              <span className="text-xs font-mono text-slate-400">Co-registered 10m Ground Grid</span>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-5 gap-2.5">
              {timeline.map((obs) => {
                const isSelected = obs.year === selectedYear;
                return (
                  <button
                    key={obs.year}
                    onClick={() => setSelectedYear(obs.year)}
                    className={`p-3 rounded-xl border text-left transition ${
                      isSelected
                        ? 'bg-blue-600 text-white border-blue-600 shadow-md ring-2 ring-blue-300'
                        : 'bg-slate-50 hover:bg-slate-100 border-slate-200 text-slate-800'
                    }`}
                  >
                    <div className="flex items-center justify-between text-xs font-mono font-extrabold mb-1">
                      <span>{obs.year}</span>
                      <span className={`text-[10px] px-1.5 py-0.2 rounded font-sans ${isSelected ? 'bg-white/20 text-white' : 'bg-slate-200 text-slate-700'}`}>
                        {obs.acquisition_date}
                      </span>
                    </div>
                    <div className={`text-xs font-bold truncate ${isSelected ? 'text-blue-100' : 'text-slate-700'}`}>
                      {obs.status}
                    </div>
                    <div className={`text-[11px] font-mono mt-1 ${isSelected ? 'text-blue-200' : 'text-slate-500'}`}>
                      NDVI: {obs.mean_ndvi} &bull; {obs.disturbed_area_ha} ha
                    </div>
                  </button>
                );
              })}
            </div>
          </div>

          {currentObs && (
            <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-4 space-y-3">
              <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                <Layers className="w-4 h-4 text-blue-600" />
                <span>Radiometric Band Reflection Values ({currentObs.year})</span>
              </h3>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5 text-xs font-mono">
                <div className="bg-slate-50 p-2.5 rounded-lg border border-slate-200">
                  <span className="text-[10px] text-slate-400 uppercase font-sans">B2 (Blue)</span>
                  <div className="font-bold text-slate-800 text-sm mt-0.5">{currentObs.band_values?.B2 || 0.08}</div>
                </div>
                <div className="bg-slate-50 p-2.5 rounded-lg border border-slate-200">
                  <span className="text-[10px] text-slate-400 uppercase font-sans">B4 (Red)</span>
                  <div className="font-bold text-slate-800 text-sm mt-0.5">{currentObs.band_values?.B4 || 0.16}</div>
                </div>
                <div className="bg-slate-50 p-2.5 rounded-lg border border-slate-200">
                  <span className="text-[10px] text-slate-400 uppercase font-sans">B8 (NIR)</span>
                  <div className="font-bold text-slate-800 text-sm mt-0.5">{currentObs.band_values?.B8 || 0.22}</div>
                </div>
                <div className="bg-slate-50 p-2.5 rounded-lg border border-slate-200">
                  <span className="text-[10px] text-slate-400 uppercase font-sans">SAR VV (Co-Pol)</span>
                  <div className="font-bold text-indigo-700 text-sm mt-0.5">{currentObs.band_values?.VV || -11.2} dB</div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
