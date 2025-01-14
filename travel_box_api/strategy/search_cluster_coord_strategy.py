#!/bin/python3

"""
Date time cluster
"""

import time
import requests

from strategy.strategy import Strategy

IMPORT_DIR_PATH = "sorted/"


# API_URL_NOMINATIM = "https://nominatim.openstreetmap.org/search.php?city={place}&country={country}&format=jsonv2&namedetails=1&extratags=1"
API_URL_NOMINATIM = "https://nominatim.openstreetmap.org/search.php?city={place}&country={country}&format=jsonv2"


class SearchClusterCoordStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.STRATEGY_CODE = "010"

    def __search_cluster_coord(self):
        for c_id, c in self.clusters.items():
            if "centroid" not in c or c["centroid"] is None:
                try:
                    req = requests.get(API_URL_NOMINATIM.format(place=c["place"], country=c.get("country","")), headers={"User-agent": "classify - v0.1", "Accept-Language": "fr-FR, en;q=0.8"})
                except KeyError as e:
                    self.log("WARNING_0010", f"Impossible de trouver la clé {e}")

                res = req.json()
                details = None
                if res:
                    details = res[0]
                else:
                    continue

                try:
                    c["display_name"] = details["display_name"]
                except KeyError:
                    continue

                try:
                    c["centroid"] = [float(details['lat']), float(details["lon"])]
                except KeyError:
                    continue

                time.sleep(0.1)

    def process(self):
        self.__search_cluster_coord()
