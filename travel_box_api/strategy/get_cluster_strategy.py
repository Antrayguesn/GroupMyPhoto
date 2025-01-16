#!/bin/python3
from travel_box_api.strategy.strategy import Strategy


class GetClusterStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.STRATEGY_CODE = "012"

    def process(self, cluster_id):
        return self.clusters[cluster_id]
