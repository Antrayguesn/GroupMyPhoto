#!/bin/python3

"""
Date time cluster
"""

import json
import sys
import copy

from group.load_images import load_images_from_paths_list
from group.clusterization import compute_centroid

clusters = {}

with sys.stdin as database:
    clusters = json.load(database)

def _compute_centroid(clusters: dict):
    return compute_centroid(clusters)

            
print(json.dumps(_compute_centroid(clusters)))
