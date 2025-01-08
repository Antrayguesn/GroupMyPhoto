#!/bin/python3

"""
Split big photo cluster
"""

import copy

from batch.batch import Batch
from utils.geo_function import distance


class ComputeFarestDistance(Batch):
    def __compute_farest_distance(self):
        for id, cluster in copy.deepcopy(self.clusters).items():
            centroid = cluster["centroid"]
            max_distance = 0
            for photo in cluster["photos"].values():
                photo_coord = photo["coord"]
                current_distance = distance(centroid, photo_coord)
                if max_distance < current_distance:
                    max_distance = current_distance
            self.clusters[id]["max_distance_km"] = max_distance

    def process(self):
        self.__compute_farest_distance()
