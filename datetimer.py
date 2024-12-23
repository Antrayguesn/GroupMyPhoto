#!/bin/python3

"""
Date time cluster
"""

import json
import sys
import copy

from group.load_images import load_images_from_paths_list
from group.clusterization import clusterize

clusters = {}

with sys.stdin as database:
    clusters = json.load(database)

def datetimer(clusters: dict):
    for cluster_id, cluster in copy.deepcopy(clusters).items():
        sorted_date_image = sorted(cluster["photos"].items(), key=lambda item: item[1]["datetime"])
        old_time   = None
        first_time = None
        end_time   = None
        for sha, image in sorted_date_image:
            image_time = image["datetime"]
            if old_time is None:
                old_time = image_time
            if first_time is None:
                first_time = image_time
            #print(image_time, first_time, end_time, old_time, image_time-old_time)
            if (image_time - old_time) > 3600 * 2:
                end_time = image_time
                try:
                    clusters[cluster_id]["periode"].append((first_time, end_time))
                except KeyError:
                    clusters[cluster_id]["periode"] = []
                    clusters[cluster_id]["periode"].append((first_time, end_time))

                first_time = end_time = None
            else:
                old_date = image_time
        if first_time is not None:
            end_time = image_time
            try:
                clusters[cluster_id]["periode"].append((first_time, end_time))
            except KeyError:
                clusters[cluster_id]["periode"] = [(first_time, end_time)]
    return clusters
            
print(json.dumps(datetimer(clusters)))
