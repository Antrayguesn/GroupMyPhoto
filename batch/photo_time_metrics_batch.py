#!/bin/python3

"""
Date time cluster
"""

import copy

from batch.batch import Batch


class PhotoTimeMetricsBatch(Batch):
    def _photo_time_metrics(self):
        for cluster_id, cluster in copy.deepcopy(self.clusters).items():
            sorted_date_image = sorted(cluster["photos"].items(), key=lambda item: item[1]["datetime"])
            last_image_datetime = None
            end_time_of_period = None
            first_time_of_period = None
            self.clusters[cluster_id]["periode"] = []
            for sha, image in sorted_date_image:
                image_time = image["datetime"]
                if last_image_datetime is None:
                    last_image_datetime = image_time
                if first_time_of_period is None:
                    first_time_of_period = image_time
                if (image_time - last_image_datetime) > 3600 * 2:
                    end_time_of_period = last_image_datetime
                    try:
                        self.clusters[cluster_id]["periode"].append((first_time_of_period, end_time_of_period))
                    except KeyError:
                        self.clusters[cluster_id]["periode"] = []
                        self.clusters[cluster_id]["periode"].append((first_time_of_period, end_time_of_period))

                    first_time_of_period = image_time
                    end_time_of_period = None
                    last_image_datetime = image_time
                else:
                    last_image_datetime = image_time
            if first_time_of_period is not None:
                end_time_of_period = image_time
                try:
                    self.clusters[cluster_id]["periode"].append((first_time_of_period, end_time_of_period))
                except KeyError:
                    self.clusters[cluster_id]["periode"] = [(first_time_of_period, end_time_of_period)]
        return self.clusters

    def process(self):
        self._photo_time_metrics()
