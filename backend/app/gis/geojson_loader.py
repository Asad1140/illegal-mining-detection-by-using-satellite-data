import json
from typing import Dict, Any, List
from shapely.geometry import Polygon, MultiPolygon, shape, mapping

# Coordinate centers for demo regions in India
REGION_CENTERS = {
    "Keonjhar": {"lat": 21.8423, "lng": 85.5812, "state": "Odisha", "zoom": 13},
    "Bellary": {"lat": 15.0841, "lng": 76.5418, "state": "Karnataka", "zoom": 13},
    "Sukinda": {"lat": 21.0289, "lng": 85.8245, "state": "Odisha", "zoom": 13},
    "Singrauli": {"lat": 24.1952, "lng": 82.6641, "state": "Madhya Pradesh", "zoom": 13}
}

def create_polygon_coords(center_lat: float, center_lng: float, d_lat: float, d_lng: float, shape_type: str = "rect"):
    """Helper to generate polygon coordinates around an offset."""
    if shape_type == "rect":
        return [
            [center_lng - d_lng, center_lat - d_lat],
            [center_lng + d_lng, center_lat - d_lat],
            [center_lng + d_lng * 1.1, center_lat + d_lat * 0.9],
            [center_lng - d_lng * 0.9, center_lat + d_lat],
            [center_lng - d_lng, center_lat - d_lat]
        ]
    elif shape_type == "complex":
        return [
            [center_lng - d_lng, center_lat - d_lat],
            [center_lng, center_lat - d_lat * 1.2],
            [center_lng + d_lng * 1.3, center_lat - d_lat * 0.5],
            [center_lng + d_lng, center_lat + d_lat],
            [center_lng + d_lng * 0.2, center_lat + d_lat * 1.4],
            [center_lng - d_lng * 1.1, center_lat + d_lat * 0.8],
            [center_lng - d_lng, center_lat - d_lat]
        ]
    return [
        [center_lng - d_lng, center_lat - d_lat],
        [center_lng + d_lng, center_lat - d_lat],
        [center_lng + d_lng, center_lat + d_lat],
        [center_lng - d_lng, center_lat + d_lat],
        [center_lng - d_lng, center_lat - d_lat]
    ]

