from elasticsearch_dsl import connections, Search
from elasticsearch_dsl.response import Hit
from elasticsearch.helpers import bulk

import os


class ESConfig(object):
    def __init__(self, cloud_id, username, password, timeout):
        self.cloud_id = cloud_id
        self.username = username
        self.password = password
        self.timeout = timeout


class ESException(Exception):
    pass


class ES(object):
    """
    Class for handling Elasticsearch querying, with additional helper functions
    Functions should return simple python types e.g. string, dict, map, list
    NOT elasticsearch_dsl types such as Hit, Result etc..
    """

    def __init__(self, config: ESConfig):
        connections.create_connection(
            cloud_id=config.cloud_id,
            http_auth=(config.username, config.password),
            timeout=config.timeout,
        )

    def _hit_to_dict(self, hit):
        """
        Helper function to return a transform a hit from scan() resonse to the same format with a hit from execute() response
        """
        return {
            "_index": hit.meta.index,
            "_id": hit.meta.id,
            "_source": hit.to_dict(),
        }

    def get_all_documents(self, index):
        """
        Retrieve all documents from ES for the provided index
        """
        search = Search(index=index)

        yield from (hit.to_dict() for hit in search.scan())

    def get_all_stations_by_name(self, stations_index="bom_stations"):
        """
        Get all documents from the stations index and tranfrom it into a dict using name as the keys
        """
        stations = {}
        for station in self.get_all_documents(stations_index):
            stations[station["name"]] = station

        return stations

    def bulk_ingestion(self, buffer):
        bulk(connections.get_connection(), (d.to_dict(True) for d in buffer))
