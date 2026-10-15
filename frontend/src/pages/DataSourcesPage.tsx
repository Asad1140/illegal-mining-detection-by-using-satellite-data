import React from 'react';
import {
  Database,
  Satellite,
  Layers,
  CheckCircle2,
  ExternalLink,
  Shield,
  Radio,
  Globe
} from 'lucide-react';

export const DataSourcesPage: React.FC = () => {
  const sources = [
    {
      id: 'src-cdse',
      name: 'Copernicus Data Space Ecosystem (CDSE)',
      source_type: 'PRIMARY SATELLITE API',
      provider: 'European Space Agency (ESA) & European Commission',
      purpose: 'Live STAC Catalog & OData search for Sentinel-1 & Sentinel-2 constellations worldwide.',
      resolution: '10m - 20m Multi-spectral & SAR',
      update_frequency: '5-Day Revisit Time',
      status: 'OPERATIONAL (Live Online)',
      is_live: true,
      url: 'https://dataspace.copernicus.eu'
    },
    {
      id: 'src-s2',
      name: 'Sentinel-2 MSI (Level-2A BOA)',
      source_type: 'OPTICAL MULTISPECTRAL',
      provider: 'ESA / Copernicus',
      purpose: 'Surface reflectance bands (B02-B12) & Scene Classification Layer (SCL) for NDVI, BSI, NDWI & cloud masking.',
      resolution: '10m (B2, B3, B4, B8) / 20m (B11, B12)',
      update_frequency: '5 Days (Constellation 2A/2B/2C)',
      status: 'OPERATIONAL',
      is_live: true,
      url: 'https://sentinels.copernicus.eu/web/sentinel/missions/sentinel-2'
    },
    {
      id: 'src-s1',
      name: 'Sentinel-1 C-Band SAR (Level-1 GRD)',
      source_type: 'SYNTHETIC APERTURE RADAR',
      provider: 'ESA / Copernicus',
      purpose: 'All-weather, cloud-penetrating radar roughness (VV, VH polarizations) for excavation & slope anomaly detection.',
      resolution: '10m Ground Resolution',
      update_frequency: '6 - 12 Days',
      status: 'OPERATIONAL',
      is_live: true,
      url: 'https://sentinels.copernicus.eu/web/sentinel/missions/sentinel-1'
    },
    {
      id: 'src-landsat',
      name: 'USGS / NASA Landsat 8 & 9 OLI/TIRS',
      source_type: 'HISTORICAL ARCHIVE',
      provider: 'USGS / NASA Earth Observation',
      purpose: 'Decadal baseline verification & 30m historical multi-spectral trend analysis.',
      resolution: '30m Multispectral / 15m Panchromatic',
      update_frequency: '16 Days',
      status: 'OPERATIONAL',
      is_live: true,
      url: 'https://landsat.gsfc.nasa.gov'
    },
    {
      id: 'src-global-mines',
      name: 'Global Mining Footprints & Cadastre Inventory',
      source_type: 'GLOBAL GIS VECTOR',
      provider: 'USGS, S&P Global, Geoscience Australia, ANM Brazil, IBM India',
      purpose: 'Reference mining basin coordinates and official cadastral lease boundaries across 8 major mining nations.',
      resolution: 'Vector Polygon Footprints',
      update_frequency: 'Annual / Bi-annual',
      status: 'DATABASE LOADED',
      is_live: true,
      url: 'https://www.usgs.gov/centers/national-minerals-information-center'
    },
    {
      id: 'src-osm',
      name: 'OpenStreetMap Nominatim Geocoder',
      source_type: 'GEOCODING & BASEMAP',
      provider: 'OpenStreetMap Foundation',
      purpose: 'Worldwide place, city, district, and coordinate search with bounding box geometry extraction.',
      resolution: 'Global Street & Polygon Coverage',
      update_frequency: 'Continuous Community Updates',
      status: 'OPERATIONAL',
      is_live: true,
      url: 'https://nominatim.openstreetmap.org'
    }
  ];

  return (
    <div className="space-y-6 pb-16">
      {/* Header */}
      <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-blue-50 text-blue-600 rounded-lg">
            <Database className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-extrabold text-slate-900 flex items-center gap-2">
              <span>Multi-Sensor Earth Observation & GIS Data Sources Catalog</span>
              <span className="text-xs font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                6 Verified Providers
              </span>
            </h2>
            <p className="text-xs text-slate-500">
              Authoritative satellite constellations, global geocoding services, and international mining cadastre datasets.
            </p>
          </div>
        </div>
      </div>

      {/* Sources Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {sources.map((src) => (
          <div key={src.id} className="bg-white rounded-xl border border-slate-200 shadow-sm p-4 space-y-3 flex flex-col justify-between hover:border-slate-300 transition">
            <div className="space-y-2">
              <div className="flex items-start justify-between gap-2">
                <span className="text-[10px] font-bold uppercase tracking-wider text-blue-600 bg-blue-50 px-2 py-0.5 rounded border border-blue-200">
                  {src.source_type}
                </span>
                <span
                  className={`text-[10px] font-bold px-2 py-0.5 rounded border ${
                    src.is_live
                      ? 'bg-emerald-50 text-emerald-700 border-emerald-300'
                      : 'bg-amber-50 text-amber-700 border-amber-300'
                  }`}
                >
                  {src.status}
                </span>
              </div>
              <h3 className="font-bold text-sm text-slate-900">{src.name}</h3>
              <p className="text-xs text-slate-500 leading-relaxed">{src.purpose}</p>
            </div>

            <div className="pt-3 border-t border-slate-100 space-y-1.5 text-xs">
              <div className="flex justify-between text-slate-600">
                <span>Provider:</span>
                <span className="font-semibold text-slate-800 truncate max-w-[170px]">{src.provider}</span>
              </div>
              <div className="flex justify-between text-slate-600">
                <span>Spatial Resolution:</span>
                <span className="font-mono font-semibold text-slate-800">{src.resolution}</span>
              </div>
              <div className="flex justify-between text-slate-600">
                <span>Revisit Frequency:</span>
                <span className="font-semibold text-slate-800">{src.update_frequency}</span>
              </div>
              <div className="pt-1.5 flex justify-end">
                <a
                  href={src.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-1 text-[11px] font-bold text-blue-600 hover:text-blue-800"
                >
                  <span>Official Portal</span>
                  <ExternalLink className="w-3 h-3" />
                </a>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
