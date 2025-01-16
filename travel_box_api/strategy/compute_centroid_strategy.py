#!/bin/python3

"""
Date time cluster
"""

from travel_box_api.utils.clusterization import compute_centroid
from travel_box_api.strategy.strategy import Strategy


class ComputeCentroidStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.STRATEGY_CODE = "002"

    def _compute_centroid(self):
        return compute_centroid(self.clusters)

    def process(self):
        self.clusters = self._compute_centroid()
