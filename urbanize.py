import json
import sys
import copy

from group.load_images import load_images_from_paths_list
from group.clusterization import clusterize

clusters = {}

with sys.stdin as database:
  clusters = json.load(database)


def urbanize(clusters: dict):
  clusters_copy = copy.deepcopy(clusters)
  for cluster in clusters:
    cluster_data = clusters[cluster]
    cluster_len = len(cluster_data["photos"])
    if cluster_len > 150:
      paths_list = list(cluster_data["photos"].values())
      data_images = load_images_from_paths_list(paths_list)
      del clusters_copy[cluster]
      # Clusterization par coordonnées GPS (Point les proches proche à 200m)
      new_clusters = clusterize(data_images, 0.5)
      for id, new_cluster in new_clusters.items():
        if id != "ICanGroupThem":
          clusters_copy[int(cluster) * 100 + int(id)] = new_cluster

  return clusters_copy


print(json.dumps(urbanize(clusters)))
