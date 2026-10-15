from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.core.config import settings
from app.core.database import engine, Base, SessionLocal
from app.services.alert_service import alert_service

# Import API Routers
from app.api.auth_routes import router as auth_router
from app.api.dashboard_routes import router as dashboard_router
from app.api.alert_routes import router as alert_router
from app.api.mine_routes import router as mine_router
from app.api.satellite_routes import router as satellite_router
from app.api.geocode_routes import router as geocode_router
from app.api.ai_routes import router as ai_router
from app.api.verification_routes import router as verification_router
from app.api.settings_routes import router as settings_router
from app.api.reports_routes import router as reports_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("illegal-mining-detection")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables and seed initial demo data
    logger.info("Initializing Illegal Mining Detection by Using Satellite Data database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        alert_service.seed_initial_data(db)
        logger.info("Demo mining leases, alerts, and GIS records initialized successfully.")
    except Exception as e:
        logger.error(f"Error seeding initial data: {e}")
    finally:
        db.close()
    
    yield
    logger.info("Shutting down Illegal Mining Detection by Using Satellite Data backend...")

app = FastAPI(
    title="Illegal Mining Detection by Using Satellite Data",
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    lifespan=lifespan
)

# CORS Configuration for local frontend and preview development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers with /api prefix
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(dashboard_router, prefix=settings.API_V1_STR)
app.include_router(alert_router, prefix=settings.API_V1_STR)
app.include_router(mine_router, prefix=settings.API_V1_STR)
app.include_router(satellite_router, prefix=settings.API_V1_STR)
app.include_router(geocode_router, prefix=settings.API_V1_STR)
app.include_router(ai_router, prefix=settings.API_V1_STR)
app.include_router(verification_router, prefix=settings.API_V1_STR)
app.include_router(settings_router, prefix=settings.API_V1_STR)
app.include_router(reports_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "system": settings.PROJECT_NAME,
        "tagline": "AI-Powered Satellite Mining Surveillance, Change Detection & Early-Warning System",
        "version": settings.VERSION,
        "mode": "REAL SATELLITE DATA" if settings.REAL_DATA_MODE else "DEMO MODE",
        "data_source": "Copernicus Data Space Ecosystem (CDSE)",
        "docs_url": "/docs",
        "disclaimer": settings.DISCLAIMER
    }

@app.get("/health")
def health_check():
    return {
        "status": "HEALTHY",
        "database": "CONNECTED",
        "mode": "REAL SATELLITE DATA" if settings.REAL_DATA_MODE else "DEMO MODE",
        "satellite_engine": "READY (Copernicus CDSE Catalog)",
        "ai_models": "OPERATIONAL (Spectral & Radar Baseline Engine)"
    }
