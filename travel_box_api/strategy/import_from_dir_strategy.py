#!/bin/python3

"""
Date time cluster
"""

import os
import uuid

from travel_box_api.utils.load_images import load_images_from_paths_list

from travel_box_api.strategy.strategy import Strategy

IMPORT_DIR_PATH = "sorted/"


class ImportFromDirStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.STRATEGY_CODE = "000"

    def _import_from_dir(self):
        all_location = [c["location"] for c_id, c in self.clusters.items()]

        for root, dirs, files in os.walk(IMPORT_DIR_PATH, followlinks=True):
            if files:
                location = root[len(IMPORT_DIR_PATH):]
                if location not in all_location:
                    paths = [f"{root}/{f}" for f in files]
                    photos = load_images_from_paths_list(paths)
                    cluster_id = str(uuid.uuid4())
                    self.clusters[cluster_id] = {}
                    self.clusters[cluster_id]["location"] = location
                    splited_location = location.split("/")
                    self.clusters[cluster_id]["continent"] = splited_location[0]
                    self.clusters[cluster_id]["country"] = splited_location[1]
                    if len(splited_location) > 3:
                        self.clusters[cluster_id]["region"] = splited_location[2]
                        self.clusters[cluster_id]["place"] = splited_location[3]
                    else:
                        self.clusters[cluster_id]["place"] = splited_location[2]
                        self.clusters[cluster_id]["region"] = ""

                    self.clusters[cluster_id]["photos"] = {}
                    self.clusters[cluster_id]["imported"] = True
                    for _, photo in photos.items():
                        self.clusters[cluster_id]["photos"][photo.sha256] = photo.toJSON()

    def process(self):
        self._import_from_dir()
