#!/bin/python3
from travel_box_api.strategy.strategy import Strategy


class GetClustersStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.STRATEGY_CODE = "013"

    def process(self):
        return self.clusters
