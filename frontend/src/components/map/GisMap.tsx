import React, { useEffect, useState } from 'react';
import {
  MapContainer,
  TileLayer,
  GeoJSON,
  useMap
} from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { useApp } from '../../context/AppContext';
import { apiClient } from '../../api/client';
import { GlobalMiningSite, GeocodeResultItem } from '../../types';
import {
  Layers,
  Search,
  Globe,
  Satellite,
  Compass,
  MapPin,
  Sparkles,
  ChevronDown,
  X
} from 'lucide-react';

// Fix default Leaflet icon paths
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

// Map View Recenter Controller
const RecenterMap: React.FC<{ center: [number, number]; zoom: number }> = ({ center, zoom }) => {
  const map = useMap();
  useEffect(() => {
    map.flyTo(center, zoom, { duration: 1.5 });
  }, [center, zoom, map]);
  return null;
};

export const GisMap: React.FC<{ fullScreen?: boolean; onSelectAlert?: (id: string) => void }> = ({
  fullScreen = false
}) => {
  const {
    selectedRegion,
    navigateToAlert,
    isRealDataMode,
    setCurrentPage,
    setActiveAOI
  } = useApp();

  const [gisData, setGisData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [baseMapType, setBaseMapType] = useState<'satellite' | 'street' | 'topo'>('satellite');

  // Global Mining Sites
  const [globalMiningSites, setGlobalMiningSites] = useState<GlobalMiningSite[]>([]);
  const [selectedGlobalSite, setSelectedGlobalSite] = useState<GlobalMiningSite | null>(null);

  // Search & Geocoding
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [searchResults, setSearchResults] = useState<GeocodeResultItem[]>([]);
  const [isSearching, setIsSearching] = useState<boolean>(false);

  // Center & Zoom
  const [currentCenter, setCurrentCenter] = useState<[number, number]>([21.8423, 85.5812]);
  const [currentZoom, setCurrentZoom] = useState<number>(13);

  // 10 GIS Layer Visibility States
  const [layersVisibility, setLayersVisibility] = useState({
    miningLeases: true,
    surveillanceBuffer: true,
    disturbances: true,
    miningPits: true,
    overburdenDumps: true,
    forestClearance: true,
    roads: true,
    waterBodies: true,
    settlements: true
  });

  const [panelOpen, setPanelOpen] = useState<boolean>(false);
  const [globalDrawerOpen, setGlobalDrawerOpen] = useState<boolean>(false);

  // Load global mining presets on mount
  useEffect(() => {
    apiClient.getGlobalMiningSites().then(setGlobalMiningSites).catch(console.error);
  }, []);

  // Load GIS layers when selectedRegion changes
  useEffect(() => {
    setLoading(true);
    apiClient
      .getRegionGisLayers(selectedRegion)
      .then((data) => {
        setGisData(data);
        if (data && data.center) {
          setCurrentCenter([data.center.lat, data.center.lng]);
          setCurrentZoom(data.center.zoom || 13);
        }
        setLoading(false);
      })
      .catch((err) => {
        console.error('Failed to load GIS layers:', err);
        setLoading(false);
      });
  }, [selectedRegion]);

  const toggleLayer = (layerKey: keyof typeof layersVisibility) => {
    setLayersVisibility((prev) => ({ ...prev, [layerKey]: !prev[layerKey] }));
  };

  const handleGlobalSiteSelect = (site: GlobalMiningSite) => {
    setSelectedGlobalSite(site);
    setCurrentCenter([site.center_lat, site.center_lng]);
    setCurrentZoom(site.zoom || 13);
    setGlobalDrawerOpen(false);

    // Set active AOI bbox around site center
    const delta = 0.05;
    setActiveAOI({
      type: 'Polygon',
      coordinates: [[
        [site.center_lng - delta, site.center_lat - delta],
        [site.center_lng + delta, site.center_lat - delta],
        [site.center_lng + delta, site.center_lat + delta],
        [site.center_lng - delta, site.center_lat + delta],
        [site.center_lng - delta, site.center_lat - delta]
      ]]
    });
  };

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;
    setIsSearching(true);
    try {
      const results = await apiClient.geocodeSearch(searchQuery);
      setSearchResults(results);
    } catch (err) {
      console.error('Geocoding search failed:', err);
    } finally {
      setIsSearching(false);
    }
  };

  const handleSelectSearchResult = (item: GeocodeResultItem) => {
    setCurrentCenter([item.lat, item.lon]);
    setCurrentZoom(14);
    setSearchResults([]);
    setSearchQuery(item.display_name.split(',')[0]);

    const delta = 0.04;
    setActiveAOI({
      type: 'Polygon',
      coordinates: [[
        [item.lon - delta, item.lat - delta],
        [item.lon + delta, item.lat - delta],
        [item.lon + delta, item.lat + delta],
        [item.lon - delta, item.lat + delta],
        [item.lon - delta, item.lat - delta]
      ]]
    });
  };

  const handleLaunchCopernicusSearch = () => {
    const delta = 0.04;
    setActiveAOI({
      type: 'Polygon',
      coordinates: [[
        [currentCenter[1] - delta, currentCenter[0] - delta],
        [currentCenter[1] + delta, currentCenter[0] - delta],
        [currentCenter[1] + delta, currentCenter[0] + delta],
        [currentCenter[1] - delta, currentCenter[0] + delta],
        [currentCenter[1] - delta, currentCenter[0] - delta]
      ]]
    });
    setCurrentPage('satellite-analysis');
  };

  // Layer Style Functions
  const leaseStyle = () => ({
    color: '#2563eb',
    weight: 2.5,
    dashArray: '5, 5',
    fillColor: '#3b82f6',
    fillOpacity: 0.12
  });

  const bufferStyle = () => ({
    color: '#eab308',
    weight: 1.8,
    dashArray: '4, 4',
    fillColor: '#facc15',
    fillOpacity: 0.08
  });

  const disturbanceStyle = (feature: any) => {
    const score = feature?.properties?.risk_score || 70;
    const color =
      score >= 75 ? '#dc2626' : score >= 50 ? '#f97316' : score >= 25 ? '#eab308' : '#16a34a';
    return {
      color: color,
      weight: 3,
      fillColor: color,
      fillOpacity: 0.45
    };
  };

  return (
    <div
      className={`relative w-full rounded-xl overflow-hidden border border-slate-200 shadow-sm bg-slate-900 ${
        fullScreen ? 'h-[calc(100vh-125px)]' : 'h-[520px]'
      }`}
    >
      {loading && (
        <div className="absolute inset-0 bg-slate-900/60 backdrop-blur-xs z-30 flex items-center justify-center text-white">
          <div className="flex items-center gap-3 bg-slate-900/90 px-4 py-2.5 rounded-lg border border-slate-700 shadow-xl">
            <div className="w-4 h-4 border-2 border-blue-400 border-t-transparent rounded-full animate-spin"></div>
            <span className="text-sm font-semibold">Loading High-Resolution GIS Vector Layers...</span>
          </div>
        </div>
      )}

      {/* Map Tile Container */}
      <MapContainer
        center={currentCenter}
        zoom={currentZoom}
        className="w-full h-full z-10"
        scrollWheelZoom={true}
      >
        <RecenterMap center={currentCenter} zoom={currentZoom} />

        {/* Base Map Switcher */}
        {baseMapType === 'satellite' && (
          <TileLayer
            attribution="&copy; Esri &mdash; World Imagery"
            url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
            maxZoom={18}
          />
        )}
        {baseMapType === 'street' && (
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            maxZoom={19}
          />
        )}
        {baseMapType === 'topo' && (
          <TileLayer
            attribution='&copy; <a href="https://carto.com/">CartoDB</a> Dark Matter'
            url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png"
            maxZoom={19}
          />
        )}

        {/* GIS Vector Layers */}
        {gisData && (
          <>
            {/* 1. Official Mining Leases */}
            {layersVisibility.miningLeases && gisData.mining_leases && (
              <GeoJSON
                key={`leases-${selectedRegion}`}
                data={gisData.mining_leases}
                style={leaseStyle}
                onEachFeature={(feature, layer) => {
                  const p = feature.properties;
                  layer.bindPopup(`
                    <div style="font-family: sans-serif; min-width: 220px; font-size: 12px;">
                      <div style="font-weight: bold; color: #1e3a8a; border-bottom: 1px solid #cbd5e1; padding-bottom: 4px; margin-bottom: 6px;">
                        ${p.name || 'Official Mining Lease'}
                      </div>
                      <div><strong>Lease ID:</strong> ${p.lease_id}</div>
                      <div><strong>Lessee:</strong> ${p.lessee || 'Registered Lessee'}</div>
                      <div><strong>Mineral:</strong> ${p.mineral || 'Iron Ore'}</div>
                      <div><strong>Approved Area:</strong> ${p.area_ha || 0} ha</div>
                      <div><strong>Status:</strong> <span style="color: #16a34a; font-weight: bold;">AUTHORIZED LEASE</span></div>
                    </div>
                  `);
                }}
              />
            )}

            {/* 2. 500m Surveillance Buffer */}
            {layersVisibility.surveillanceBuffer && gisData.surveillance_buffers && (
              <GeoJSON
                key={`buffer-${selectedRegion}`}
                data={gisData.surveillance_buffers}
                style={bufferStyle}
              />
            )}

            {/* 3. Detected Mining Disturbances & Risk Zones */}
            {layersVisibility.disturbances && gisData.disturbances && (
              <GeoJSON
                key={`disturbances-${selectedRegion}`}
                data={gisData.disturbances}
                style={disturbanceStyle}
                onEachFeature={(feature, layer) => {
                  const p = feature.properties;
                  layer.bindPopup(`
                    <div style="font-family: sans-serif; width: 260px; font-size: 12px; color: #1e293b;">
                      <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #e2e8f0; padding-bottom: 6px; margin-bottom: 6px;">
                        <span style="font-weight: 800; color: #b91c1c; font-size: 13px;">ALERT #${p.alert_id}</span>
                        <span style="background: #fee2e2; color: #991b1b; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 10px;">${p.priority}</span>
                      </div>
                      <div style="margin-bottom: 4px;"><strong>Location:</strong> ${selectedRegion}</div>
                      <div style="margin-bottom: 4px;"><strong>Risk Score:</strong> <span style="font-weight: 800; color: #dc2626;">${p.risk_score}/100</span></div>
                      <div style="margin-bottom: 4px;"><strong>Disturbed Area:</strong> ${p.disturbed_area_ha} hectares</div>
                      <div style="margin-bottom: 4px;"><strong>Lease Relationship:</strong> <span style="color: #b91c1c; font-weight: 600;">${p.lease_status}</span></div>
                      <div style="margin-bottom: 4px;"><strong>Distance from Lease:</strong> ${p.distance_from_lease_m} m</div>
                      <div style="margin-bottom: 4px;"><strong>Detection Date:</strong> ${p.detection_date}</div>
                      <div style="margin-bottom: 6px;"><strong>Status:</strong> ${p.status}</div>
                      <div style="border-top: 1px solid #e2e8f0; padding-top: 6px; text-align: center;">
                        <a href="#alert-dossier" id="btn-view-dossier-${p.alert_id}" style="display: block; background: #2563eb; color: #fff; padding: 5px 8px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 11px;">
                          View Explainable Dossier &rarr;
                        </a>
                      </div>
                    </div>
                  `);
                  layer.on('popupopen', () => {
                    const btn = document.getElementById(`btn-view-dossier-${p.alert_id}`);
                    if (btn) {
                      btn.onclick = (e) => {
                        e.preventDefault();
                        navigateToAlert(p.alert_id);
                      };
                    }
                  });
                }}
              />
            )}
          </>
        )}
      </MapContainer>

      {/* Top Floating Bar: Global Geocoding & Mining Presets */}
      <div className="absolute top-3 left-3 z-20 flex flex-wrap items-center gap-2 max-w-xl">
        {/* Place Search Bar */}
        <div className="relative">
          <form onSubmit={handleSearch} className="flex items-center bg-slate-900/95 backdrop-blur-md rounded-lg border border-slate-700 shadow-xl overflow-hidden text-xs">
            <input
              type="text"
              placeholder="Search worldwide city, mine, or coords..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="bg-transparent text-white px-3 py-2 w-56 sm:w-64 focus:outline-none placeholder-slate-400"
            />
            <button
              type="submit"
              className="px-2.5 py-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold flex items-center gap-1 transition"
            >
              {isSearching ? <div className="w-3 h-3 border-2 border-white border-t-transparent rounded-full animate-spin" /> : <Search className="w-3.5 h-3.5" />}
            </button>
          </form>

          {/* Autocomplete Dropdown */}
          {searchResults.length > 0 && (
            <div className="absolute top-full left-0 right-0 mt-1 bg-slate-900/95 backdrop-blur-md rounded-lg border border-slate-700 shadow-2xl p-1 z-30 max-h-48 overflow-y-auto">
              <div className="flex justify-between items-center px-2 py-1 text-[10px] text-slate-400 font-semibold border-b border-slate-800">
                <span>Location Matches ({searchResults.length})</span>
                <button onClick={() => setSearchResults([])} className="hover:text-white"><X className="w-3 h-3" /></button>
              </div>
              {searchResults.map((r, i) => (
                <button
                  key={i}
                  onClick={() => handleSelectSearchResult(r)}
                  className="w-full text-left px-2 py-1.5 hover:bg-blue-600/30 text-slate-200 text-xs rounded transition flex items-start gap-1.5"
                >
                  <MapPin className="w-3.5 h-3.5 text-blue-400 shrink-0 mt-0.5" />
                  <span className="truncate">{r.display_name}</span>
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Global Mining Hubs Preset Dropdown */}
        <div className="relative">
          <button
            onClick={() => setGlobalDrawerOpen(!globalDrawerOpen)}
            className="flex items-center gap-1.5 bg-slate-900/95 backdrop-blur-md text-white px-3 py-2 rounded-lg border border-slate-700 shadow-xl hover:bg-slate-800 text-xs font-semibold transition"
          >
            <Globe className="w-3.5 h-3.5 text-emerald-400" />
            <span>{selectedGlobalSite ? selectedGlobalSite.name.split('(')[0] : 'Global Mining Hubs'}</span>
            <ChevronDown className="w-3 h-3 text-slate-400" />
          </button>

          {globalDrawerOpen && (
            <div className="absolute top-full left-0 mt-1 bg-slate-900/95 backdrop-blur-md rounded-xl border border-slate-700 shadow-2xl p-2 z-30 w-72 text-xs max-h-64 overflow-y-auto">
              <div className="text-[10px] font-bold uppercase tracking-wider text-slate-400 px-2 py-1 border-b border-slate-800 mb-1">
                Global Monitored Mining Basins
              </div>
              <div className="space-y-1">
                {globalMiningSites.map((site) => (
                  <button
                    key={site.id}
                    onClick={() => handleGlobalSiteSelect(site)}
                    className="w-full text-left p-2 rounded-lg hover:bg-slate-800 text-slate-200 hover:text-white transition flex justify-between items-center"
                  >
                    <div>
                      <div className="font-bold text-white flex items-center gap-1.5">
                        <span>{site.name}</span>
                      </div>
                      <div className="text-[11px] text-slate-400">{site.country} &bull; {site.mineral}</div>
                    </div>
                    <span className={`text-[9px] font-mono px-1.5 py-0.5 rounded ${site.has_authoritative_lease ? 'bg-blue-500/20 text-blue-300' : 'bg-slate-800 text-slate-400'}`}>
                      {site.has_authoritative_lease ? 'Lease CAD' : 'Footprint'}
                    </span>
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Live Copernicus Sentinel Search Action */}
        <button
          onClick={handleLaunchCopernicusSearch}
          className="flex items-center gap-1.5 bg-blue-600 hover:bg-blue-700 text-white px-3 py-2 rounded-lg shadow-xl text-xs font-bold transition"
        >
          <Satellite className="w-3.5 h-3.5" />
          <span>Search Copernicus for AOI</span>
        </button>
      </div>

      {/* Top Right: Layer Visibility & Base Map Switcher */}
      <div className="absolute top-3 right-3 z-20 flex items-center gap-2">
        <div className="flex items-center bg-slate-900/90 p-1 rounded-lg border border-slate-700 shadow-lg text-xs font-semibold text-white">
          <button
            onClick={() => setBaseMapType('satellite')}
            className={`px-2 py-1 rounded transition ${baseMapType === 'satellite' ? 'bg-blue-600 text-white' : 'text-slate-300 hover:text-white'}`}
          >
            Satellite
          </button>
          <button
            onClick={() => setBaseMapType('street')}
            className={`px-2 py-1 rounded transition ${baseMapType === 'street' ? 'bg-blue-600 text-white' : 'text-slate-300 hover:text-white'}`}
          >
            Street
          </button>
        </div>

        <button
          onClick={() => setPanelOpen(!panelOpen)}
          className="flex items-center gap-1.5 bg-slate-900/90 text-white px-3 py-2 rounded-lg border border-slate-700 shadow-lg hover:bg-slate-800 text-xs font-semibold transition"
        >
          <Layers className="w-3.5 h-3.5 text-blue-400" />
          <span>Layers</span>
        </button>
      </div>
    </div>
  );
};
