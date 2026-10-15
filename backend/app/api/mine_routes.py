from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app.core.database import get_db
from app.models.db_models import MiningLease, Alert
from app.schemas.schemas import MiningLeaseSummary, MiningLeaseDetail, GlobalMiningSite
from app.gis.geojson_loader import get_demo_gis_layers
from app.gis.global_mines_data import get_all_global_mining_sites, get_mining_site_by_id

router = APIRouter(prefix="", tags=["Global Mining Sites & Cadastral Leases"])

@router.get("/mining-sites", response_model=List[GlobalMiningSite])
def get_global_mining_sites(
    country: Optional[str] = None,
    mineral: Optional[str] = None
):
    """
    Returns global reference mining inventory across India, Australia, Brazil,
    Chile, Canada, South Africa, Indonesia, and USA.
    """
    sites = get_all_global_mining_sites()
    if country and country != "ALL":
        sites = [s for s in sites if s["country"].lower() == country.lower() or s["country_code"].lower() == country.lower()]
    if mineral and mineral != "ALL":
        sites = [s for s in sites if mineral.lower() in s["mineral"].lower()]
    return sites

@router.get("/mining-sites/{site_id}", response_model=GlobalMiningSite)
def get_global_mining_site_details(site_id: str):
    """Returns detailed metadata for a global mining sector."""
    site = get_mining_site_by_id(site_id)
    if not site:
        raise HTTPException(status_code=404, detail=f"Mining site {site_id} not found")
    return site

@router.get("/mines/leases", response_model=List[MiningLeaseSummary])
def get_all_leases(
    state: Optional[str] = None,
    district: Optional[str] = None,
    mineral: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(MiningLease)
    if state and state != "ALL":
        query = query.filter(MiningLease.state.ilike(f"%{state}%"))
    if district and district != "ALL":
        query = query.filter(MiningLease.district.ilike(f"%{district}%"))
    if mineral and mineral != "ALL":
        query = query.filter(MiningLease.mineral.ilike(f"%{mineral}%"))
    if status and status != "ALL":
        query = query.filter(MiningLease.status == status)

    leases = query.all()
    results = []
    for l in leases:
        alerts_count = db.query(Alert).filter(Alert.lease_id == l.id).count()
        results.append(
            MiningLeaseSummary(
                id=l.id,
                name=l.name,
                state=l.state,
                district=l.district,
                mineral=l.mineral,
                area_hectares=l.area_hectares,
                status=l.status,
                lessee_name=l.lessee_name,
                grant_date=l.grant_date,
                expiry_date=l.expiry_date,
                center_lat=l.center_lat,
                center_lng=l.center_lng,
                active_alerts_count=alerts_count
            )
        )
    return results

@router.get("/mines/leases/{lease_id}", response_model=MiningLeaseDetail)
def get_lease_by_id(lease_id: str, db: Session = Depends(get_db)):
    lease = db.query(MiningLease).filter(MiningLease.id == lease_id).first()
    if not lease:
        raise HTTPException(status_code=404, detail=f"Lease {lease_id} not found")
    
    alerts_count = db.query(Alert).filter(Alert.lease_id == lease.id).count()
    return MiningLeaseDetail(
        id=lease.id,
        name=lease.name,
        state=lease.state,
        district=lease.district,
        mineral=lease.mineral,
        area_hectares=lease.area_hectares,
        status=lease.status,
        lessee_name=lease.lessee_name,
        grant_date=lease.grant_date,
        expiry_date=lease.expiry_date,
        center_lat=lease.center_lat,
        center_lng=lease.center_lng,
        active_alerts_count=alerts_count,
        geometry=lease.geometry,
        surveillance_buffer_geojson=lease.surveillance_buffer_geojson
    )

@router.get("/mines/gis/layers/{region_name}")
def get_region_gis_layers(region_name: str):
    """Returns complete 12 GIS layers in GeoJSON format for the map."""
    layers = get_demo_gis_layers(region_name)
    return layers
