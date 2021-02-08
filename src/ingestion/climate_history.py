#!/usr/bin/env python3

import csv
import os
import sys

from datetime import datetime
from elasticsearch_dsl import Document, Date, Float, Keyword, GeoPoint


from common.common import INDEX_NAME, CLIMATE_HISTORY_FIELDS


def load_climate_history(data_dir, file_type=".csv"):
    climate_history = []
    fields_count = len(CLIMATE_HISTORY_FIELDS)
    # Resursively check the dirs
    for root, _subdirs, files in os.walk(data_dir):
        # Looping through each file in the current dir
        for file in files:
            if file_type not in file:
                continue

            print(f"Reading file: {file}")

            station_name = file.replace("_", " ").lower()
            with open(f"{root}/{file}", newline="", encoding="ISO-8859-1") as climate_file:
                rows = csv.reader(climate_file, delimiter=",")

                for row in rows:
                    if not row:
                        continue

                    # Skip if not a data row
                    if not row[0] or row[0].strip().lower() not in station_name:
                        continue
                        
                    if len(row) != fields_count:
                        raise Exception(f"Error: Unexpected number of fields for the provided row: {row}")
                    
                    record = {}
                    for index, field_name in enumerate(CLIMATE_HISTORY_FIELDS):
                        field_value = row[index].strip()
                        if not field_value:
                            field_value = None

                        record[field_name] = field_value

                    climate_history.append(record)

    print("Finished reading all files")
    return climate_history

def ingest_climate_history(climate_history, es_client, BOMClimateHistory, init_index=True, batch=1000):
    """
    Ingest the climate history data into ES
    """
    # Create the mappings in ES
    if init_index:
        BOMClimateHistory.init()

    stations = es_client.get_all_stations_by_name()

    record_count = len(climate_history)
    buffer = []
    for index, record in enumerate(climate_history):
        station_id = None
        station_coordinates = None
        station_details = stations.get(record["station_name"])

        if station_details:
            station_id = station_details["id"]
            station_coordinates = station_details["coordinates"]

        document = BOMClimateHistory(
            # Required fields
            date=record["date"],
            station_name=record["station_name"],

            # Foreign fields
            station_id=station_id,
            station_coordinates=station_coordinates,

            # Data fields
            evapotranspiration=record["evapotranspiration"],
            rain=record["rain"],
            pan_evaporation=record["pan_evaporation"],
            maximum_temperature=record["maximum_temperature"],
            minimum_temperature=record["minimum_temperature"],
            maximum_relative_humidity=record["maximum_relative_humidity"],
            minimum_relative_humidity=record["minimum_relative_humidity"],
            average_10m_wind_speed=record["average_10m_wind_speed"],
            solar_rediation=record["solar_rediation"],
        )

        buffer.append(document)

        # Reach the batch size or the last doc
        if not index % batch or index == record_count-1 :
            if not index:
                continue
            
            es_client.bulk_ingestion(buffer)
            buffer.clear()

            print(f"Ingested {index+1} out of total {record_count} documents")


class BOMClimateHistory(Document):
    # id = Keyword()
    date = Date(required=True, format="dd/mm/yyyy")
    station_name = Keyword(required=True)
    station_id = Keyword()
    station_coordinates = GeoPoint()
    evapotranspiration = Float()
    rain = Float()
    pan_evaporation = Float()
    maximum_temperature = Float()
    minimum_temperature = Float()
    maximum_relative_humidity = Float()
    minimum_relative_humidity = Float()
    average_10m_wind_speed = Float()
    solar_rediation = Float()
    last_update_date = Date()

    def save(self):
        self.last_updated_date = datetime.now()
        super().save()

    class Index:
        name = INDEX_NAME["history"]
        settings = {"number_of_shards": 2, "number_of_replicas": 1}