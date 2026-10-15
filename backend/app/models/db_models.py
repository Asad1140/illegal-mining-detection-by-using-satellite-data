from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class MiningLease(Base):
    __tablename__ = "mining_leases"

    id = Column(String(50), primary_key=True, index=True) # e.g. ML-OR-KJ-01
    name = Column(String(150), nullable=False)
    state = Column(String(100), nullable=False, index=True)
    district = Column(String(100), nullable=False, index=True)
    mineral = Column(String(100), nullable=False)
    area_hectares = Column(Float, nullable=False)
    status = Column(String(50), default="ACTIVE") # ACTIVE, EXPIRED, SUSPENDED, UNDER_RENEWAL
    lessee_name = Column(String(200), nullable=False)
    grant_date = Column(String(20), nullable=True)
    expiry_date = Column(String(20), nullable=True)
    center_lat = Column(Float, nullable=False)
    center_lng = Column(Float, nullable=False)
    geometry = Column(JSON, nullable=False) # GeoJSON polygon
    surveillance_buffer_geojson = Column(JSON, nullable=True) # GeoJSON 500m buffer

    alerts = relationship("Alert", back_populates="lease")

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(String(50), primary_key=True, index=True) # e.g. MG-2026-00421
    title = Column(String(200), nullable=False)
    lease_id = Column(String(50), ForeignKey("mining_leases.id"), nullable=True)
    state = Column(String(100), nullable=False, index=True)
    district = Column(String(100), nullable=False, index=True)
    location_name = Column(String(150), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    risk_score = Column(Float, nullable=False, index=True) # 0-100
    priority = Column(String(20), nullable=False, default="HIGH") # LOW, MEDIUM, HIGH, CRITICAL
    disturbed_area_ha = Column(Float, nullable=False)
    
    lease_status = Column(String(100), nullable=False) # "Outside registered lease", "Inside lease", "500m Buffer Zone"
    distance_from_lease_m = Column(Float, default=0.0)
    
    first_detected = Column(String(30), nullable=False)
    last_detected = Column(String(30), nullable=False)
    status = Column(String(50), default="PENDING") # PENDING, UNDER_REVIEW, FIELD_VERIFICATION, VERIFIED, FALSE_POSITIVE, REJECTED, CLOSED
    confidence = Column(Float, default=0.88)
    
    # Explainable AI factors
    explanation_summary = Column(Text, nullable=False)
    risk_factors_json = Column(JSON, nullable=False) # { disturbance: 22, temporal: 18, outside_lease: 20, ... }
    
    # Disturbance geometry
    geometry = Column(JSON, nullable=False) # GeoJSON polygon of disturbance
    
    assigned_officer = Column(String(100), default="Anil Kumar Patnaik")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    lease = relationship("MiningLease", back_populates="alerts")
    verifications = relationship("VerificationRecord", back_populates="alert", cascade="all, delete-orphan")

class VerificationRecord(Base):
    __tablename__ = "verification_records"

    id = Column(String(50), primary_key=True, index=True)
    alert_id = Column(String(50), ForeignKey("alerts.id"), nullable=False)
    verified_by = Column(String(150), nullable=False)
    officer_role = Column(String(50), default="FIELD_OFFICER")
    status = Column(String(50), nullable=False) # VERIFIED, FALSE_POSITIVE, REJECTED, UNDER_REVIEW
    comments = Column(Text, nullable=False)
    gps_coordinates = Column(String(100), nullable=True) # "21.8423, 85.5812"
    evidence_notes = Column(Text, nullable=True)
    photo_urls = Column(JSON, default=list) # List of image URLs
    timestamp = Column(DateTime, default=datetime.utcnow)

    alert = relationship("Alert", back_populates="verifications")

class SatelliteObservation(Base):
    __tablename__ = "satellite_observations"

    id = Column(String(50), primary_key=True, index=True)
    platform = Column(String(50), nullable=False) # Sentinel-2, Sentinel-1, Landsat-8/9
    sensor_type = Column(String(50), nullable=False) # Optical, SAR
    region = Column(String(100), nullable=False, index=True)
    acquisition_date = Column(String(30), nullable=False, index=True)
    year = Column(Integer, nullable=False)
    cloud_coverage = Column(Float, default=0.0)
    cloud_masked = Column(Boolean, default=True)
    
    # Indices and band statistics
    mean_ndvi = Column(Float, default=0.0)
    mean_ndwi = Column(Float, default=0.0)
    mean_ndbi = Column(Float, default=0.0)
    mean_bsi = Column(Float, default=0.0)
    sar_vv_mean = Column(Float, default=0.0)
    sar_vh_mean = Column(Float, default=0.0)
    
    thumbnail_url = Column(String(255), nullable=True)
    metadata_json = Column(JSON, default=dict)

class DataSource(Base):
    __tablename__ = "data_sources"

    id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    source_type = Column(String(50), nullable=False) # Satellite, GIS, Cadastre, DEM
    provider = Column(String(100), nullable=False)
    purpose = Column(String(255), nullable=False)
    resolution = Column(String(50), nullable=False)
    update_frequency = Column(String(50), nullable=False)
    status = Column(String(50), default="ACTIVE / DEMO MODE")
    is_live = Column(Boolean, default=False)
    last_sync = Column(String(50), default="2026-08-20")
