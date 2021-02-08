#!/usr/bin/env python3

from stations import load_stations, BOMStations
from ingestion.climate_history import load_climate_history, ingest_climate_history, BOMClimateHistory

from elasticsearch_client import ES, ESConfig

CREDENTIALS = {
    "cloud_id": "memory-optimized-deployment:YXVzdHJhbGlhLXNvdXRoZWFzdDEuZ2NwLmVsYXN0aWMtY2xvdWQuY29tJGEzNTUxZWYxOTdiMTRjZTI4NDI3ZDJlMDg5ZTBlNThmJDcyZGIxMzVkMGEwNjQ5ZDhhZjk2MGM1ZDNkNjZiYTQ3",
    "username": "elastic",
    "password": "PCPlFOzefe1IgQFg0NKR1TbF",
}

STATIONS_FILE = "data/tables/stations_db.txt"
CLIMATE_DATA_ROOT_DIR = "data/tables/nsw/young_airport"

def main():
    # Create an ES connection
    es_config = ESConfig(
        cloud_id=CREDENTIALS["cloud_id"],
        username=CREDENTIALS["username"],
        password=CREDENTIALS["password"],
        timeout=20
    )

    es_client = ES(es_config)

    # Load data from file
    # stations = load_stations(STATIONS_FILE)
    climate_history = load_climate_history(CLIMATE_DATA_ROOT_DIR)

    # ingest_stations(stations,BOMStations)

    ingest_climate_history(climate_history, es_client, BOMClimateHistory)


if __name__ == "__main__":
    main()
