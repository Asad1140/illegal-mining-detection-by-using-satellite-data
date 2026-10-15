from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.schemas import GeocodeSearchRequest, GeocodeResultItem
from app.services.geocoding_service import geocoding_service

router = APIRouter(prefix="/geocode", tags=["Worldwide Location Geocoding"])

@router.post("/search", response_model=List[GeocodeResultItem])
async def geocode_location_search(req: GeocodeSearchRequest):
    """
    Search for global locations, mining districts, or coordinates by name
    using OpenStreetMap Nominatim.
    """
    try:
        results = await geocoding_service.search_location(req.query, limit=req.limit)
        return [
            GeocodeResultItem(
                display_name=r["display_name"],
                lat=r["lat"],
                lon=r["lon"],
                type=r.get("type"),
                class_name=r.get("class"),
                bbox=r.get("bbox"),
                geojson=r.get("geojson")
            )
            for r in results
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Geocoding service error: {str(e)}")
