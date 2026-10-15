# GIS Methodology & Spatial Analysis

## Coordinate Reference System
All spatial vector boundaries and raster grids use standard **WGS84 (EPSG:4326)**.

## Spatial Intersection Pipeline
1. **Registered Lease Polygons**: Official boundary coordinates from the State Directorate of Mines & Geology / IBM.
2. **500m Statutory Surveillance Buffer**: Geometrically expanded polygon buffer calculated via `shapely.geometry.Polygon.buffer()`.
3. **Distance Calculation**: Exact metric distance from nearest perimeter calculated using Vincenty/Haversine geodesics.
4. **Relationship Classification**:
   - `INSIDE AUTHORIZED LEASE` (0m distance, full overlap)
   - `WITHIN 500M SURVEILLANCE BUFFER` (1m - 500m distance from boundary)
   - `OUTSIDE LEASE & BUFFER` (> 500m from authorized boundary)

## Neutral Legal Standard
All non-lease extractions are classified as **Potential Unauthorized Activity** for decision support.
