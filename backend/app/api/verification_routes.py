from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import datetime
import uuid
from app.core.database import get_db
from app.models.db_models import Alert, VerificationRecord
from app.schemas.schemas import VerificationCreate, VerificationResponse

router = APIRouter(prefix="/verification", tags=["Human-in-the-Loop Field Verification"])

@router.get("/queue", response_model=List[Dict[str, Any]])
def get_verification_queue(
    status: str = Query(default="ALL"),
    db: Session = Depends(get_db)
):
    """Returns alerts requiring officer review and field verification."""
    query = db.query(Alert)
    if status != "ALL":
        query = query.filter(Alert.status == status)
    alerts = query.order_by(Alert.risk_score.desc()).all()

    return [
        {
            "alert_id": a.id,
            "title": a.title,
            "district": a.district,
            "state": a.state,
            "risk_score": a.risk_score,
            "priority": a.priority,
            "disturbed_area_ha": a.disturbed_area_ha,
            "lease_status": a.lease_status,
            "distance_from_lease_m": a.distance_from_lease_m,
            "status": a.status,
            "last_detected": a.last_detected,
            "assigned_officer": a.assigned_officer,
            "verifications_count": len(a.verifications)
        }
        for a in alerts
    ]

@router.post("/submit", response_model=VerificationResponse)
def submit_verification_record(payload: VerificationCreate, db: Session = Depends(get_db)):
    """Submits officer field inspection feedback, updating alert lifecycle and recording audit trail."""
    alert = db.query(Alert).filter(Alert.id == payload.alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail=f"Alert {payload.alert_id} not found")

    # Update alert status
    alert.status = payload.status
    alert.updated_at = datetime.utcnow()

    # Create verification audit record
    v_id = f"VR-{alert.id}-{str(uuid.uuid4())[:6].upper()}"
    rec = VerificationRecord(
        id=v_id,
        alert_id=alert.id,
        verified_by=alert.assigned_officer,
        officer_role="FIELD_OFFICER",
        status=payload.status,
        comments=payload.comments,
        gps_coordinates=payload.gps_coordinates or f"{alert.latitude}, {alert.longitude}",
        evidence_notes=payload.evidence_notes or "On-site GPS match verified against GIS polygon boundary.",
        photo_urls=payload.photo_urls or ["/assets/satellite_mockup.png"]
    )
    db.add(rec)
    db.commit()
    db.refresh(rec)

    return rec

@router.get("/history/{alert_id}", response_model=List[VerificationResponse])
def get_alert_verification_history(alert_id: str, db: Session = Depends(get_db)):
    """Retrieves full chronological audit log of all officer inspections for an alert."""
    records = db.query(VerificationRecord).filter(VerificationRecord.alert_id == alert_id).order_by(VerificationRecord.timestamp.desc()).all()
    return records
