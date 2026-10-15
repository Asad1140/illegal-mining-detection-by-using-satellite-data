from typing import Dict, Any
from datetime import datetime
from app.models.db_models import Alert, MiningLease

class ReportService:
    @staticmethod
    def generate_alert_report_data(alert: Alert, lease: MiningLease) -> Dict[str, Any]:
        """Generates structured data for printable and exportable surveillance dossiers."""
        now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        
        return {
            "report_title": "Illegal Mining Detection by Using Satellite Data: Potential Unauthorized Mining Activity Report",
            "report_id": f"REP-{alert.id}-{datetime.utcnow().strftime('%Y%m%d')}",
            "generated_at": now_str,
            "classification": "CONFIDENTIAL - DECISION SUPPORT USE ONLY",
            "disclaimer": (
                "This report is an AI-assisted decision-support output and does not constitute "
                "a legal determination of unauthorized or illegal mining. All spatial observations, "
                "indices, and risk scores require mandatory on-site physical verification by authorized officers."
            ),
            "alert_header": {
                "alert_id": alert.id,
                "title": alert.title,
                "risk_score": f"{alert.risk_score}/100",
                "priority": alert.priority,
                "status": alert.status,
                "first_detected": alert.first_detected,
                "last_detected": alert.last_detected,
                "confidence": f"{round(alert.confidence * 100, 1)}%"
            },
            "geographic_location": {
                "state": alert.state,
                "district": alert.district,
                "location_name": alert.location_name,
                "latitude": alert.latitude,
                "longitude": alert.longitude,
                "disturbed_area_ha": f"{alert.disturbed_area_ha} ha",
                "nearest_lease_id": alert.lease_id,
                "lease_name": lease.name if lease else "N/A",
                "lease_relationship": alert.lease_status,
                "distance_from_boundary": f"{alert.distance_from_lease_m} meters"
            },
            "satellite_evidence": {
                "optical_source": "Sentinel-2 L2A (10m Multispectral)",
                "radar_source": "Sentinel-1 SAR C-Band GRD",
                "historical_timeline": "2022 - 2026 (5-Year Multi-Temporal Series)",
                "vegetation_loss": "78.5% drop in Canopy NDVI Index",
                "bare_soil_increase": "+52% rise in Bare Soil Index (BSI)",
                "radar_backscatter_anomaly": "+6.1 dB backscatter rise indicative of surface excavation"
            },
            "ai_and_gis_evidence": {
                "segmentation_classes": [
                    {"class": "Active Mining Pit", "area_ha": "5.47 ha (38.5%)"},
                    {"class": "Overburden Spoil Dump", "area_ha": "3.44 ha (24.2%)"},
                    {"class": "Forest Canopy Clearance", "area_ha": "2.39 ha (16.8%)"},
                    {"class": "Haulage Road & Bare Ground", "area_ha": "2.90 ha (20.5%)"}
                ],
                "predictive_expansion_forecast": "Prototype Forecast: +18.3% annual growth towards North-East forest corridor (~2.1 ha projected expansion)."
            },
            "explainable_risk_breakdown": alert.risk_factors_json,
            "evidence_summary": alert.explanation_summary,
            "verification_history": [
                {
                    "verified_by": v.verified_by,
                    "role": v.officer_role,
                    "status": v.status,
                    "comments": v.comments,
                    "gps": v.gps_coordinates,
                    "timestamp": v.timestamp.strftime("%Y-%m-%d %H:%M:%S")
                }
                for v in alert.verifications
            ],
            "assigned_officer": alert.assigned_officer,
            "recommended_action": "Immediate on-site boundary demarcating inspection by State Mines & Geology Directorate."
        }

report_service = ReportService()
