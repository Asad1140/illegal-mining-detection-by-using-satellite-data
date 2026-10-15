import math
from typing import Dict, Any, List, Tuple, Optional
from shapely.geometry import shape, Polygon, MultiPolygon, Point
from shapely.ops import nearest_points

class SpatialIntersectionResult:
    def __init__(
        self,
        relationship: str,
        is_inside_lease: bool,
        is_within_buffer: bool,
        distance_from_lease_meters: float,
        overlap_area_ha: float,
        disturbed_area_ha: float,
        nearest_lease_id: Optional[str] = None,
        nearest_lease_name: Optional[str] = None,
        buffer_distance_configured_m: float = 500.0,
        authoritative_lease_available: bool = True
    ):
        self.relationship = relationship
        self.is_inside_lease = is_inside_lease
        self.is_within_buffer = is_within_buffer
        self.distance_from_lease_meters = round(distance_from_lease_meters, 2)
        self.overlap_area_ha = round(overlap_area_ha, 2)
        self.disturbed_area_ha = round(disturbed_area_ha, 2)
        self.nearest_lease_id = nearest_lease_id
        self.nearest_lease_name = nearest_lease_name
        self.buffer_distance_configured_m = buffer_distance_configured_m
        self.authoritative_lease_available = authoritative_lease_available

    def to_dict(self) -> Dict[str, Any]:
        if not self.authoritative_lease_available:
            compliance = "MONITORING DISTURBANCE ONLY (OFFICIAL LEASE DATA UNAVAILABLE)"
        elif self.is_inside_lease:
            compliance = "AUTHORIZED LEASE EXTRACTION"
        else:
            compliance = "POTENTIAL UNAUTHORIZED ACTIVITY (REQUIRES HUMAN VERIFICATION)"

        return {
            "relationship": self.relationship,
            "is_inside_lease": self.is_inside_lease,
            "is_within_buffer": self.is_within_buffer,
            "distance_from_lease_meters": self.distance_from_lease_meters,
            "overlap_area_ha": self.overlap_area_ha,
            "disturbed_area_ha": self.disturbed_area_ha,
            "nearest_lease_id": self.nearest_lease_id,
            "nearest_lease_name": self.nearest_lease_name,
            "buffer_distance_configured_m": self.buffer_distance_configured_m,
            "authoritative_lease_available": self.authoritative_lease_available,
            "compliance_classification": compliance
        }

def calculate_geodesic_polygon_area_ha(poly: Polygon) -> float:
    """
    Calculates accurate surface area in hectares for WGS84 lon/lat coordinates
    using the WGS84 ellipsoidal projection approximation across any latitude.
    """
    if poly.is_empty:
        return 0.0

    centroid_lat = poly.centroid.y
    lat_rad = math.radians(centroid_lat)
    
    # WGS84 metric meters per degree
    # 1 deg latitude ≈ 111,132.95 - 559.82 * cos(2*lat) + 1.175 * cos(4*lat)
    m_per_deg_lat = 111132.95 - 559.82 * math.cos(2 * lat_rad) + 1.175 * math.cos(4 * lat_rad)
    # 1 deg longitude ≈ 111412.84 * cos(lat) - 93.5 * cos(3*lat)
    m_per_deg_lon = 111412.84 * math.cos(lat_rad) - 93.5 * math.cos(3 * lat_rad)
    
    # Transform polygon degrees to meters
    exterior_coords = poly.exterior.coords
    meter_coords = [
        (x * m_per_deg_lon, y * m_per_deg_lat)
        for x, y in exterior_coords
    ]
    meter_poly = Polygon(meter_coords)
    sq_meters = abs(meter_poly.area)
    return round(sq_meters / 10000.0, 2)

def degrees_to_meters(deg_dist: float, lat: float = 0.0) -> float:
    """Accurate conversion from WGS84 degree distance to meters at a given latitude."""
    lat_rad = math.radians(lat)
    m_lat = 111132.95 - 559.82 * math.cos(2 * lat_rad)
    m_lon = 111412.84 * math.cos(lat_rad)
    avg_m_per_deg = (m_lat + m_lon) / 2.0
    return deg_dist * avg_m_per_deg

def meters_to_degrees(meters: float, lat: float = 0.0) -> float:
    """Conversion from meters to WGS84 degrees at a given latitude."""
    lat_rad = math.radians(lat)
    m_lon = max(1000.0, 111412.84 * math.cos(lat_rad))
    return meters / m_lon

