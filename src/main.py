#!/usr/bin/env python3
import argparse
from common.helper import read_json_file
from ingestion.stations import load_stations, ingest_stations
from ingestion.climate_history import load_climate_history, ingest_climate_history

from elastic.elasticsearch_client import ES, ESConfig
from elastic.indices import BOMStations, BOMClimateHistory

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--climate-data-root-dir", default="data/tables/nsw/young_airport", help="Folder of to the climate history CSV files"
    )
    parser.add_argument(
        "--stations-file", default="data/tables/stations_db.txt", help="Path to stations list txt file"
    )
    parser.add_argument(
        "--es-creds-file", default="config/creds.json", help="Path to the ElasticSearch Cluster credentials file"
    )
    parser.add_argument(
        "--init-index", action="store_true", help="Flag if init the ES index",
    )

    args = parser.parse_args()
    init_index = args.init_index

    # Read the creds file
    es_creds = read_json_file(args.es_creds_file)

    # Create an ES connection
    es_config = ESConfig(
        cloud_id=es_creds["cloud_id"],
        username=es_creds["username"],
        password=es_creds["password"],
        timeout=20
    )

    es_client = ES(es_config)

    # Load data from file
    stations = load_stations(args.stations_file)
    climate_history = load_climate_history(args.climate_data_root_dir)

    # Ingest the data into ES
    ingest_stations(stations,BOMStations, init_index)
    ingest_climate_history(climate_history, es_client, BOMClimateHistory, init_index)


if __name__ == "__main__":
    main()
