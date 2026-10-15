import pytest
import numpy as np
from app.services.satellite.sentinel2_service import sentinel2_processor
from app.services.satellite.sentinel1_service import sentinel1_processor
from app.services.satellite.scene_selector import scene_selector
from app.services.satellite.cdse_catalog import RealSatelliteObservationMetadata
from app.services.ai.change_detection_service import change_detection_service
from app.gis.spatial_engine import calculate_geodesic_polygon_area_ha, analyze_disturbance_spatial_boundary
from app.gis.global_mines_data import get_all_global_mining_sites
from shapely.geometry import Polygon

def test_sentinel2_indices_calculation():
    # Synthetic reflectance bands
    b02 = np.array([0.05, 0.10], dtype=np.float32) # Blue
    b03 = np.array([0.10, 0.15], dtype=np.float32) # Green
    b04 = np.array([0.08, 0.35], dtype=np.float32) # Red
    b08 = np.array([0.45, 0.15], dtype=np.float32) # NIR
    b11 = np.array([0.15, 0.45], dtype=np.float32) # SWIR1

    indices = sentinel2_processor.calculate_spectral_indices(b02, b03, b04, b08, b11)

    # Pixel 0: High vegetation -> High NDVI, Low BSI
    assert indices["NDVI"][0] > 0.5
    assert indices["BSI"][0] < 0.0

    # Pixel 1: Bare soil / Mining pit -> Low NDVI, High BSI
    assert indices["NDVI"][1] < 0.0
    assert indices["BSI"][1] > 0.2

def test_scl_cloud_masking():
    # SCL array: 4 = Vegetation, 9 = High prob cloud, 3 = Cloud shadow
    scl = np.array([4, 4, 9, 3], dtype=np.int32)
    data = {"NDVI": np.array([0.6, 0.7, 0.8, 0.5], dtype=np.float32)}

    masked, usable_pct = sentinel2_processor.apply_scl_cloud_mask(scl, data)

    # 2 out of 4 pixels are clear -> 50%
    assert usable_pct == 50.0
    assert np.isnan(masked["NDVI"][2])
    assert np.isnan(masked["NDVI"][3])
    assert not np.isnan(masked["NDVI"][0])

def test_sentinel1_sar_features():
    sar = sentinel1_processor.calculate_sar_features(
        vv_db=-7.5,
        vh_db=-15.0,
        baseline_vv_db=-14.2,
        baseline_vh_db=-17.0
    )
    assert sar["sar_ratio_vv_vh_db"] == 7.5
    assert sar["temporal_delta_vv_db"] == 6.7 # High positive shift indicates rough excavation
    assert sar["sar_anomaly_detected"] is True

def test_scene_selector_cloud_fallback():
    optical_cloudy = RealSatelliteObservationMetadata(
        product_id="s2-cloudy",
        product_name="S2A_MSIL2A_20260815",
        mission="Sentinel-2",
        sensor_type="Optical",
        processing_level="L2A",
        acquisition_date="2026-08-15T04:00:00Z",
        cloud_cover=88.5,
        footprint=None
    )
    sar_radar = RealSatelliteObservationMetadata(
        product_id="s1-radar",
        product_name="S1A_IW_GRDH_20260816",
        mission="Sentinel-1",
        sensor_type="SAR",
        processing_level="L1-GRD",
        acquisition_date="2026-08-16T12:00:00Z",
        cloud_cover=0.0,
        footprint=None
    )

    selection = scene_selector.rank_and_select_scenes(
        [optical_cloudy, sar_radar],
        max_cloud_cover=30.0,
        prefer_radar_on_cloud=True
    )
    assert selection["optical_is_clear"] is False
    assert selection["primary_observation"].mission == "Sentinel-1"
    assert "Sentinel-1" in selection["explanation"]

def test_global_geodesic_area_calculation():
    # Polygon in Australia (lat -23.36) vs Canada (lat +46.52) vs Equator (lat 0.0)
    # A box of 0.01 x 0.01 deg
    poly_aus = Polygon([(119.67, -23.36), (119.68, -23.36), (119.68, -23.35), (119.67, -23.35)])
    area_aus = calculate_geodesic_polygon_area_ha(poly_aus)
    assert area_aus > 100.0 # ~110 ha

    poly_can = Polygon([(-80.95, 46.52), (-80.94, 46.52), (-80.94, 46.53), (-80.95, 46.53)])
    area_can = calculate_geodesic_polygon_area_ha(poly_can)
    assert area_can > 50.0 and area_can < area_aus # Higher latitude = smaller area in deg space

def test_global_mining_inventory():
    sites = get_all_global_mining_sites()
    countries = {s["country"] for s in sites}
    assert "Australia" in countries
    assert "Brazil" in countries
    assert "Chile" in countries
    assert "Canada" in countries
    assert "South Africa" in countries
    assert "India" in countries
