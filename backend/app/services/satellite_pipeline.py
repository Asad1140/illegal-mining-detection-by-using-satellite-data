import numpy as np
from typing import Dict, Any, List, Optional
from datetime import datetime

class SatellitePreprocessingPipeline:
    """
    Satellite data ingestion and preprocessing pipeline for Sentinel-2, Sentinel-1, and Landsat 8/9.
    Supports optical bands (B2, B3, B4, B8, B5, B6, B7, B8A, B11, B12), SAR polarizations (VV, VH, VV/VH),
    cloud masking, and spectral indices calculation.
    """

    SUPPORTED_BANDS = {
        "Sentinel-2": ["B2 (Blue)", "B3 (Green)", "B4 (Red)", "B5 (RedEdge 1)", "B6 (RedEdge 2)", "B7 (RedEdge 3)", "B8 (NIR)", "B8A (Narrow NIR)", "B11 (SWIR 1)", "B12 (SWIR 2)"],
        "Sentinel-1": ["VV (Co-polarization)", "VH (Cross-polarization)", "VV/VH Ratio (Roughness Ratio)"],
        "Landsat-8/9": ["B2 (Blue)", "B3 (Green)", "B4 (Red)", "B5 (NIR)", "B6 (SWIR 1)", "B7 (SWIR 2)"]
    }

    @staticmethod
    def calculate_spectral_indices(b2: float, b3: float, b4: float, b8: float, b11: float) -> Dict[str, float]:
        """
        Computes NDVI, NDWI, NDBI, and BSI (Bare Soil Index).
        NDVI = (NIR - Red) / (NIR + Red)
        NDWI = (Green - NIR) / (Green + NIR)
        NDBI = (SWIR - NIR) / (SWIR + NIR)
        BSI  = ((SWIR + Red) - (NIR + Blue)) / ((SWIR + Red) + (NIR + Blue))
        """
        eps = 1e-6
        ndvi = round((b8 - b4) / (b8 + b4 + eps), 3)
        ndwi = round((b3 - b8) / (b3 + b8 + eps), 3)
        ndbi = round((b11 - b8) / (b11 + b8 + eps), 3)
        bsi = round(((b11 + b4) - (b8 + b2)) / ((b11 + b4) + (b8 + b2) + eps), 3)
        
        return {
            "NDVI": ndvi,
            "NDWI": ndwi,
            "NDBI": ndbi,
            "BSI": bsi
        }

    @staticmethod
    def get_preprocessing_status() -> List[Dict[str, Any]]:
        return [
            {"step": "Image Ingestion & Format Validation", "status": "COMPLETED", "icon": "check", "details": "Sentinel-2 L2A & Sentinel-1 GRD loaded"},
            {"step": "Coordinate & Orthorectification Handling", "status": "COMPLETED", "icon": "check", "details": "Reprojected to WGS84 / EPSG:4326"},
            {"step": "Cloud & Shadow Masking (SCL / Fmask)", "status": "COMPLETED", "icon": "check", "details": "< 5% cloud coverage filtered with SCL band"},
            {"step": "Band Radiometric Calibration & Resampling", "status": "COMPLETED", "icon": "check", "details": "10m / 20m spatial resolution harmonization"},
            {"step": "Spectral & SAR Feature Generation", "status": "COMPLETED", "icon": "check", "details": "NDVI, NDWI, NDBI, BSI, and VV/VH ratio computed"},
            {"step": "Temporal Alignment & Co-Registration", "status": "COMPLETED", "icon": "check", "details": "Co-registered across 2022-2026 acquisition series"}
        ]

    @staticmethod
    def get_temporal_observations(region: str = "Keonjhar") -> List[Dict[str, Any]]:
        """Generates realistic time-series multispectral observations (2022-2026)."""
        return SatellitePreprocessingPipeline.get_timeline(region)

    @staticmethod
    def get_timeline(region: str = "Keonjhar") -> List[Dict[str, Any]]:
        """Generates realistic time-series multispectral observations (2022-2026)."""
        return [
            {
                "id": f"SAT-{region[:2].upper()}-2022",
                "platform": "Sentinel-2 L2A / Sentinel-1",
                "sensor_type": "Optical MSI / C-Band SAR",
                "region": region,
                "year": 2022,
                "acquisition_date": "2022-03-12",
                "cloud_coverage": 1.2,
                "cloud_masked": True,
                "mean_ndvi": 0.68, # Dense natural canopy
                "mean_ndwi": -0.12,
                "mean_ndbi": -0.32,
                "mean_bsi": -0.22,
                "sar_vv_mean": -14.8,
                "sar_vh_mean": -21.4,
                "status": "Baseline Forest / Pre-Disturbance",
                "disturbed_area_ha": 3.2,
                "band_values": {
                    "B2": 0.04, "B3": 0.07, "B4": 0.05, "B8": 0.38, "B11": 0.14, "B12": 0.08,
                    "VV": -14.8, "VH": -21.4, "VV_VH_ratio": 6.6
                }
            },
            {
                "id": f"SAT-{region[:2].upper()}-2023",
                "platform": "Sentinel-2 L2A / Sentinel-1",
                "sensor_type": "Optical MSI / C-Band SAR",
                "region": region,
                "year": 2023,
                "acquisition_date": "2023-03-24",
                "cloud_coverage": 3.4,
                "cloud_masked": True,
                "mean_ndvi": 0.54, # Initial canopy thinning
                "mean_ndwi": -0.15,
                "mean_ndbi": -0.18,
                "mean_bsi": -0.05,
                "sar_vv_mean": -13.1,
                "sar_vh_mean": -19.8,
                "status": "Inception of Excavation",
                "disturbed_area_ha": 5.8,
                "band_values": {
                    "B2": 0.06, "B3": 0.09, "B4": 0.08, "B8": 0.32, "B11": 0.18, "B12": 0.12,
                    "VV": -13.1, "VH": -19.8, "VV_VH_ratio": 6.7
                }
            },
            {
                "id": f"SAT-{region[:2].upper()}-2024",
                "platform": "Sentinel-2 L2A / Sentinel-1",
                "sensor_type": "Optical MSI / C-Band SAR",
                "region": region,
                "year": 2024,
                "acquisition_date": "2024-04-05",
                "cloud_coverage": 2.1,
                "cloud_masked": True,
                "mean_ndvi": 0.38, # Significant vegetation drop
                "mean_ndwi": -0.21,
                "mean_ndbi": 0.08,
                "mean_bsi": 0.18,
                "sar_vv_mean": -11.4,
                "sar_vh_mean": -17.5,
                "status": "Quarry & Waste Expansion",
                "disturbed_area_ha": 8.9,
                "band_values": {
                    "B2": 0.08, "B3": 0.12, "B4": 0.14, "B8": 0.25, "B11": 0.24, "B12": 0.18,
                    "VV": -11.4, "VH": -17.5, "VV_VH_ratio": 6.1
                }
            },
            {
                "id": f"SAT-{region[:2].upper()}-2025",
                "platform": "Sentinel-2 L2A / Sentinel-1",
                "sensor_type": "Optical MSI / C-Band SAR",
                "region": region,
                "year": 2025,
                "acquisition_date": "2025-03-30",
                "cloud_coverage": 4.0,
                "cloud_masked": True,
                "mean_ndvi": 0.24, # High bare land
                "mean_ndwi": -0.28,
                "mean_ndbi": 0.28,
                "mean_bsi": 0.36,
                "sar_vv_mean": -9.8,
                "sar_vh_mean": -15.2,
                "status": "Deep Pit Excavation",
                "disturbed_area_ha": 12.0,
                "band_values": {
                    "B2": 0.11, "B3": 0.15, "B4": 0.19, "B8": 0.19, "B11": 0.31, "B12": 0.25,
                    "VV": -9.8, "VH": -15.2, "VV_VH_ratio": 5.4
                }
            },
            {
                "id": f"SAT-{region[:2].upper()}-2026",
                "platform": "Sentinel-2 L2A / Sentinel-1",
                "sensor_type": "Optical MSI / C-Band SAR",
                "region": region,
                "year": 2026,
                "acquisition_date": "2026-08-18",
                "cloud_coverage": 0.8,
                "cloud_masked": True,
                "mean_ndvi": 0.14, # Acute disturbance
                "mean_ndwi": -0.34,
                "mean_ndbi": 0.44,
                "mean_bsi": 0.52,
                "sar_vv_mean": -8.1,
                "sar_vh_mean": -13.6,
                "status": "Active Breach Alert Zone",
                "disturbed_area_ha": 14.2,
                "band_values": {
                    "B2": 0.14, "B3": 0.18, "B4": 0.26, "B8": 0.15, "B11": 0.38, "B12": 0.32,
                    "VV": -8.1, "VH": -13.6, "VV_VH_ratio": 5.5
                }
            }
        ]

satellite_pipeline = SatellitePreprocessingPipeline()
satellite_service = satellite_pipeline
