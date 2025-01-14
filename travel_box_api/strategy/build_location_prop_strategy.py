"""
Date time cluster
"""
import copy

from strategy.strategy import Strategy


class BuildLocationPropStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.STRATEGY_CODE = "011"

    def __build_location_props(self):
        for id_cluster, cluster in copy.deepcopy(self.clusters).items():
            if cluster.get("location", None):
                continue
            location = ""
            if "continent" in cluster and cluster["continent"]:
                location += cluster["continent"] + "/"
            if "country" in cluster and cluster["country"]:
                location += cluster["country"] + "/"
            if "region" in cluster and cluster["region"]:
                location += cluster["region"] + "/"
            if "place" in cluster and cluster["place"]:
                location += cluster["place"]
            self.clusters[id_cluster]["location"] = location.strip("/")

    def process(self):
        self.__build_location_props()
