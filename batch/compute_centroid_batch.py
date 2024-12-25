#!/bin/python3

"""
Date time cluster
"""

from utils.clusterization import compute_centroid
from batch.batch import Batch


class ComputeCentroidBatch(Batch):
    def _compute_centroid(self):
        return compute_centroid(self.clusters)

    def process(self):
        self.clusters = self._compute_centroid()
