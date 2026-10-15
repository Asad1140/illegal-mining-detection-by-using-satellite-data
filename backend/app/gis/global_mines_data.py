from typing import List, Dict, Any, Optional

GLOBAL_MINING_SITES: List[Dict[str, Any]] = [
    # 1. India
    {
        "id": "MINE-IN-KJ-01",
        "name": "Keonjhar Iron Ore Sector (Joda-Barbil)",
        "country": "India",
        "country_code": "IN",
        "region": "Odisha",
        "mineral": "Iron Ore",
        "center_lat": 21.8423,
        "center_lng": 85.5812,
        "zoom": 13,
        "source": "Indian Bureau of Mines (IBM) & Odisha Directorate of Mines",
        "source_url": "https://ibm.gov.in",
        "data_type": "OFFICIAL_LEASE",
        "has_authoritative_lease": True,
        "operator": "Odisha Mineral Exploration Ltd. / Tata Steel",
        "estimated_area_ha": 1240.0
    },
    {
        "id": "MINE-IN-BE-01",
        "name": "Bellary-Sandur Iron Ore Basin",
        "country": "India",
        "country_code": "IN",
        "region": "Karnataka",
        "mineral": "Iron Ore",
        "center_lat": 15.0841,
        "center_lng": 76.5418,
        "zoom": 13,
        "source": "Karnataka DMG Cadastre",
        "source_url": "https://mines.karnataka.gov.in",
        "data_type": "OFFICIAL_LEASE",
        "has_authoritative_lease": True,
        "operator": "National Mineral Development Corporation (NMDC)",
        "estimated_area_ha": 980.0
    },
    {
        "id": "MINE-IN-SU-01",
        "name": "Sukinda Chromite Valley",
        "country": "India",
        "country_code": "IN",
        "region": "Odisha",
        "mineral": "Chromite",
        "center_lat": 21.0289,
        "center_lng": 85.8245,
        "zoom": 13,
        "source": "Odisha Mining Cadastre",
        "source_url": "https://odishamining.in",
        "data_type": "OFFICIAL_LEASE",
        "has_authoritative_lease": True,
        "operator": "Odisha Mining Corporation (OMC)",
        "estimated_area_ha": 650.0
    },
    {
        "id": "MINE-IN-SI-01",
        "name": "Singrauli Northern Coalfield",
        "country": "India",
        "country_code": "IN",
        "region": "Madhya Pradesh",
        "mineral": "Coal",
        "center_lat": 24.1952,
        "center_lng": 82.6641,
        "zoom": 13,
        "source": "Coal India Cadastral GIS",
        "source_url": "https://coalindia.in",
        "data_type": "OFFICIAL_LEASE",
        "has_authoritative_lease": True,
        "operator": "Northern Coalfields Limited (NCL)",
        "estimated_area_ha": 2100.0
    },

    # 2. Australia
    {
        "id": "MINE-AU-PIL-01",
        "name": "Pilbara Iron Ore Complex (Mount Whaleback / Newman)",
        "country": "Australia",
        "country_code": "AU",
        "region": "Western Australia",
        "mineral": "Iron Ore",
        "center_lat": -23.3631,
        "center_lng": 119.6714,
        "zoom": 13,
        "source": "Geoscience Australia & WA Dept of Mines",
        "source_url": "https://www.dmp.wa.gov.au",
        "data_type": "MINING_FOOTPRINT",
        "has_authoritative_lease": False,
        "operator": "BHP / Rio Tinto",
        "estimated_area_ha": 3450.0
    },
    {
        "id": "MINE-AU-KAL-02",
        "name": "Kalgoorlie Fimiston Super Pit (Gold)",
        "country": "Australia",
        "country_code": "AU",
        "region": "Western Australia",
        "mineral": "Gold",
        "center_lat": -30.7745,
        "center_lng": 121.5034,
        "zoom": 14,
        "source": "Geoscience Australia",
        "source_url": "https://www.ga.gov.au",
        "data_type": "MINING_FOOTPRINT",
        "has_authoritative_lease": False,
        "operator": "Northern Star Resources",
        "estimated_area_ha": 820.0
    },

    # 3. Brazil
    {
        "id": "MINE-BR-CAR-01",
        "name": "Carajás Mining Complex (N4W / N5)",
        "country": "Brazil",
        "country_code": "BR",
        "region": "Pará (Amazon Rainforest Basin)",
        "mineral": "Iron Ore",
        "center_lat": -6.0592,
        "center_lng": -50.1834,
        "zoom": 13,
        "source": "Agência Nacional de Mineração (ANM) Brazil",
        "source_url": "https://www.gov.br/anm",
        "data_type": "MINING_FOOTPRINT",
        "has_authoritative_lease": False,
        "operator": "Vale S.A.",
        "estimated_area_ha": 5200.0
    },

    # 4. Chile
    {
        "id": "MINE-CL-ESC-01",
        "name": "Minera Escondida (Atacama Desert)",
        "country": "Chile",
        "country_code": "CL",
        "region": "Antofagasta",
        "mineral": "Copper",
        "center_lat": -24.2691,
        "center_lng": -69.0722,
        "zoom": 13,
        "source": "SERNAGEOMIN Chile National Mining Cadastre",
        "source_url": "https://www.sernageomin.cl",
        "data_type": "MINING_FOOTPRINT",
        "has_authoritative_lease": False,
        "operator": "BHP / Rio Tinto",
        "estimated_area_ha": 4100.0
    },

    # 5. Canada
    {
        "id": "MINE-CA-SUD-01",
        "name": "Sudbury Basin Nickel-Copper Cluster",
        "country": "Canada",
        "country_code": "CA",
        "region": "Ontario",
        "mineral": "Nickel / Copper",
        "center_lat": 46.5218,
        "center_lng": -80.9542,
        "zoom": 13,
        "source": "Natural Resources Canada (NRCan)",
        "source_url": "https://natural-resources.canada.ca",
        "data_type": "MINING_FOOTPRINT",
        "has_authoritative_lease": False,
        "operator": "Vale Canada / Glencore",
        "estimated_area_ha": 1800.0
    },

    # 6. South Africa
    {
        "id": "MINE-ZA-RUS-01",
        "name": "Rustenburg Platinum Mines (Bushveld Complex)",
        "country": "South Africa",
        "country_code": "ZA",
        "region": "North West Province",
        "mineral": "Platinum / Palladium",
        "center_lat": -25.6421,
        "center_lng": 27.2845,
        "zoom": 13,
        "source": "Council for Geoscience South Africa",
        "source_url": "https://www.geoscience.org.za",
        "data_type": "MINING_FOOTPRINT",
        "has_authoritative_lease": False,
        "operator": "Anglo American Platinum / Impala",
        "estimated_area_ha": 2400.0
    },

    # 7. Indonesia
    {
        "id": "MINE-ID-GRA-01",
        "name": "Grasberg Copper-Gold Open Pit",
        "country": "Indonesia",
        "country_code": "ID",
        "region": "Central Papua",
        "mineral": "Copper / Gold",
        "center_lat": -4.0558,
        "center_lng": 137.1167,
        "zoom": 13,
        "source": "Ministry of Energy and Mineral Resources (ESDM)",
        "source_url": "https://www.esdm.go.id",
        "data_type": "MINING_FOOTPRINT",
        "has_authoritative_lease": False,
        "operator": "PT Freeport Indonesia",
        "estimated_area_ha": 3100.0
    },

    # 8. United States
    {
        "id": "MINE-US-BIN-01",
        "name": "Bingham Canyon Kennecott Open Pit",
        "country": "United States",
        "country_code": "US",
        "region": "Utah",
        "mineral": "Copper",
        "center_lat": 40.5222,
        "center_lng": -112.1508,
        "zoom": 13,
        "source": "USGS Mineral Resources Program",
        "source_url": "https://www.usgs.gov",
        "data_type": "MINING_FOOTPRINT",
        "has_authoritative_lease": False,
        "operator": "Rio Tinto Kennecott",
        "estimated_area_ha": 1900.0
    }
]

def get_all_global_mining_sites() -> List[Dict[str, Any]]:
    return GLOBAL_MINING_SITES

def get_mining_site_by_id(site_id: str) -> Optional[Dict[str, Any]]:
    return next((s for s in GLOBAL_MINING_SITES if s["id"] == site_id), None)
