#!/usr/bin/env python3

from datetime import datetime
from elasticsearch_dsl import Document, Date, Keyword, GeoPoint
import re

from common.common import INDEX_NAME, STATION_FIELDS


def load_stations(stations_file):
    """
    Load the station data file and tranfrom it into a more usable structure
    """

    with open(stations_file) as file:
        content = file.readlines()

    stations = []
    for row in content:
        # Matching the pattern using regex
        values = re.split(
            "^([0-9]{6})\s+([A-Z]{2,3})\s+([a-zA-Z0-9_]{1,4})\s+([\s\S]+)\s+([0-9]{8})..\s+(-?[0-9]\d*(\.\d+))\s+(-?[0-9]\d*(\.\d+))",
            row.strip(),
        )

        if len(values) != 11:
            raise Exception(f"Error: Provided row contains unsupported format: {row}")

        # e.g. sameple values ==> ['', '015590', 'NT', '15B', 'ALICE SPRINGS AIRPORT                   ', '19400101', '-23.7951', '.7951', '133.889', '.889', '']

        # remove undesired items
        values.pop(0)
        values.pop(6)
        values.pop(7)
        values.pop()

        # Strip name
        values[3] = values[3].strip()
        # Consturct coordinates
        coordinates = {"lat": values.pop(-2), "lon": values.pop(-1)}
        values.append(coordinates)

        # Transfrom the data into a dict
        station = {}
        for index in range(len(STATION_FIELDS)):
            station[STATION_FIELDS[index]] = values[index]

        # Add the station details
        stations.append(station)

    return stations


def ingest_stations(stations, BOMStations, init_index):
    """
    Ingest the stations data into ES
    """
    # Create the mappings in ES
    if init_index:
        BOMStations.init()

    for station in stations:
        document = BOMStations(
            id=station["id"],
            state=station["state"],
            rainfall_districts=station["rainfall_districts"],
            name=station["name"],
            date_opened=station["date_opened"],
            coordinates=station["coordinates"],
        )
        document.save()
