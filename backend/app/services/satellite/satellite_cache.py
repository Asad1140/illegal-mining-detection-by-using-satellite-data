import hashlib
import json
import time
from typing import Dict, Any, Optional

class SatelliteCache:
    """
    In-memory and lightweight persistent cache for satellite search results
    and processed observation features.
    """
    def __init__(self, ttl_seconds: int = 3600):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._ttl = ttl_seconds

    @staticmethod
    def generate_aoi_hash(aoi: Any, start_date: str, end_date: str, sensors: list) -> str:
        payload = json.dumps({
            "aoi": aoi,
            "start": start_date,
            "end": end_date,
            "sensors": sorted(sensors) if sensors else []
        }, sort_keys=True)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]

    def get(self, key: str) -> Optional[Any]:
        entry = self._cache.get(key)
        if entry:
            if time.time() < entry["expires_at"]:
                return entry["data"]
            else:
                del self._cache[key]
        return None

    def set(self, key: str, data: Any, custom_ttl: Optional[int] = None):
        ttl = custom_ttl or self._ttl
        self._cache[key] = {
            "data": data,
            "expires_at": time.time() + ttl
        }

    def clear(self):
        self._cache.clear()

satellite_cache = SatelliteCache()
