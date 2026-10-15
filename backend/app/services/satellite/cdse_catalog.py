import urllib.parse
import httpx
import logging
from typing import List, Dict, Any, Optional, Tuple
from shapely.geometry import shape, Polygon, Point, box
from app.core.config import settings
from app.services.satellite.copernicus_auth import copernicus_auth

logger = logging.getLogger("illegal-mining-detection.satellite.catalog")

class RealSatelliteObservationMetadata:
    def __init__(
        self,
        product_id: str,
        product_name: str,
        mission: str,
        sensor_type: str,
        processing_level: str,
        acquisition_date: str,
        cloud_cover: Optional[float],
        footprint: Optional[Dict[str, Any]],
        polarisation_channels: Optional[str] = None,
        orbit_number: Optional[int] = None,
        orbit_direction: Optional[str] = None,
        quicklook_url: Optional[str] = None,
        content_length_bytes: Optional[int] = None,
        data_source: str = "Copernicus Data Space Ecosystem (CDSE)"
    ):
        self.product_id = product_id
        self.product_name = product_name
        self.mission = mission
        self.sensor_type = sensor_type
        self.processing_level = processing_level
        self.acquisition_date = acquisition_date
        self.cloud_cover = round(cloud_cover, 2) if cloud_cover is not None else None
        self.footprint = footprint
        self.polarisation_channels = polarisation_channels
        self.orbit_number = orbit_number
        self.orbit_direction = orbit_direction
        self.quicklook_url = quicklook_url
        self.content_length_bytes = content_length_bytes
        self.data_source = data_source

    def to_dict(self) -> Dict[str, Any]:
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "mission": self.mission,
            "sensor_type": self.sensor_type,
            "processing_level": self.processing_level,
            "acquisition_date": self.acquisition_date,
            "cloud_cover": self.cloud_cover,
            "footprint": self.footprint,
            "polarisation_channels": self.polarisation_channels,
            "orbit_number": self.orbit_number,
            "orbit_direction": self.orbit_direction,
            "quicklook_url": self.quicklook_url,
            "content_length_bytes": self.content_length_bytes,
            "data_source": self.data_source
        }

