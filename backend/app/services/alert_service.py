from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.db_models import Alert, MiningLease, VerificationRecord, DataSource
from app.gis.geojson_loader import get_demo_gis_layers, REGION_CENTERS
from app.ai.risk_engine import risk_engine

class AlertService:
    @staticmethod
    def seed_initial_data(db: Session):
        """Seeds initial mining leases, alerts, verification records, and data sources if database is empty."""
        if db.query(MiningLease).first() is not None:
            return

        # 1. Seed Leases across all 4 regions
        for region_name, center_info in REGION_CENTERS.items():
            layers = get_demo_gis_layers(region_name)
            for feat in layers["mining_leases"]["features"]:
                p = feat["properties"]
                buf_feat = next((b for b in layers["surveillance_buffers"]["features"] if b["properties"]["lease_id"] == p["lease_id"]), None)
                
                lease = MiningLease(
                    id=p["lease_id"],
                    name=p["name"],
                    state=center_info["state"],
                    district=region_name,
                    mineral=p["mineral"],
                    area_hectares=p["area_ha"],
                    status=p["status"],
                    lessee_name=p["lessee"],
                    grant_date=p["grant_date"],
                    expiry_date=p["expiry_date"],
                    center_lat=center_info["lat"],
                    center_lng=center_info["lng"],
                    geometry=feat["geometry"],
                    surveillance_buffer_geojson=buf_feat["geometry"] if buf_feat else None
                )
                db.add(lease)

        db.commit()

        # 2. Seed Alerts
        demo_alerts_data = [
            {
                "id": "MG-2026-00421",
                "title": "Potential Unauthorized Mining Excavation - Keonjhar East",
                "lease_id": "ML-KE-01",
                "state": "Odisha",
                "district": "Keonjhar",
                "location_name": "Joda-Barbil Iron Sector Block C",
                "latitude": 21.8523,
                "longitude": 85.5932,
                "disturbed_area_ha": 14.2,
                "lease_status": "Outside registered lease",
                "distance_from_lease_m": 180.0,
                "first_detected": "2023-03-15",
                "last_detected": "2026-08-18",
                "status": "PENDING",
                "assigned_officer": "Anil Kumar Patnaik (District Mining Officer)",
                "explanation_summary": "14.2 ha unapproved excavation detected 180m outside registered mining lease boundary ML-KE-01. Severe canopy loss (75%) and persistent SAR backscatter shift indicate active extraction.",
                "geometry": get_demo_gis_layers("Keonjhar")["disturbances"]["features"][0]["geometry"],
                "factors": {
                    "disturbed_area_ha": 14.2,
                    "is_persistent": True,
                    "lease_status": "Outside registered lease",
                    "distance_from_lease_m": 180.0,
                    "vegetation_loss_pct": 78.5,
                    "sar_anomaly_detected": True,
                    "growth_rate_pct": 18.3,
                    "near_vulnerable_ecosystem": True
                }
            },
            {
                "id": "MG-2026-00388",
                "title": "Perimeter Encroachment in 500m Buffer - Keonjhar North",
                "lease_id": "ML-KE-02",
                "state": "Odisha",
                "district": "Keonjhar",
                "location_name": "Bamebari North Ridge",
                "latitude": 21.8641,
                "longitude": 85.5958,
                "disturbed_area_ha": 6.8,
                "lease_status": "Within 500m Buffer Zone",
                "distance_from_lease_m": 45.0,
                "first_detected": "2024-04-10",
                "last_detected": "2026-08-12",
                "status": "FIELD_VERIFICATION",
                "assigned_officer": "Anil Kumar Patnaik (District Mining Officer)",
                "explanation_summary": "6.8 ha waste spoil encroaching into the statutory 500m surveillance buffer of lease ML-KE-02. Potential risk to tributary runoff.",
                "geometry": get_demo_gis_layers("Keonjhar")["disturbances"]["features"][1]["geometry"],
                "factors": {
                    "disturbed_area_ha": 6.8,
                    "is_persistent": True,
                    "lease_status": "Within 500m Buffer Zone",
                    "distance_from_lease_m": 45.0,
                    "vegetation_loss_pct": 62.0,
                    "sar_anomaly_detected": True,
                    "growth_rate_pct": 14.0,
                    "near_vulnerable_ecosystem": True
                }
            },
            {
                "id": "MG-2026-00214",
                "title": "Unauthorized Ridge Extraction - Sandur Schist Belt",
                "lease_id": "ML-BE-01",
                "state": "Karnataka",
                "district": "Bellary",
                "location_name": "Sandur Hills Range #4",
                "latitude": 15.0941,
                "longitude": 76.5538,
                "disturbed_area_ha": 11.5,
                "lease_status": "Outside registered lease",
                "distance_from_lease_m": 120.0,
                "first_detected": "2023-08-01",
                "last_detected": "2026-08-14",
                "status": "UNDER_REVIEW",
                "assigned_officer": "K. Venkatesh (Bellary Enforcement Wing)",
                "explanation_summary": "11.5 ha opencast disturbance outside lease ML-BE-01 along sensitive ridge. Optical BSI elevated by 42% over baseline.",
                "geometry": get_demo_gis_layers("Bellary")["disturbances"]["features"][0]["geometry"],
                "factors": {
                    "disturbed_area_ha": 11.5,
                    "is_persistent": True,
                    "lease_status": "Outside registered lease",
                    "distance_from_lease_m": 120.0,
                    "vegetation_loss_pct": 71.0,
                    "sar_anomaly_detected": True,
                    "growth_rate_pct": 16.5,
                    "near_vulnerable_ecosystem": True
                }
            },
            {
                "id": "MG-2026-00192",
                "title": "Chromite Valley Spoil Expansion - Sukinda West",
                "lease_id": "ML-SU-01",
                "state": "Odisha",
                "district": "Sukinda",
                "location_name": "Damsall Nallah Watershed",
                "latitude": 21.0389,
                "longitude": 85.8365,
                "disturbed_area_ha": 9.4,
                "lease_status": "Within 500m Buffer Zone",
                "distance_from_lease_m": 75.0,
                "first_detected": "2024-01-20",
                "last_detected": "2026-08-10",
                "status": "UNDER_REVIEW",
                "assigned_officer": "Ramesh Chandra Mohanty",
                "explanation_summary": "9.4 ha overburden dump within 500m buffer zone bordering Damsall Nallah. Elevated sedimentation risk detected by NDWI anomaly.",
                "geometry": get_demo_gis_layers("Sukinda")["disturbances"]["features"][0]["geometry"],
                "factors": {
                    "disturbed_area_ha": 9.4,
                    "is_persistent": True,
                    "lease_status": "Within 500m Buffer Zone",
                    "distance_from_lease_m": 75.0,
                    "vegetation_loss_pct": 68.0,
                    "sar_anomaly_detected": True,
                    "growth_rate_pct": 15.2,
                    "near_vulnerable_ecosystem": True
                }
            },
            {
                "id": "MG-2026-00105",
                "title": "Internal Pit Deepening - Approved Mine Block A",
                "lease_id": "ML-KE-01",
                "state": "Odisha",
                "district": "Keonjhar",
                "location_name": "Joda Central Pit Floor",
                "latitude": 21.8373,
                "longitude": 85.5752,
                "disturbed_area_ha": 22.4,
                "lease_status": "Inside Authorized Lease",
                "distance_from_lease_m": 0.0,
                "first_detected": "2022-05-10",
                "last_detected": "2026-07-28",
                "status": "VERIFIED",
                "assigned_officer": "Anil Kumar Patnaik (District Mining Officer)",
                "explanation_summary": "22.4 ha extraction activity entirely inside authorized lease ML-KE-01. Validated as compliant with approved Mining Plan (IBM).",
                "geometry": get_demo_gis_layers("Keonjhar")["disturbances"]["features"][2]["geometry"],
                "factors": {
                    "disturbed_area_ha": 22.4,
                    "is_persistent": True,
                    "lease_status": "Inside Authorized Lease",
                    "distance_from_lease_m": 0.0,
                    "vegetation_loss_pct": 45.0,
                    "sar_anomaly_detected": False,
                    "growth_rate_pct": 8.0,
                    "near_vulnerable_ecosystem": False
                }
            },
            {
                "id": "MG-2026-00054",
                "title": "Overburden Dump Extension - Singrauli Coalfield",
                "lease_id": "ML-SI-01",
                "state": "Madhya Pradesh",
                "district": "Singrauli",
                "location_name": "Jayant-Nigahi Peripheral Corridor",
                "latitude": 24.2052,
                "longitude": 82.6741,
                "disturbed_area_ha": 18.1,
                "lease_status": "Outside registered lease",
                "distance_from_lease_m": 210.0,
                "first_detected": "2023-11-12",
                "last_detected": "2026-08-05",
                "status": "PENDING",
                "assigned_officer": "Sanjay Tiwari (Singrauli Surveillance Unit)",
                "explanation_summary": "18.1 ha coal spoil dump outside lease boundary. High thermal and reflectance changes detected on Landsat/Sentinel-2.",
                "geometry": get_demo_gis_layers("Singrauli")["disturbances"]["features"][0]["geometry"],
                "factors": {
                    "disturbed_area_ha": 18.1,
                    "is_persistent": True,
                    "lease_status": "Outside registered lease",
                    "distance_from_lease_m": 210.0,
                    "vegetation_loss_pct": 82.0,
                    "sar_anomaly_detected": True,
                    "growth_rate_pct": 19.5,
                    "near_vulnerable_ecosystem": False
                }
            }
        ]

        for a in demo_alerts_data:
            risk_calc = risk_engine.calculate_risk(a["factors"])
            alert = Alert(
                id=a["id"],
                title=a["title"],
                lease_id=a["lease_id"],
                state=a["state"],
                district=a["district"],
                location_name=a["location_name"],
                latitude=a["latitude"],
                longitude=a["longitude"],
                risk_score=risk_calc["total_score"],
                priority=risk_calc["risk_category"],
                disturbed_area_ha=a["disturbed_area_ha"],
                lease_status=a["lease_status"],
                distance_from_lease_m=a["distance_from_lease_m"],
                first_detected=a["first_detected"],
                last_detected=a["last_detected"],
                status=a["status"],
                confidence=0.92,
                explanation_summary=a["explanation_summary"],
                risk_factors_json=risk_calc["factor_scores"],
                geometry=a["geometry"],
                assigned_officer=a["assigned_officer"]
            )
            db.add(alert)

            # Add initial verification records for verified or under review cases
            if a["status"] in ["VERIFIED", "FIELD_VERIFICATION"]:
                rec = VerificationRecord(
                    id=f"VR-{a['id']}-01",
                    alert_id=a["id"],
                    verified_by=a["assigned_officer"],
                    officer_role="FIELD_OFFICER",
                    status=a["status"],
                    comments=f"Ground patrol inspected site coordinates ({a['latitude']}, {a['longitude']}). Boundary stakes inspected against cadastral map.",
                    gps_coordinates=f"{a['latitude']}, {a['longitude']}",
                    evidence_notes="Handheld DGPS verification confirmed footprint coordinates matching satellite polygon.",
                    photo_urls=["/assets/satellite_mockup.png"]
                )
                db.add(rec)

        # 3. Seed Data Sources Catalog
        data_sources_list = [
            DataSource(
                id="DS-S2",
                name="Sentinel-2 MSI (Multispectral)",
                source_type="Optical Satellite",
                provider="European Space Agency (ESA) Copernicus",
                purpose="10m/20m multispectral vegetation, bare soil (BSI), and land-use disturbance monitoring",
                resolution="10m (B2, B3, B4, B8) / 20m (SWIR)",
                update_frequency="Every 5 days",
                status="DEMO / INTEGRATION READY",
                is_live=False,
                last_sync="2026-08-18"
            ),
            DataSource(
                id="DS-S1",
                name="Sentinel-1 SAR (C-Band Radar)",
                source_type="Radar Satellite",
                provider="ESA Copernicus",
                purpose="All-weather surface roughness and pit topography change detection under cloudy monsoon conditions",
                resolution="10m (GRD)",
                update_frequency="Every 6-12 days",
                status="DEMO / INTEGRATION READY",
                is_live=False,
                last_sync="2026-08-18"
            ),
            DataSource(
                id="DS-L89",
                name="Landsat 8 & 9 OLI/TIRS",
                source_type="Optical & Thermal Satellite",
                provider="USGS / NASA",
                purpose="Historical baseline analysis (2022-2026) and thermal pit footprint comparison",
                resolution="30m Multispectral / 15m Panchromatic",
                update_frequency="Every 8 days (constellation)",
                status="DEMO / INTEGRATION READY",
                is_live=False,
                last_sync="2026-08-15"
            ),
            DataSource(
                id="DS-CAD",
                name="Official State Mining Cadastre & Leases",
                source_type="GIS Cadastre Database",
                provider="State Directorate of Mines & Geology / Indian Bureau of Mines (IBM)",
                purpose="Authoritative mining lease boundary polygons and statutory 500m surveillance buffer perimeters",
                resolution="Sub-meter Cadastral Vector",
                update_frequency="Monthly / Real-time sync",
                status="ACTIVE / INTEGRATED",
                is_live=True,
                last_sync="2026-08-20"
            ),
            DataSource(
                id="DS-DEM",
                name="SRTM & CartoDEM Elevation",
                source_type="Digital Elevation Model",
                provider="ISRO / USGS",
                purpose="Topographic slope and watershed vulnerability analysis for risk scoring",
                resolution="30m Elevation Grid",
                update_frequency="Static Baseline",
                status="ACTIVE / INTEGRATED",
                is_live=True,
                last_sync="2026-08-01"
            )
        ]

        for ds in data_sources_list:
            db.add(ds)

        db.commit()

alert_service = AlertService()