def analyze_disturbance_spatial_boundary(
    disturbance_geojson: Dict[str, Any],
    leases_geojson: Optional[Dict[str, Any]] = None,
    buffer_distance_m: float = 500.0
) -> SpatialIntersectionResult:
    """
    Performs spatial intersection, 500m buffer containment, and distance analysis
    between detected mining disturbance and registered mining leases.
    """
    disturbance_poly = shape(disturbance_geojson) if "type" in disturbance_geojson else Polygon()
    if disturbance_poly.is_empty:
        return SpatialIntersectionResult(
            relationship="UNKNOWN / INVALID GEOMETRY",
            is_inside_lease=False,
            is_within_buffer=False,
            distance_from_lease_meters=0.0,
            overlap_area_ha=0.0,
            disturbed_area_ha=0.0,
            authoritative_lease_available=False
        )

    disturbed_ha = calculate_geodesic_polygon_area_ha(disturbance_poly)
    centroid_lat = disturbance_poly.centroid.y
    buffer_deg = meters_to_degrees(buffer_distance_m, centroid_lat)

    features = leases_geojson.get("features", []) if leases_geojson else []
    if not features:
        return SpatialIntersectionResult(
            relationship="LEGAL-STATUS ANALYSIS UNAVAILABLE (NO OFFICIAL LEASE DATA)",
            is_inside_lease=False,
            is_within_buffer=False,
            distance_from_lease_meters=0.0,
            overlap_area_ha=0.0,
            disturbed_area_ha=disturbed_ha,
            buffer_distance_configured_m=buffer_distance_m,
            authoritative_lease_available=False
        )

    best_match_lease_id = None
    best_match_lease_name = None
    min_dist_m = float("inf")
    inside_any_lease = False
    inside_buffer_zone = False
    total_overlap_ha = 0.0

    for feat in features:
        lease_geom = shape(feat["geometry"])
        props = feat.get("properties", {})
        l_id = props.get("lease_id", "Unknown")
        l_name = props.get("name", "Unknown Lease")

        # 1. Direct Containment check
        if lease_geom.contains(disturbance_poly) or disturbance_poly.intersection(lease_geom).area > 0.95 * disturbance_poly.area:
            inside_any_lease = True
            min_dist_m = 0.0
            best_match_lease_id = l_id
            best_match_lease_name = l_name
            overlap_geom = disturbance_poly.intersection(lease_geom)
            total_overlap_ha = calculate_geodesic_polygon_area_ha(overlap_geom)
            break

        # 2. Check overlap
        if disturbance_poly.intersects(lease_geom):
            overlap_geom = disturbance_poly.intersection(lease_geom)
            overlap_ha = calculate_geodesic_polygon_area_ha(overlap_geom)
            total_overlap_ha = max(total_overlap_ha, overlap_ha)

        # 3. Distance calculation
        dist_deg = disturbance_poly.distance(lease_geom)
        dist_m = degrees_to_meters(dist_deg, centroid_lat)

        if dist_m < min_dist_m:
            min_dist_m = dist_m
            best_match_lease_id = l_id
            best_match_lease_name = l_name

        # 4. Check 500m buffer
        lease_buffer = lease_geom.buffer(buffer_deg)
        if disturbance_poly.intersects(lease_buffer):
            inside_buffer_zone = True

    if inside_any_lease:
        rel = "INSIDE AUTHORIZED LEASE"
        min_dist_m = 0.0
    elif inside_buffer_zone or min_dist_m <= buffer_distance_m:
        rel = f"WITHIN {int(buffer_distance_m)}M SURVEILLANCE BUFFER"
    else:
        rel = "OUTSIDE LEASE & BUFFER"

    return SpatialIntersectionResult(
        relationship=rel,
        is_inside_lease=inside_any_lease,
        is_within_buffer=inside_buffer_zone,
        distance_from_lease_meters=min_dist_m if min_dist_m != float("inf") else 0.0,
        overlap_area_ha=total_overlap_ha,
        disturbed_area_ha=disturbed_ha,
        nearest_lease_id=best_match_lease_id,
        nearest_lease_name=best_match_lease_name,
        buffer_distance_configured_m=buffer_distance_m,
        authoritative_lease_available=True
    )
