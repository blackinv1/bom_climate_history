
from datetime import datetime
from elasticsearch_dsl import Document, Date, Float, Keyword, GeoPoint

from common.common import INDEX_NAME

class BOMStations(Document):
    id = Keyword(required=True)
    name = Keyword(required=True)
    state = Keyword()
    rainfall_districts = Keyword()
    date_opened = Date()
    coordinates = GeoPoint()
    last_update_date = Date()

    def save(self):
        self.meta.id = self.id
        self.last_updated_date = datetime.now()
        super().save()

    class Index:
        name = INDEX_NAME["stations"]
        settings = {"number_of_shards": 2, "number_of_replicas": 1}


class BOMClimateHistory(Document):
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