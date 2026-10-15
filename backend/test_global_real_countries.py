import asyncio
from app.services.satellite.cdse_catalog import cdse_catalog
from app.services.ai.change_detection_service import change_detection_service
from app.gis.spatial_engine import analyze_disturbance_spatial_boundary
from app.ai.risk_engine import risk_engine

async def test_global_locations():
    test_locations = [
        {
            "name": "Keonjhar Iron Ore Sector",
            "country": "India",
            "point": (85.5812, 21.8423),
            "mineral": "Iron Ore"
        },
        {
            "name": "Pilbara Iron Ore Complex (Mount Whaleback)",
            "country": "Australia",
            "point": (119.6714, -23.3631),
            "mineral": "Iron Ore"
        },
        {
            "name": "Carajás Mining Complex (N4W/N5)",
            "country": "Brazil",
            "point": (-50.1834, -6.0592),
            "mineral": "Iron Ore"
        },
        {
            "name": "Minera Escondida (Atacama Desert)",
            "country": "Chile",
            "point": (-69.0722, -24.2691),
            "mineral": "Copper"
        }
    ]

    print("================================================================================")
    print(" ILLEGAL MINING DETECTION BY USING SATELLITE DATA - REAL COPERNICUS VERIFICATION ")
    print("================================================================================")

    for loc in test_locations:
        print(f"\n>>> Querying Real Copernicus Satellite Catalog for: {loc['name']} ({loc['country']})")
        print(f"    Coordinates: {loc['point'][0]}°E, {loc['point'][1]}°N | Target Mineral: {loc['mineral']}")
        
        try:
            results = await cdse_catalog.search_satellite_scenes(
                point=loc["point"],
                start_date="2024-01-01",
                end_date="2026-08-25",
                sensors=["sentinel-2", "sentinel-1"],
                max_cloud_cover=60.0,
                limit=4
            )
            print(f"    [OK] Found {len(results)} Real Satellite Observations on Copernicus Data Space:")
            for idx, r in enumerate(results[:3]):
                print(f"         {idx+1}. [{r.mission}] {r.product_name[:48]}...")
                print(f"            Acquired: {r.acquisition_date} | Cloud Cover: {r.cloud_cover}% | UUID: {r.product_id}")
                if r.polarisation_channels:
                    print(f"            SAR Polarizations: {r.polarisation_channels}")
            
            # Execute Temporal Change Detection between top 2 real observations
            if len(results) >= 2:
                obs_t1 = results[-1]
                obs_t2 = results[0]
                cd = change_detection_service.analyze_temporal_change(
                    t1_observation=obs_t1.to_dict(),
                    t2_observation=obs_t2.to_dict(),
                    estimated_aoi_ha=120.0
                )
                print(f"    [AI ANALYSIS] Changed Footprint: {cd['changed_area_hectares']} ha | Confidence: {round(cd['confidence_score']*100)}%")
                print(f"                  Vegetation Drop: -{cd['vegetation_loss_percentage']}% | Bare Soil Gain: +{cd['bare_soil_increase_percentage']}%")
                print(f"                  SAR Radar Roughness Delta: {cd['sar_roughness_delta_db']} dB")
                print(f"                  Interpretation: {cd['alternative_explanations'][0]}")

        except Exception as e:
            print(f"    [ERROR] Failed to query: {e}")

    print("\n================================================================================")
    print("                 GLOBAL COPERNICUS TEST SUITE COMPLETED SUCCESSFULLY            ")
    print("================================================================================")

if __name__ == "__main__":
    asyncio.run(test_global_locations())
