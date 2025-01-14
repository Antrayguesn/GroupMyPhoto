#!/bin/python3

"""
Split big photo cluster
"""

import copy

from strategy.strategy import Strategy


class ClearEmptyClusterStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.STRATEGY_CODE = "001"

    def __clear_empty_cluster(self):
        for id, cluster in copy.deepcopy(self.clusters).items():
            if "photos" not in cluster or not cluster["photos"]:
                del self.cluster[id]

    def process(self):
        self.__clear_empty_cluster()
