#!/bin/python3
from travel_box_api.strategy.strategy import Strategy


class DeletePhotoFromClusterStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.STRATEGY_CODE = "017"

    def process(self, cluster_id, photo_id):
        photo_to_del = self.clusters[cluster_id]["photos"][photo_id]
        try:
            self.clusters["BIN"]["photos"]["photo_id"] = photo_to_del
        except KeyError:
            self.clusters["BIN"] = {"place": "bin", "photos": {photo_id: photo_to_del}}
        del self.clusters[cluster_id]["photos"][photo_id]


