#!/bin/python3
from strategy.strategy import Strategy


class UpdateClusterStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.STRATEGY_CODE = "015"

    def process(self, cluster_id, data):
        try:
            self.clusters[str(cluster_id)].update(data)
            if "continent" in data \
               or "region" in data \
               or "country" in data \
               or "place" in data:
                self.clusters[str(cluster_id)]["location"] = None
        except KeyError:
            self.log("DEBUG_9999", "Impossible de trouver le cluster")
            return {}
        return {}
