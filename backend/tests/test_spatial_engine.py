import pytest
from app.gis.spatial_engine import analyze_disturbance_spatial_boundary, degrees_to_meters
from app.gis.geojson_loader import get_demo_gis_layers

def test_spatial_engine_outside_lease():
    layers = get_demo_gis_layers("Keonjhar")
    leases = layers["mining_leases"]
    # Flagship alert disturbance outside lease
    flagship_disturbance = layers["disturbances"]["features"][0]["geometry"]
    
    result = analyze_disturbance_spatial_boundary(flagship_disturbance, leases, buffer_distance_m=500.0)
    assert result.is_inside_lease is False
    assert result.distance_from_lease_meters > 0.0
    assert "OUTSIDE" in result.relationship or "BUFFER" in result.relationship

def test_spatial_engine_inside_lease():
    layers = get_demo_gis_layers("Keonjhar")
    leases = layers["mining_leases"]
    inside_disturbance = layers["disturbances"]["features"][2]["geometry"]
    
    result = analyze_disturbance_spatial_boundary(inside_disturbance, leases, buffer_distance_m=500.0)
    assert result.is_inside_lease is True
    assert result.distance_from_lease_meters == 0.0
    assert result.relationship == "INSIDE AUTHORIZED LEASE"
