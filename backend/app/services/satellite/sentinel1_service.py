import numpy as np
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger("illegal-mining-detection.satellite.sentinel1")

class Sentinel1Processor:
    """
    Sentinel-1 Ground Range Detected (GRD) C-Band SAR processing engine:
    - Radiometric calibration to sigma0 (dB)
    - Co-polarization (VV) and Cross-polarization (VH) analysis
    - Radar backscatter ratio (VV/VH)
    - Multi-temporal backscatter delta detection for cloud-resilient surveillance
    """

    @staticmethod
    def linear_to_db(intensity: np.ndarray, eps: float = 1e-7) -> np.ndarray:
        """Converts linear SAR amplitude/intensity to logarithmic decibels (dB)."""
        arr = np.asarray(intensity, dtype=np.float32)
        arr_clean = np.where(arr > 0, arr, eps)
        return 10.0 * np.log10(arr_clean)

    @staticmethod
    def calculate_sar_features(
        vv_db: float,
        vh_db: float,
        baseline_vv_db: Optional[float] = None,
        baseline_vh_db: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Calculates SAR polarization features and temporal backscatter shift.
        """
        # Radar roughness ratio: VV_dB - VH_dB (equivalent to 10 * log10(VV / VH))
        vv_vh_ratio_db = round(vv_db - vh_db, 2)
        
        # Temporal backscatter delta if baseline is provided
        delta_vv_db = round(vv_db - baseline_vv_db, 2) if baseline_vv_db is not None else 0.0
        delta_vh_db = round(vh_db - baseline_vh_db, 2) if baseline_vh_db is not None else 0.0

        # High positive shift in VV backscatter (> +4 dB) typically indicates surface excavation,
        # steep slope cleavage, or metal equipment.
        roughness_anomaly = abs(delta_vv_db) >= 4.0

        return {
            "sar_vv_mean_db": round(vv_db, 2),
            "sar_vh_mean_db": round(vh_db, 2),
            "sar_ratio_vv_vh_db": vv_vh_ratio_db,
            "temporal_delta_vv_db": delta_vv_db,
            "temporal_delta_vh_db": delta_vh_db,
            "sar_anomaly_detected": roughness_anomaly,
            "radar_penetration_status": "All-Weather Cloud-Penetrating Active Radar Acquisition",
            "interpretation": (
                f"SAR C-Band radar backscatter shift of {delta_vv_db:+.1f} dB (VV) and {delta_vh_db:+.1f} dB (VH). "
                + ("Significant surface roughness and slope cleavage detected." if roughness_anomaly else "Normal surface backscatter stability.")
            )
        }

sentinel1_processor = Sentinel1Processor()
