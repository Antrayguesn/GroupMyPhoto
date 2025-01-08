#!/bin/python3

"""
Split big photo cluster
"""

import copy

from batch.batch import Batch


class MergeClusterSameLocation(Batch):
    def __merge_cluster(self):
        copy_clusters = copy.deepcopy(self.clusters)
        cluster_already_sorted = []

        for id_cluster, cluster in copy_clusters.items():
            if id_cluster not in cluster_already_sorted:
                for id_cluster_2, cluster_2 in copy_clusters.items():
                    if cluster["location"] == cluster_2["location"] and id_cluster != id_cluster_2:
                        self.clusters[str(id_cluster)]["photos"].update(self.clusters[str(id_cluster_2)]["photos"])
                        del self.clusters[str(id_cluster_2)]
                        cluster_already_sorted.append(id_cluster_2)

    def process(self):
        self.__merge_cluster()
