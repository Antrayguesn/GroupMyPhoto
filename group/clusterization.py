from exif import Image
from math import cos, asin, sqrt, pi
from sklearn.cluster import DBSCAN
import numpy as np
import datetime
import os
import sys
import shutil
import uuid
import json
import hashlib

def _create_clusterize(data_images: dict, eps_km: float):
  coordinates_list = [i.coord for i in data_images.values() if i.coord]
  photo_paths = [i.path for i in data_images.values() if i.coord]
  
  coords = np.array(coordinates_list)
  
  # Conversion en radians
  eps_in_radians = eps_km / 6371
  
  # Clustering by DBSCAN 
  db = DBSCAN(eps=eps_in_radians, min_samples=3, metric='haversine').fit(np.radians(coords))
  
  labels = db.labels_
  
  # labelize photo paths
  clusters = {}
  for label, path, coord in zip(labels, photo_paths, coords):
    if label not in clusters:
      clusters[label] = []
    clusters[label].append(data_images[path])
  
  return clusters

def clusterize(data_images: dict, eps_km: float):
  clusters = _create_clusterize(data_images, eps_km)
  clusters_with_data = {}
  # Cluster by GPS
  for cluster_id, items in clusters.items():
    paths = [item.path for item in items]
    cluster_coords = np.array([item.coord for item in items])
    cluster_datetime = np.array([item.datetime.timestamp() for item in items])
  
    centroid = cluster_coords.mean(axis=0)
    avg_datetime = cluster_datetime.mean(axis=0)
  
    str_cluster_id = "ICanGroupThem" if cluster_id < 0 else int(cluster_id)
  
    clusters_with_data[str_cluster_id] = {}
    clusters_with_data[str_cluster_id]["datetime"] = avg_datetime
    clusters_with_data[str_cluster_id]["esp"] = eps_km
  
    # Need to convert np array to tuple for json dump
    clusters_with_data[str_cluster_id]["centroid"] = tuple(centroid)
    clusters_with_data[str_cluster_id]["photos"] = {}
  
    for path in paths:
      # Dedup
      clusters_with_data[str_cluster_id]["photos"][data_images[path].sha256] = path
  return clusters_with_data