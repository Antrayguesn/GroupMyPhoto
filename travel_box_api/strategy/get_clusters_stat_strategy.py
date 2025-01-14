#!/bin/python3
from strategy.strategy import Strategy


class GetClustersStatStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.STRATEGY_CODE = "019"

    def process(self):
        stat = {"continent": {}, "country": {}}
        for cluster_id, cluster in self.clusters.items():
            try:
                stat["continent"][cluster["continent"]] = None
                stat["country"][cluster["country"]] = None
            except KeyError:
                continue

        return {"nb_continent": len(stat["continent"].keys()), "nb_country": len(stat["country"].keys()), "country": list(stat["country"].keys())}
