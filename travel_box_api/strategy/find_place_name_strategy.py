#!/bin/python3

"""
Find name places from coord
"""
import requests
import time
import copy
import re

from travel_box_api.utils.country_code import COUNTRY_CODE
from travel_box_api.strategy.strategy import Strategy

from travel_box_api.data.log import DEBUG_FIND_CLUSTER_PLACE

# DUCKDUCK_URL = "https://duckduckgo.com/?q={search}&kl={locale}&format=json&kp=-2&kc=1&kaf=1"
DUCKDUCK_URL = "https://duckduckgo.com/?q={search}&format=json"
NOMINATIM_API = "https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"


class FindPlaceNameStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.STRATEGY_CODE = "004"

    def _find_place_name(self):
        new_metadatas = copy.deepcopy(self.clusters)
        for cluster, metadata in self.clusters.items():
            try:
                coord = metadata["centroid"]
            except KeyError:
                continue

            if "continent" in metadata \
               or "region" in metadata \
               or "country" in metadata \
               or "place" in metadata:
                continue
            
            self.log(DEBUG_FIND_CLUSTER_PLACE, f"Finding the place for the cluster {cluster}", cluster_id=cluster)

            try:
                ret = requests.get(NOMINATIM_API.format(lat=coord[0], lon=coord[1]), headers={"User-agent": "classify - v0.1", "Accept-Language": "fr-FR, en;q=0.8"})
            except KeyboardInterrupt:
                exit()
            # I have realy bad connection ... If the request timeout, we play again the scrpit again
            except Exception:
                continue

            res = ret.json()

            if "error" in res:
                continue

            region = None
            if "city" in res["address"]:
                region = res["address"]["city"]
            elif "village" in res["address"]:
                region = res["address"]["village"]
            elif "hamlet" in res["address"]:
                region = res["address"]["hamlet"]
            elif "town" in res["address"]:
                region = res["address"]["town"]
            elif "town" in res["address"]:
                region = res["address"]["town"]
            elif "county" in res["address"]:
                region = res["address"]["county"]
            else:
                region = ""

            country = res["address"]["country"]
            if "name" in res and res["name"]:
                place = res["name"]
            else:
                # On filtre les numero de rue
                display_name = res["display_name"]
                if re.match(r"^[0-9]* ", display_name):
                    place = display_name.split(",")[0]
                else:
                    place = display_name.split(",")[1]

            # L'API nominatim impose un delai de 1 sec entre chaque requete
            time.sleep(1)

            try:
                new_metadatas[cluster]["continent"] = COUNTRY_CODE[res["address"]["country_code"]]["continent"]["fr"]
            except KeyError as e:
                print(f"Impossible de trouvé la clé {e}")
            new_metadatas[cluster]["country"] = country.strip()
            new_metadatas[cluster]["region"] = region.strip()
            new_metadatas[cluster]["place"] = place.strip()
            new_metadatas[cluster]["address"] = res["address"]
        return new_metadatas

    def process(self):
        self.clusters = self._find_place_name()
