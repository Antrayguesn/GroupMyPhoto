#!/bin/python3

"""
Split big photo cluster
"""

import copy
import uuid

from travel_box_api.utils.load_images import load_images_from_paths_list
from travel_box_api.utils.clusterization import clusterize
from travel_box_api.strategy.strategy import Strategy


class FindUrbanClusterStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.STRATEGY_CODE = "005"

    def _urbanize(self):
        clusters_copy = copy.deepcopy(self.clusters)
        for cluster, cluster_data in self.clusters.items():
            cluster_len = len(cluster_data["photos"])

            if cluster_len > 150:
                paths_list = list([v["path"] for v in cluster_data["photos"].values()])
                data_images = load_images_from_paths_list(paths_list)
                del clusters_copy[cluster]
                # Clusterization par coordonnées GPS (Point les proches proche à 200m)
                new_clusters = clusterize(data_images, 0.5)

                for id, new_cluster in new_clusters.items():
                    if id != "ICanGroupThem":
                        uuid_group = str(uuid.uuid4())
                        clusters_copy[uuid_group] = new_cluster
                        clusters_copy[uuid_group]["urbanized"] = True

        return clusters_copy

    def process(self):
        self.clusters = self._urbanize()
