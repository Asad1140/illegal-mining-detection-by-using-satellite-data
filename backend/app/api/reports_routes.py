from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.db_models import Alert, MiningLease
from app.services.report_service import report_service

router = APIRouter(prefix="/reports", tags=["Report Generation"])

@router.get("/alert/{alert_id}")
def get_alert_report_dossier(alert_id: str, db: Session = Depends(get_db)):
    """Generates official Potential Unauthorized Mining Activity Report dossier."""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail=f"Alert {alert_id} not found")

    lease = db.query(MiningLease).filter(MiningLease.id == alert.lease_id).first()
    report_data = report_service.generate_alert_report_data(alert, lease)
    return report_data
