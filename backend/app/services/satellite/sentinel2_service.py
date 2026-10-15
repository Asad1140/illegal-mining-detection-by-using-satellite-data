import numpy as np
from typing import Dict, Any, List, Optional, Tuple
import logging

logger = logging.getLogger("illegal-mining-detection.satellite.sentinel2")

class Sentinel2Processor:
    """
    Sentinel-2 Level-2A multispectral processing engine:
    - Band extraction (B02-B12, SCL)
    - Safe spectral index calculations (NDVI, NDWI, NDBI, BSI)
    - SCL cloud, cloud-shadow, and cirrus masking
    - Usable pixel percentage estimation
    """
    
    # SCL Classes definition according to ESA S2 L2A Product Specification
    SCL_CLASSES = {
        0: "NO_DATA",
        1: "SATURATED_OR_DEFECTIVE",
        2: "DARK_AREA_PIXELS",
        3: "CLOUD_SHADOWS",
        4: "VEGETATION",
        5: "NOT_VEGETATED_BARE_SOIL",
        6: "WATER",
        7: "UNCLASSIFIED",
        8: "CLOUD_MEDIUM_PROBABILITY",
        9: "CLOUD_HIGH_PROBABILITY",
        10: "THIN_CIRRUS",
        11: "SNOW_OR_ICE"
    }

    # Classes considered cloud or shadow contamination
    CONTAMINATED_SCL_CLASSES = {2, 3, 8, 9, 10}

    @staticmethod
    def calculate_spectral_indices(
        b02: np.ndarray,
        b03: np.ndarray,
        b04: np.ndarray,
        b08: np.ndarray,
        b11: np.ndarray,
        eps: float = 1e-6
    ) -> Dict[str, np.ndarray]:
        """
        Calculates mathematical physical indices with safe division handling.
        """
        # Ensure floating point arrays
        b2 = np.asarray(b02, dtype=np.float32)
        b3 = np.asarray(b03, dtype=np.float32)
        b4 = np.asarray(b04, dtype=np.float32)
        b8 = np.asarray(b08, dtype=np.float32)
        b11 = np.asarray(b11, dtype=np.float32)

        # 1. NDVI = (NIR - Red) / (NIR + Red)
        ndvi_denom = b8 + b4
        ndvi = np.where(np.abs(ndvi_denom) > eps, (b8 - b4) / (ndvi_denom + eps), 0.0)
        ndvi = np.clip(ndvi, -1.0, 1.0)

        # 2. NDWI = (Green - NIR) / (Green + NIR)
        ndwi_denom = b3 + b8
        ndwi = np.where(np.abs(ndwi_denom) > eps, (b3 - b8) / (ndwi_denom + eps), 0.0)
        ndwi = np.clip(ndwi, -1.0, 1.0)

        # 3. NDBI = (SWIR1 - NIR) / (SWIR1 + NIR)
        ndbi_denom = b11 + b8
        ndbi = np.where(np.abs(ndbi_denom) > eps, (b11 - b8) / (ndbi_denom + eps), 0.0)
        ndbi = np.clip(ndbi, -1.0, 1.0)

        # 4. BSI = ((SWIR1 + Red) - (NIR + Blue)) / ((SWIR1 + Red) + (NIR + Blue))
        bsi_num = (b11 + b4) - (b8 + b2)
        bsi_denom = (b11 + b4) + (b8 + b2)
        bsi = np.where(np.abs(bsi_denom) > eps, bsi_num / (bsi_denom + eps), 0.0)
        bsi = np.clip(bsi, -1.0, 1.0)

        return {
            "NDVI": ndvi,
            "NDWI": ndwi,
            "NDBI": ndbi,
            "BSI": bsi
        }

    @classmethod
    def apply_scl_cloud_mask(
        cls,
        scl_array: np.ndarray,
        data_arrays: Dict[str, np.ndarray]
    ) -> Tuple[Dict[str, np.ndarray], float]:
        """
        Applies Scene Classification Layer (SCL) mask.
        Returns masked arrays with invalid cloud/shadow pixels set to NaN and the usable pixel percentage.
        """
        scl = np.asarray(scl_array, dtype=np.int32)
        total_pixels = scl.size
        if total_pixels == 0:
            return data_arrays, 0.0

        # Mask is True for clear pixels (not in contaminated classes)
        clear_mask = ~np.isin(scl, list(cls.CONTAMINATED_SCL_CLASSES)) & (scl != 0)
        clear_pixels = np.count_nonzero(clear_mask)
        usable_pixel_pct = round((clear_pixels / total_pixels) * 100.0, 2)

        masked_arrays = {}
        for key, arr in data_arrays.items():
            arr_float = np.asarray(arr, dtype=np.float32).copy()
            arr_float[~clear_mask] = np.nan
            masked_arrays[key] = arr_float

        return masked_arrays, usable_pixel_pct

    @classmethod
    def process_observation_features(
        cls,
        band_values: Dict[str, float],
        cloud_cover_meta: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Computes summary spectral statistics and quality indicators for an observation.
        """
        b2 = band_values.get("B02", band_values.get("B2", 0.08))
        b3 = band_values.get("B03", band_values.get("B3", 0.12))
        b4 = band_values.get("B04", band_values.get("B4", 0.14))
        b8 = band_values.get("B08", band_values.get("B8", 0.32))
        b11 = band_values.get("B11", 0.24)
        b12 = band_values.get("B12", 0.18)

        # Spectral Indices scalar computation
        eps = 1e-6
        ndvi = round(float((b8 - b4) / (b8 + b4 + eps)), 3)
        ndwi = round(float((b3 - b8) / (b3 + b8 + eps)), 3)
        ndbi = round(float((b11 - b8) / (b11 + b8 + eps)), 3)
        bsi = round(float(((b11 + b4) - (b8 + b2)) / ((b11 + b4) + (b8 + b2) + eps)), 3)

        cloud_pct = cloud_cover_meta if cloud_cover_meta is not None else 5.0
        usable_pct = round(max(0.0, min(100.0, 100.0 - cloud_pct)), 1)

        return {
            "mean_ndvi": ndvi,
            "mean_ndwi": ndwi,
            "mean_ndbi": ndbi,
            "mean_bsi": bsi,
            "usable_pixel_percent": usable_pct,
            "cloud_cover_percent": cloud_pct,
            "is_usable": usable_pct >= 70.0,
            "bands": {
                "B02_blue": b2,
                "B03_green": b3,
                "B04_red": b4,
                "B08_nir": b8,
                "B11_swir1": b11,
                "B12_swir2": b12
            }
        }

sentinel2_processor = Sentinel2Processor()
