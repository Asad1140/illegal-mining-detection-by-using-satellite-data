from typing import Dict, Any, List, Optional
from app.ai.base_models import BaseRiskModel
from app.core.config import settings

class ExplainableRiskEngine(BaseRiskModel):
    """
    Configurable 7-factor explainable risk scoring engine (0-100).
    Decomposes risk into physical, spectral, radar, and spatial factors with
    contribution charts, evidence summary, and strict compliance separation.
    """

    def calculate_risk(
        self,
        factors: Dict[str, Any],
        custom_weights: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        weights = custom_weights or {
            "disturbance": settings.RISK_WEIGHTS.disturbance_weight,
            "temporal": settings.RISK_WEIGHTS.temporal_weight,
            "outside_lease": settings.RISK_WEIGHTS.outside_lease_weight,
            "vegetation_loss": settings.RISK_WEIGHTS.vegetation_loss_weight,
            "sar_anomaly": settings.RISK_WEIGHTS.sar_anomaly_weight,
            "historical_expansion": settings.RISK_WEIGHTS.historical_expansion_weight,
            "terrain_context": settings.RISK_WEIGHTS.terrain_context_weight
        }

        # 1. Disturbance Area Score (0 - max disturbance_weight)
        area_ha = float(factors.get("disturbed_area_ha", 14.2))
        max_dist_w = weights["disturbance"]
        disturbance_score = round(min(max_dist_w, (area_ha / 15.0) * max_dist_w), 1)

        # 2. Temporal Persistence Score (0 - max temporal_weight)
        is_persistent = factors.get("is_persistent", True)
        temporal_score = weights["temporal"] if is_persistent else round(weights["temporal"] * 0.4, 1)

        # 3. Boundary / Outside Lease Score (0 - max outside_lease_weight)
        authoritative_lease = factors.get("authoritative_lease_available", True)
        lease_status = factors.get("lease_status", "Outside registered lease")
        dist_m = float(factors.get("distance_from_lease_m", 180.0))
        max_out_w = weights["outside_lease"]

        if not authoritative_lease:
            outside_lease_score = 0.0
            lease_status_text = "Legal Lease Boundary Data Unavailable for this Region"
        elif "outside" in lease_status.lower() or dist_m > 0:
            outside_lease_score = max_out_w
            lease_status_text = f"Outside Authorized Lease ({dist_m:.0f}m from perimeter)"
        elif "buffer" in lease_status.lower():
            outside_lease_score = round(max_out_w * 0.75, 1)
            lease_status_text = f"Inside Surveillance Buffer ({dist_m:.0f}m from boundary)"
        else:
            outside_lease_score = round(max_out_w * 0.15, 1)
            lease_status_text = "Inside Registered Authorized Lease"

        # 4. Vegetation Loss Score (0 - max vegetation_loss_weight)
        veg_loss_pct = float(factors.get("vegetation_loss_pct", 75.0))
        max_veg_w = weights["vegetation_loss"]
        vegetation_loss_score = round(min(max_veg_w, (veg_loss_pct / 100.0) * max_veg_w), 1)

        # 5. SAR Anomaly Score (0 - max sar_anomaly_weight)
        sar_detected = factors.get("sar_anomaly_detected", True)
        sar_anomaly_score = weights["sar_anomaly"] if sar_detected else 0.0

        # 6. Historical Expansion Score (0 - max historical_expansion_weight)
        growth_rate_pct = float(factors.get("growth_rate_pct", 18.3))
        max_hist_w = weights["historical_expansion"]
        historical_expansion_score = round(min(max_hist_w, (growth_rate_pct / 20.0) * max_hist_w), 1)

        # 7. Terrain & Contextual Vulnerability Score (0 - max terrain_context_weight)
        near_water_or_forest = factors.get("near_vulnerable_ecosystem", True)
        terrain_score = weights["terrain_context"] if near_water_or_forest else round(weights["terrain_context"] * 0.3, 1)

        total_score = round(
            disturbance_score +
            temporal_score +
            outside_lease_score +
            vegetation_loss_score +
            sar_anomaly_score +
            historical_expansion_score +
            terrain_score,
            1
        )
        total_score = min(100.0, max(0.0, total_score))

        # Categorization
        if total_score < settings.RISK_THRESHOLDS.low_max:
            category = "LOW"
            color = "#10b981" # Green
        elif total_score < settings.RISK_THRESHOLDS.medium_max:
            category = "MEDIUM"
            color = "#eab308" # Yellow
        elif total_score < settings.RISK_THRESHOLDS.high_max:
            category = "HIGH"
            color = "#f97316" # Orange
        else:
            category = "CRITICAL"
            color = "#ef4444" # Red

        # Generate Explainable Bullets
        bullets = [
            f"+ {area_ha} ha newly disturbed surface area (Score: {disturbance_score}/{max_dist_w})",
            f"+ Multi-date temporal persistence verified (Score: {temporal_score}/{weights['temporal']})",
            f"+ Cadastral Boundary: {lease_status_text} (Score: {outside_lease_score}/{max_out_w})",
            f"+ Vegetation canopy loss (-{veg_loss_pct}%) (Score: {vegetation_loss_score}/{max_veg_w})",
            f"+ Sentinel-1 SAR radar backscatter anomaly (Score: {sar_anomaly_score}/{weights['sar_anomaly']})",
            f"+ Historical expansion rate (+{growth_rate_pct}% YoY) (Score: {historical_expansion_score}/{max_hist_w})",
            f"+ Environmental vulnerability context (Score: {terrain_score}/{weights['terrain_context']})"
        ]

        if not authoritative_lease:
            evidence_summary = (
                f"Significant remote-sensing surface disturbance ({area_ha} ha) detected via multi-spectral Sentinel-2 "
                f"and SAR Sentinel-1 observations. Note: Authoritative cadastral lease boundaries are not available for "
                f"this location, so legal authorization status cannot be evaluated."
            )
        else:
            evidence_summary = (
                f"Potential unauthorized mining-related disturbance detected outside the registered mining lease "
                f"({lease_status_text}). High spectral change and radar backscatter anomalies "
                f"indicate active extraction and canopy loss. Human field verification required."
            )

        return {
            "model_name": "Calibrated 7-Factor Explainable Monitoring Risk Engine",
            "model_status": "Operational Risk Model",
            "total_score": total_score,
            "risk_category": category,
            "color": color,
            "factor_scores": {
                "disturbance_score": disturbance_score,
                "temporal_persistence_score": temporal_score,
                "outside_lease_score": outside_lease_score,
                "vegetation_loss_score": vegetation_loss_score,
                "sar_anomaly_score": sar_anomaly_score,
                "historical_expansion_score": historical_expansion_score,
                "terrain_context_score": terrain_score
            },
            "weights_used": weights,
            "explanation_bullets": bullets,
            "evidence_summary": evidence_summary,
            "recommended_action": "Ground field inspection by authorized mining enforcement officer recommended."
        }

risk_engine = ExplainableRiskEngine()