def get_demo_gis_layers(region_name: str = "Keonjhar") -> Dict[str, Any]:
    """Generates complete GIS layers for the requested region."""
    center = REGION_CENTERS.get(region_name, REGION_CENTERS["Keonjhar"])
    lat = center["lat"]
    lng = center["lng"]

    # 1. Registered Mining Lease Polygons
    leases_geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "id": f"ML-{region_name[:2].upper()}-01",
                "properties": {
                    "lease_id": f"ML-{region_name[:2].upper()}-01",
                    "name": f"{region_name} Central Iron/Mineral Block A",
                    "lessee": "Odisha Mineral Exploration Ltd.",
                    "mineral": "Iron Ore" if "Keonjhar" in region_name or "Bellary" in region_name else ("Chromite" if "Sukinda" in region_name else "Coal"),
                    "area_ha": 340.5,
                    "status": "ACTIVE",
                    "grant_date": "2015-04-12",
                    "expiry_date": "2035-04-11"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [create_polygon_coords(lat - 0.005, lng - 0.008, 0.007, 0.007, "complex")]
                }
            },
            {
                "type": "Feature",
                "id": f"ML-{region_name[:2].upper()}-02",
                "properties": {
                    "lease_id": f"ML-{region_name[:2].upper()}-02",
                    "name": f"{region_name} Northern Quarry Extension B",
                    "lessee": "Eastern Mining & Minerals Corp",
                    "mineral": "Iron Ore" if "Keonjhar" in region_name or "Bellary" in region_name else ("Chromite" if "Sukinda" in region_name else "Coal"),
                    "area_ha": 210.0,
                    "status": "ACTIVE",
                    "grant_date": "2018-09-01",
                    "expiry_date": "2038-08-31"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [create_polygon_coords(lat + 0.025, lng + 0.025, 0.007, 0.007, "rect")]
                }
            }
        ]
    }

    # 2. Compute 500m Surveillance Buffer Polygons with Shapely
    buffer_features = []
    for feat in leases_geojson["features"]:
        poly = Polygon(feat["geometry"]["coordinates"][0])
        # Degree approximate buffer (~0.0045 deg is roughly 500m)
        buf_poly = poly.buffer(0.0045)
        buffer_features.append({
            "type": "Feature",
            "properties": {
                "lease_id": feat["properties"]["lease_id"],
                "buffer_type": "500-Meter Surveillance Perimeter",
                "color": "#eab308"
            },
            "geometry": mapping(buf_poly)
        })
    surveillance_buffer_geojson = {
        "type": "FeatureCollection",
        "features": buffer_features
    }

    # 3. Detected Mining Disturbances (including Outside Lease Alert Zones)
    # The flagship demo alert: MG-2026-00421 in Keonjhar (Outside lease, 180m away, 14.2 ha)
    disturbances_geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "id": "MG-2026-00421",
                "properties": {
                    "alert_id": "MG-2026-00421",
                    "title": f"Potential Unauthorized Mining Excavation - {region_name} East",
                    "risk_score": 91.0,
                    "priority": "CRITICAL",
                    "disturbed_area_ha": 14.2,
                    "lease_status": "Outside registered lease",
                    "distance_from_lease_m": 180.0,
                    "confidence": 0.94,
                    "status": "PENDING",
                    "detection_date": "2026-08-18",
                    "fill_color": "#ef4444"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [create_polygon_coords(lat + 0.006, lng + 0.004, 0.0025, 0.003, "complex")]
                }
            },
            {
                "type": "Feature",
                "id": f"MG-2026-00388",
                "properties": {
                    "alert_id": f"MG-2026-00388",
                    "title": f"Perimeter Encroachment in 500m Buffer - {region_name} North",
                    "risk_score": 78.0,
                    "priority": "HIGH",
                    "disturbed_area_ha": 6.8,
                    "lease_status": "Within 500m Buffer Zone",
                    "distance_from_lease_m": 45.0,
                    "confidence": 0.89,
                    "status": "FIELD_VERIFICATION",
                    "detection_date": "2026-08-12",
                    "fill_color": "#f97316"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [create_polygon_coords(lat + 0.016, lng + 0.025, 0.002, 0.0025, "rect")]
                }
            },
            {
                "type": f"Feature",
                "id": f"MG-2026-00105",
                "properties": {
                    "alert_id": f"MG-2026-00105",
                    "title": f"Internal Pit Expansion - Lease ML-{region_name[:2].upper()}-01",
                    "risk_score": 38.0,
                    "priority": "MEDIUM",
                    "disturbed_area_ha": 22.4,
                    "lease_status": "Inside Authorized Lease",
                    "distance_from_lease_m": 0.0,
                    "confidence": 0.96,
                    "status": "VERIFIED",
                    "detection_date": "2026-07-28",
                    "fill_color": "#eab308"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [create_polygon_coords(lat - 0.005, lng - 0.008, 0.003, 0.003, "rect")]
                }
            }
        ]
    }

    # 4. Contextual Vector Layers: Mining Pits, Overburden Dumps, Forest, Water, Roads, Settlements
    pits_geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "Active Extraction Pit #1", "depth_m": 45.0, "type": "Active Pit"},
                "geometry": {"type": "Polygon", "coordinates": [create_polygon_coords(lat - 0.004, lng - 0.007, 0.004, 0.005)]}
            },
            {
                "type": "Feature",
                "properties": {"name": "Unauthorized Excavation Pit #2", "depth_m": 22.0, "type": "Unapproved Pit"},
                "geometry": {"type": "Polygon", "coordinates": [create_polygon_coords(lat + 0.010, lng + 0.012, 0.003, 0.004)]}
            }
        ]
    }

    dumps_geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "Overburden Dump Tier 1", "height_m": 30.0, "type": "Overburden Dump"},
                "geometry": {"type": "Polygon", "coordinates": [create_polygon_coords(lat - 0.012, lng - 0.002, 0.004, 0.004)]}
            },
            {
                "type": "Feature",
                "properties": {"name": "Illegal Waste Spoil Dump", "height_m": 15.0, "type": "Waste Spoil"},
                "geometry": {"type": "Polygon", "coordinates": [create_polygon_coords(lat + 0.014, lng + 0.009, 0.003, 0.003)]}
            }
        ]
    }

    forest_geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": f"{region_name} Reserved Forest Block", "density": "Dense Mixed Forest", "canopy_loss_pct": 34.5},
                "geometry": {"type": "Polygon", "coordinates": [create_polygon_coords(lat + 0.012, lng + 0.024, 0.015, 0.012, "complex")]}
            }
        ]
    }

    water_geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": f"{region_name} Stream / Drainage Catchment", "turbidity": "High Suspended Solids"},
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [lng - 0.030, lat - 0.020],
                        [lng - 0.010, lat - 0.005],
                        [lng + 0.005, lat + 0.010],
                        [lng + 0.025, lat + 0.025]
                    ]
                }
            }
        ]
    }

    roads_geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "Heavy Mineral Haulage Corridor", "surface": "Unpaved Mineral Road"},
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [lng - 0.025, lat + 0.015],
                        [lng - 0.005, lat + 0.008],
                        [lng + 0.010, lat + 0.011],
                        [lng + 0.030, lat + 0.005]
                    ]
                }
            }
        ]
    }

    settlements_geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": f"{region_name} Rural Settlement & Tribal Hamlet", "population": 1450},
                "geometry": {"type": "Polygon", "coordinates": [create_polygon_coords(lat - 0.022, lng + 0.015, 0.006, 0.008)]}
            }
        ]
    }

    return {
        "region": region_name,
        "center": center,
        "mining_leases": leases_geojson,
        "surveillance_buffers": surveillance_buffer_geojson,
        "disturbances": disturbances_geojson,
        "mining_pits": pits_geojson,
        "overburden_dumps": dumps_geojson,
        "forest_areas": forest_geojson,
        "water_bodies": water_geojson,
        "roads": roads_geojson,
        "settlements": settlements_geojson
    }
