#!/bin/python3

"""
Split big photo cluster
"""

import copy

from batch.batch import Batch


class ClearEmptyClusterBatch(Batch):
    def __clear_empty_cluster(self):
        for id, cluster in copy.deepcopy(self.clusters).items():
            if "photos" not in cluster or not cluster["photos"]:
                del self.cluster[id]

    def process(self):
        self.__merge_same_location()