class CopernicusCatalogService:
    """
    Search and metadata catalog service for real Copernicus Sentinel-1 and Sentinel-2 data worldwide.
    """
    
    @staticmethod
    def _format_wkt_spatial_filter(aoi_geom: Optional[Dict[str, Any]], bbox: Optional[List[float]], point: Optional[Tuple[float, float]]) -> str:
        """Constructs OData WKT spatial intersection filter string."""
        if aoi_geom:
            geom = shape(aoi_geom)
            if isinstance(geom, Point):
                return f"OData.CSC.Intersects(area=geography'SRID=4326;POINT({geom.x} {geom.y})')"
            elif isinstance(geom, Polygon):
                # Simplify polygon if too many vertices for OData URL limit
                if len(geom.exterior.coords) > 20:
                    geom = geom.simplify(0.005)
                coords_str = ", ".join(f"{lon} {lat}" for lon, lat in geom.exterior.coords)
                return f"OData.CSC.Intersects(area=geography'SRID=4326;POLYGON(({coords_str}))')"
        
        if bbox and len(bbox) == 4:
            min_lon, min_lat, max_lon, max_lat = bbox
            coords_str = f"{min_lon} {min_lat}, {max_lon} {min_lat}, {max_lon} {max_lat}, {min_lon} {max_lat}, {min_lon} {min_lat}"
            return f"OData.CSC.Intersects(area=geography'SRID=4326;POLYGON(({coords_str}))')"

        if point and len(point) == 2:
            lon, lat = point
            return f"OData.CSC.Intersects(area=geography'SRID=4326;POINT({lon} {lat})')"

        # Default fallback to center of Keonjhar if unspecified
        return "OData.CSC.Intersects(area=geography'SRID=4326;POINT(85.58 21.84)')"

    async def search_satellite_scenes(
        self,
        aoi_geom: Optional[Dict[str, Any]] = None,
        bbox: Optional[List[float]] = None,
        point: Optional[Tuple[float, float]] = None,
        start_date: str = "2024-01-01T00:00:00.000Z",
        end_date: str = "2026-08-25T23:59:59.000Z",
        sensors: Optional[List[str]] = None,
        max_cloud_cover: float = 30.0,
        limit: int = 20
    ) -> List[RealSatelliteObservationMetadata]:
        """
        Executes live query against Copernicus Data Space Catalogue API
        to search for real Sentinel-2 L2A and Sentinel-1 GRD observations.
        """
        if sensors is None:
            sensors = ["sentinel-2", "sentinel-1"]

        # Normalize sensors list
        req_s2 = any("2" in s.lower() for s in sensors)
        req_s1 = any("1" in s.lower() for s in sensors)

        spatial_filter = self._format_wkt_spatial_filter(aoi_geom, bbox, point)

        # Standardize dates
        if "T" not in start_date:
            start_date = f"{start_date}T00:00:00.000Z"
        if "T" not in end_date:
            end_date = f"{end_date}T23:59:59.000Z"

        results: List[RealSatelliteObservationMetadata] = []
        headers = await copernicus_auth.get_auth_headers()

        async with httpx.AsyncClient(timeout=30.0) as client:
            # 1. Search Sentinel-2 L2A Optical Scenes
            if req_s2:
                s2_filter = (
                    f"Collection/Name eq 'SENTINEL-2' and contains(Name,'MSIL2A') and "
                    f"{spatial_filter} and ContentDate/Start gt {start_date} and "
                    f"ContentDate/Start lt {end_date}"
                )
                params = {
                    "$filter": s2_filter,
                    "$top": str(limit),
                    "$orderby": "ContentDate/Start desc",
                    "$expand": "Attributes"
                }
                url = f"{settings.CDSE_CATALOG_URL}?{urllib.parse.urlencode(params)}"
                try:
                    resp = await client.get(url, headers=headers)
                    if resp.status_code == 200:
                        data = resp.json()
                        for p in data.get("value", []):
                            attrs = {a["Name"]: a["Value"] for a in p.get("Attributes", [])}
                            cloud = attrs.get("cloudCover")
                            cloud_val = float(cloud) if cloud is not None else None

                            # Apply cloud cover filter
                            if cloud_val is not None and cloud_val > max_cloud_cover:
                                continue

                            obs = RealSatelliteObservationMetadata(
                                product_id=p["Id"],
                                product_name=p["Name"],
                                mission="Sentinel-2",
                                sensor_type="Optical Multispectral (MSI)",
                                processing_level="Level-2A (Surface Reflectance)",
                                acquisition_date=p["ContentDate"]["Start"],
                                cloud_cover=cloud_val,
                                footprint=p.get("GeoFootprint"),
                                orbit_number=attrs.get("orbitNumber"),
                                orbit_direction=attrs.get("orbitDirection"),
                                content_length_bytes=p.get("ContentLength")
                            )
                            results.append(obs)
                    else:
                        logger.warning(f"CDSE Sentinel-2 search error: HTTP {resp.status_code} - {resp.text}")
                except Exception as e:
                    logger.error(f"Error querying Sentinel-2 from CDSE: {e}")

            # 2. Search Sentinel-1 GRD SAR Radar Scenes
            if req_s1:
                s1_filter = (
                    f"Collection/Name eq 'SENTINEL-1' and contains(Name,'_GRD') and "
                    f"{spatial_filter} and ContentDate/Start gt {start_date} and "
                    f"ContentDate/Start lt {end_date}"
                )
                params = {
                    "$filter": s1_filter,
                    "$top": str(limit),
                    "$orderby": "ContentDate/Start desc",
                    "$expand": "Attributes"
                }
                url = f"{settings.CDSE_CATALOG_URL}?{urllib.parse.urlencode(params)}"
                try:
                    resp = await client.get(url, headers=headers)
                    if resp.status_code == 200:
                        data = resp.json()
                        for p in data.get("value", []):
                            attrs = {a["Name"]: a["Value"] for a in p.get("Attributes", [])}
                            pol = attrs.get("polarisationChannels", "VV+VH")

                            obs = RealSatelliteObservationMetadata(
                                product_id=p["Id"],
                                product_name=p["Name"],
                                mission="Sentinel-1",
                                sensor_type="Synthetic Aperture Radar (SAR C-Band)",
                                processing_level="Level-1 GRD (Ground Range Detected)",
                                acquisition_date=p["ContentDate"]["Start"],
                                cloud_cover=0.0, # Radar is unaffected by cloud cover
                                footprint=p.get("GeoFootprint"),
                                polarisation_channels=str(pol),
                                orbit_number=attrs.get("orbitNumber"),
                                orbit_direction=attrs.get("orbitDirection"),
                                content_length_bytes=p.get("ContentLength")
                            )
                            results.append(obs)
                    else:
                        logger.warning(f"CDSE Sentinel-1 search error: HTTP {resp.status_code} - {resp.text}")
                except Exception as e:
                    logger.error(f"Error querying Sentinel-1 from CDSE: {e}")

        # Sort all observations chronologically descending
        results.sort(key=lambda x: x.acquisition_date, reverse=True)
        return results

cdse_catalog = CopernicusCatalogService()
