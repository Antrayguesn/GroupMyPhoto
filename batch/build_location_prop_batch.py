"""
Date time cluster
"""
import copy

from batch.batch import Batch


class BuildLocationPropBatch(Batch):
    def __build_location_props(self):
        for id_cluster, cluster in copy.deepcopy(self.clusters).items():
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
