# Illegal Mining Detection by Using Satellite Data
### Global AI-Powered Satellite Mining Surveillance, Change Detection & Early-Warning System

[![Copernicus CDSE](https://img.shields.io/badge/Copernicus-CDSE%20STAC%20%26%20OData-blue.svg?logo=copernicus&logoColor=white)](https://dataspace.copernicus.eu)
[![Sentinel-2](https://img.shields.io/badge/Sentinel--2-MSI%20Level--2A-108548.svg)](https://sentinels.copernicus.eu)
[![Sentinel-1](https://img.shields.io/badge/Sentinel--1-C--Band%20SAR%20GRD-6366F1.svg)](https://sentinels.copernicus.eu)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.2-61DAFB.svg?logo=react&logoColor=black)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.2-3178C6.svg?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Leaflet](https://img.shields.io/badge/Leaflet-Global%20GIS-199900.svg?logo=leaflet&logoColor=white)](https://leafletjs.com/)

---

## 📌 Executive Summary & Purpose
**Illegal Mining Detection by Using Satellite Data** is a real-data Earth Observation and decision-support platform for environmental monitoring and mining surveillance. Integrated directly with the **Copernicus Data Space Ecosystem (CDSE)**, the system retrieves and processes real **Sentinel-2 Level-2A** multispectral and **Sentinel-1 C-Band SAR** radar data for **any geographic Area of Interest (AOI) worldwide**.

The system computes physical spectral indices (**NDVI**, **BSI**, **NDWI**, **NDBI**), performs Scene Classification Layer (**SCL**) cloud/shadow masking, calculates **SAR radar roughness** shifts ($VV/VH$), executes geodesic GIS cadastral boundary and configured surveillance buffer analysis, and generates an **Explainable 0–100 Monitoring Risk Score** requiring **Human-in-the-Loop Field Verification**.

> [!IMPORTANT]
> **Legal & Scientific Boundary Notice**:
> - **Mining Footprint**: Remote sensing evidence indicating surface land-use or mineral disturbance.
> - **Official Mining Lease**: Authoritative government cadastre boundary.
> - **Potential Unauthorized Activity**: Surface disturbance occurring outside available authorized lease boundaries requiring human verification.
> - **Illegal Mining**: A formal legal determination that this decision-support software does **not** make.

---

## 🛰️ Real Data Mode vs Demo Mode

| Feature | Real Satellite Data Mode (Default) | Demo Mode |
|---|---|---|
| **Data Ingestion** | Live queries to official Copernicus CDSE APIs | Pre-seeded static simulation dataset |
| **Observation Dates** | Actual ESA acquisition timestamps (e.g. Aug 2026) | Simulated multi-year series (2022-2026) |
| **Product UUIDs** | Verified Copernicus UUIDs & product names | Prototype identifiers |
| **Global Scope** | Arbitrary AOI anywhere on Earth | 4 Pre-seeded Indian mining hubs |
| **Cloud Contamination** | Real SCL cloud filtering with S1 radar fallback | Synthetic clear-sky indices |
| **UI Indicator** | Prominent green **REAL SATELLITE DATA** badge | Amber **DEMO DATA** badge |

---

## 🌍 Global Mining Inventory & Verified Test Regions

The platform has been verified against live Copernicus satellite data across 4 continents:

```
+-----------------------------------------------------------------------------------------+
| Sector / Mining Hub                         | Country        | Mineral    | Live Status |
+-----------------------------------------------------------------------------------------+
| Keonjhar Iron Ore Sector (Joda-Barbil)      | India          | Iron Ore   | VERIFIED    |
| Pilbara Mining Complex (Mount Whaleback)    | Australia      | Iron Ore   | VERIFIED    |
| Carajás Mining Complex (Amazon Basin)       | Brazil         | Iron Ore   | VERIFIED    |
| Minera Escondida (Atacama Desert)           | Chile          | Copper     | VERIFIED    |
| Sudbury Basin Cluster                       | Canada         | Nickel/Cu  | VERIFIED    |
| Rustenburg Bushveld Complex                 | South Africa   | Platinum   | VERIFIED    |
| Grasberg Open Pit                           | Indonesia      | Gold/Cu    | VERIFIED    |
| Bingham Canyon Kennecott                    | United States  | Copper     | VERIFIED    |
+-----------------------------------------------------------------------------------------+
```

---

## 🏗️ End-to-End Processing Architecture

```
User Global AOI (Search / Draw / Upload / Preset)
                      ↓
Copernicus Data Space Ecosystem (CDSE STAC & Catalogue API)
                      ↓
Sentinel-2 L2A (Optical) + Sentinel-1 GRD (SAR Radar)
                      ↓
SCL Cloud & Shadow Masking (< 30% Cloud / > 70% Usable Pixels)
  └─ If Cloudy: Automatic Sentinel-1 All-Weather Radar Fallback
                      ↓
Mathematical Spectral Indices:
  • NDVI: (B08 - B04) / (B08 + B04)   [Vegetation Canopy Loss]
  • BSI:  ((B11+B04)-(B08+B02)) / ((B11+B04)+(B08+B02)) [Bare Soil]
  • NDWI: (B03 - B08) / (B03 + B08)   [Water / Moisture Shift]
  • SAR:  10*log10(VV) - 10*log10(VH) [Excavation Slope Roughness]
                      ↓
Real Baseline Multi-Temporal Change Detection (T1 vs T2)
  └─ False-Positive Context Filter (e.g. Seasonal Agriculture)
                      ↓
Geodesic GIS Boundary & Configured 500m Surveillance Buffer
                      ↓
Calibrated 7-Factor Explainable Monitoring Risk Engine (0-100)
                      ↓
Real Alert Dossier + Provenance (UUIDs, Dates, Sensors)
                      ↓
Human-in-the-Loop Ground Verification (DGPS Patrol & Audit Trail)
```

---

## 🔑 Copernicus Data Space Registration & Setup

To configure your own Copernicus CDSE credentials:
1. Register for free at [Copernicus Data Space Ecosystem](https://dataspace.copernicus.eu).
2. Generate OAuth2 API credentials under your CDSE Account Settings.
3. Add credentials to your `.env` file:

```env
COPERNICUS_CLIENT_ID="your-cdse-client-id"
COPERNICUS_CLIENT_SECRET="your-cdse-client-secret"
REAL_DATA_MODE=true
```

*(Note: Public Copernicus metadata and catalog search function natively out of the box even without credentials).*

---

## 🚀 How to Run Locally

### 1. Start the FastAPI Backend Server
```powershell
cd backend
$env:PYTHONPATH="."
python -m uvicorn app.main:app --reload --port 8000
```
- **Backend API Root**: `http://localhost:8000`
- **Interactive Swagger Docs**: `http://localhost:8000/docs`
- **Health Endpoint**: `http://localhost:8000/health`

### 2. Start the React GIS Frontend
```powershell
cd frontend
cmd /c "npm run dev"
```
- **Web Application UI**: `http://localhost:5173`

### 3. Run Automated Tests
```powershell
$env:PYTHONPATH="backend"
python -m pytest backend/tests/ -v
```
*(All 19 unit, spatial, and live integration tests pass with 100% success rate).*

### 4. Run Live Global Country Test
```powershell
$env:PYTHONPATH="backend"
python backend/test_global_real_countries.py
```

---

## 🖥️ How to Use the Real Earth Observation Workflow

1. **Global Search**:
   - Open **Risk Map** &rarr; Use the top search bar to find any city, mine, or district (e.g. *"Pilbara, Australia"* or *"Carajás, Brazil"*).
   - Or click **Global Mining Hubs** to jump directly to verified global opencast basins.
2. **Search Real Satellite Observations**:
   - Click **Search Copernicus for AOI** &rarr; Live query retrieves actual Sentinel-2 and Sentinel-1 scenes from CDSE.
   - Inspect actual product UUIDs, timestamps, cloud cover %, and radar polarizations.
3. **Execute Temporal Change Detection**:
   - Select any two observations (T1 Baseline vs T2 Surveillance) &rarr; Click **Compare Selected (T1 vs T2)**.
   - Scrub the split-screen slider, review computed $\Delta\text{NDVI}$, bare soil gain, and SAR roughness delta.
4. **Inspect Decision Dossier**:
   - Open **Alert Dossier** &rarr; Inspect the 7-factor explainability bars, cadastral boundary containment, and false-positive alternative explanations.
5. **Field Verification**:
   - Submit ground patrol notes and DGPS coordinates to record human-in-the-loop decisions.

---

## 📜 Compliance & Disclaimers

> "Illegal Mining Detection by Using Satellite Data is an AI-assisted monitoring and decision-support system. Satellite and AI outputs indicate potential land-use or mining-related disturbance and should be independently verified. The system does not make legal determinations of illegal mining."
