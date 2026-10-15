from typing import List, Dict, Any, Optional, Tuple
from app.services.satellite.cdse_catalog import RealSatelliteObservationMetadata

class SceneSelector:
    """
    Intelligent scene selector:
    - Ranks optical scenes by cloud cover
    - Evaluates optical usability threshold
    - Automatically selects Sentinel-1 SAR radar observations during cloudy conditions
    """

    @staticmethod
    def rank_and_select_scenes(
        observations: List[RealSatelliteObservationMetadata],
        max_cloud_cover: float = 30.0,
        prefer_radar_on_cloud: bool = True
    ) -> Dict[str, Any]:
        s2_scenes = [obs for obs in observations if obs.mission == "Sentinel-2"]
        s1_scenes = [obs for obs in observations if obs.mission == "Sentinel-1"]

        # Sort optical scenes by lowest cloud cover
        s2_scenes.sort(key=lambda x: (x.cloud_cover if x.cloud_cover is not None else 100.0))

        # Check for usable optical observation
        usable_s2 = [s for s in s2_scenes if s.cloud_cover is not None and s.cloud_cover <= max_cloud_cover]

        selected_optical: Optional[RealSatelliteObservationMetadata] = usable_s2[0] if usable_s2 else (s2_scenes[0] if s2_scenes else None)
        selected_sar: Optional[RealSatelliteObservationMetadata] = s1_scenes[0] if s1_scenes else None

        optical_is_clear = selected_optical is not None and selected_optical.cloud_cover is not None and selected_optical.cloud_cover <= max_cloud_cover

        status_message = ""
        primary_selection: Optional[RealSatelliteObservationMetadata] = None

        if optical_is_clear and selected_optical:
            primary_selection = selected_optical
            status_message = f"Optimal clear optical observation selected (Sentinel-2, Cloud Cover: {selected_optical.cloud_cover}%)."
        elif prefer_radar_on_cloud and selected_sar:
            primary_selection = selected_sar
            cloud_str = f"{selected_optical.cloud_cover}%" if selected_optical and selected_optical.cloud_cover is not None else "unavailable"
            status_message = (
                f"Sentinel-2 optical observation rejected due to cloud cover ({cloud_str} > {max_cloud_cover}%). "
                f"Sentinel-1 SAR C-Band radar observation selected for all-weather penetration."
            )
        else:
            primary_selection = selected_optical or selected_sar
            status_message = "Selected latest available satellite observation."

        return {
            "primary_observation": primary_selection,
            "selected_optical": selected_optical,
            "selected_sar": selected_sar,
            "optical_is_clear": optical_is_clear,
            "explanation": status_message,
            "total_candidates": len(observations),
            "optical_candidates": len(s2_scenes),
            "sar_candidates": len(s1_scenes)
        }

scene_selector = SceneSelector()
