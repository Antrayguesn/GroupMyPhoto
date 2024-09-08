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

try:
  path = sys.argv[1]
  out_path = sys.argv[2]
except:
  print("Usage: python triage input_dir output_dir")
  exit()

data_images = {}

# Les données Lat et Lon sont exprimées en DMS (Degres minutes secondes), il faut les convertir en DD (Degres décimal) pour être exploitées
def DMStoDD(degres, minutes, secondes, hemisphere):
  # DD = Degres + minutes / 60 + secondes / 3600
  dd = degres + (minutes / 60) + (secondes / 3600)
  # L'hemisphere définit le signe de la coordonée
  return -dd if hemisphere == "S" or hemisphere == "W" else dd

class ImageData:
  def __init__(self, file_path):
    self.path = file_path
    self.datetime = None
    self.coord = None
    self.cluster = None
    self.load_exif_data()

  def load_exif_data(self):
    """Extract EXIF data from the image."""
    with open(self.path, 'rb') as image_file:
      my_image = Image(image_file)
      if my_image.has_exif:
        self.datetime = datetime.datetime.strptime(my_image.datetime, "%Y:%m:%d %H:%M:%S")
        self.coord = self.extract_gps_data(my_image)

  def extract_gps_data(self, image):
    """Extract GPS coordinates from EXIF data and convert them to decimal degrees."""
    try:
      lat = self.DMStoDD(*image.gps_latitude, image.gps_latitude_ref)
      lon = self.DMStoDD(*image.gps_longitude, image.gps_longitude_ref)
      return lat, lon
    except AttributeError:
      return None

  @staticmethod
  def DMStoDD(degrees, minutes, seconds, hemisphere):
    """Convert DMS (Degrees, Minutes, Seconds) to DD (Decimal Degrees)."""
    dd = degrees + (minutes / 60) + (seconds / 3600)
    return -dd if hemisphere in ['S', 'W'] else dd

def load_images(path):
  """Load images and extract their EXIF data using ImageData class."""
  data_images = {}
  for root, _, files in os.walk(path):
    for file in files:
      file_path = os.path.join(root, file)
      try:
        image_data = ImageData(file_path)
      except:
        continue

      data_images[file_path] = image_data
  return data_images

data_images = load_images(path)

# Pas de 
if not data_images:
  print(f"Can't found {path}")
  exit()

# Array numpy cast 
coordinates_list = [i.coord for i in data_images.values() if i.coord]
photo_paths = [i.path for i in data_images.values() if i.coord]

coords = np.array(coordinates_list)

eps_in_km = 4.0 

# Conversion en radians
eps_in_radians = eps_in_km / 6371

# Clustering by DBSCAN 
db = DBSCAN(eps=eps_in_radians, min_samples=3, metric='haversine').fit(np.radians(coords))

labels = db.labels_

# labelize photo paths
clusters = {}
for label, path, coord in zip(labels, photo_paths, coords):
  if label not in clusters:
    clusters[label] = []
  clusters[label].append(data_images[path])
  data_images[path].cluster = label

cluster_centroid = {}
info_clusters = {}

# Cluster by GPS
for cluster_id, items in clusters.items():
  paths = [item.path for item in items]
  cluster_coords = np.array([item.coord for item in items])
  cluster_datetime = np.array([item.datetime.timestamp() for item in items])

  centroid = cluster_coords.mean(axis=0)
  avg_datetime = cluster_datetime.mean(axis=0)

  cluster_centroid[cluster_id] = centroid
  
  gps_cluster_id = int(cluster_id)


  if cluster_id < 0:
    str_cluster_id = "ICanGroupThem"
  else: 
    str_cluster_id = gps_cluster_id

  try:
    os.makedirs(f"{out_path}/{str_cluster_id}", exist_ok=True)
  except FileExistsError:
    pass


  info_clusters[str_cluster_id] = {}
  info_clusters[str_cluster_id]["datetime"] = avg_datetime
  # Need to convert np array to tuple for json dump
  info_clusters[str_cluster_id]["centroid"] = tuple(centroid)

  for path in paths:
    try:
      dest = f"{out_path}/{gps_cluster_id}/{path.split("/")[-1]}"
      shutil.copy(path, dest)
    except FileNotFoundError:
      pass

with open(f"{out_path}/clusters_metadata.json", "w") as clusters_metadata_file:
  json.dump(info_clusters, clusters_metadata_file)
