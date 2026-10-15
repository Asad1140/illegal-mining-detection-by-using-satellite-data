import httpx
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger("illegal-mining-detection.geocoding")

class GeocodingService:
    """
    Worldwide location search using OpenStreetMap Nominatim API.
    """
    NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

    async def search_location(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Geocodes a place, district, or mine name to latitude, longitude, and bounding box.
        """
        if not query or len(query.strip()) < 2:
            return []

        headers = {
            "User-Agent": "IllegalMiningDetection-Surveillance/2.0 (Environmental-Decision-Support)"
        }
        params = {
            "q": query,
            "format": "json",
            "polygon_geojson": "1",
            "limit": str(limit),
            "addressdetails": "1"
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(self.NOMINATIM_URL, params=params, headers=headers)
                if resp.status_code == 200:
                    data = resp.json()
                    results = []
                    for item in data:
                        bbox = item.get("boundingbox", [])
                        # Nominatim returns bbox as [min_lat, max_lat, min_lon, max_lon]
                        std_bbox = [float(bbox[2]), float(bbox[0]), float(bbox[3]), float(bbox[1])] if len(bbox) == 4 else None
                        
                        results.append({
                            "display_name": item.get("display_name"),
                            "lat": float(item.get("lat")),
                            "lon": float(item.get("lon")),
                            "type": item.get("type"),
                            "class": item.get("class"),
                            "bbox": std_bbox,
                            "geojson": item.get("geojson")
                        })
                    return results
                else:
                    logger.warning(f"Nominatim geocoding error: HTTP {resp.status_code}")
                    return []
        except Exception as e:
            logger.error(f"Geocoding request failed: {e}")
            return []

geocoding_service = GeocodingService()
