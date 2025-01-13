#!/bin/python3

"""
Split big photo cluster
"""

import copy

from strategy.strategy import Strategy
from utils.geo_function import distance

from data.log import DEBUG_UNABLE_TO_FIND_CENTROID, DEBUG_NO_CENTROID


class ComputeFarestDistanceStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.STRATEGY_CODE = "003"

    def __compute_farest_distance(self):
        for id, cluster in copy.deepcopy(self.clusters).items():
            try:
                centroid = cluster["centroid"]
            except KeyError:
                self.log(DEBUG_UNABLE_TO_FIND_CENTROID, f"Impossible de trouver le centroid dans le cluster {id}")
            max_distance = 0
            for photo in cluster["photos"].values():
                if "coord" not in photo or photo["coord"] is None:
                    self.log(DEBUG_NO_CENTROID, f"No GPS coordinate for the photo {photo["path"]}", photo_path=photo["path"])
                    continue
                photo_coord = photo["coord"]

                current_distance = distance(centroid, photo_coord)
                if max_distance < current_distance:
                    max_distance = current_distance
            self.clusters[id]["max_distance_km"] = max_distance

    def process(self):
        self.__compute_farest_distance()
