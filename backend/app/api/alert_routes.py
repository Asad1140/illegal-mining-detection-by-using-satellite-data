from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.db_models import Alert, MiningLease, VerificationRecord
from app.schemas.schemas import AlertSummary, AlertDetail, RiskFactorBreakdown
from app.ai.risk_engine import risk_engine

router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.get("", response_model=List[AlertSummary])
def get_alerts(
    district: Optional[str] = None,
    priority: Optional[str] = None,
    status: Optional[str] = None,
    min_risk: Optional[float] = None,
    sort_by: str = Query(default="risk_score", enum=["risk_score", "disturbed_area_ha", "last_detected"]),
    db: Session = Depends(get_db)
):
    query = db.query(Alert)
    if district and district != "ALL":
        query = query.filter(Alert.district.ilike(f"%{district}%"))
    if priority and priority != "ALL":
        query = query.filter(Alert.priority == priority)
    if status and status != "ALL":
        query = query.filter(Alert.status == status)
    if min_risk is not None:
        query = query.filter(Alert.risk_score >= min_risk)

    if sort_by == "disturbed_area_ha":
        query = query.order_by(Alert.disturbed_area_ha.desc())
    elif sort_by == "last_detected":
        query = query.order_by(Alert.last_detected.desc())
    else:
        query = query.order_by(Alert.risk_score.desc())

    return query.all()

@router.get("/{alert_id}", response_model=AlertDetail)
def get_alert_by_id(alert_id: str, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail=f"Alert {alert_id} not found")

    factors = alert.risk_factors_json or {}
    bullets = [
        f"+ {alert.disturbed_area_ha} ha newly disturbed surface area (Score: {factors.get('disturbance_score', 22.0)}/25)",
        f"+ Persistent multi-temporal change detected (Score: {factors.get('temporal_persistence_score', 18.0)}/20)",
        f"+ Spatial status: {alert.lease_status} (Distance: {alert.distance_from_lease_m}m) (Score: {factors.get('outside_lease_score', 20.0)}/20)",
        f"+ Significant vegetation canopy decline (Score: {factors.get('vegetation_loss_score', 8.5)}/10)",
        f"+ SAR backscatter radar anomaly confirmed (Score: {factors.get('sar_anomaly_score', 10.0)}/10)",
        f"+ Historical expansion trend observed (Score: {factors.get('historical_expansion_score', 8.5)}/10)",
        f"+ Proximity to watershed/vulnerable terrain (Score: {factors.get('terrain_context_score', 4.0)}/5)"
    ]

    breakdown = RiskFactorBreakdown(
        disturbance_score=factors.get("disturbance_score", 22.0),
        temporal_persistence_score=factors.get("temporal_persistence_score", 18.0),
        outside_lease_score=factors.get("outside_lease_score", 20.0),
        vegetation_loss_score=factors.get("vegetation_loss_score", 8.5),
        sar_anomaly_score=factors.get("sar_anomaly_score", 10.0),
        historical_expansion_score=factors.get("historical_expansion_score", 8.5),
        terrain_context_score=factors.get("terrain_context_score", 4.0),
        total_score=alert.risk_score,
        risk_category=alert.priority,
        explanation_bullets=bullets
    )

    return AlertDetail(
        id=alert.id,
        title=alert.title,
        lease_id=alert.lease_id,
        state=alert.state,
        district=alert.district,
        location_name=alert.location_name,
        latitude=alert.latitude,
        longitude=alert.longitude,
        risk_score=alert.risk_score,
        priority=alert.priority,
        disturbed_area_ha=alert.disturbed_area_ha,
        lease_status=alert.lease_status,
        distance_from_lease_m=alert.distance_from_lease_m,
        first_detected=alert.first_detected,
        last_detected=alert.last_detected,
        status=alert.status,
        confidence=alert.confidence,
        explanation_summary=alert.explanation_summary,
        assigned_officer=alert.assigned_officer,
        geometry=alert.geometry,
        risk_factors=breakdown,
        verifications=alert.verifications,
        created_at=alert.created_at,
        updated_at=alert.updated_at
    )
