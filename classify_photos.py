import sys
import json

from group.image_data import ImageData
from group.clusterization import clusterize
from group.load_images import load_images_from_dir

ESP_KM = 4

try:
  path = sys.argv[1]
except:
  print("Usage: python triage input_dir")
  exit()

data_images = load_images_from_dir(path)

if not data_images:
  print(f"Can't found {path}")
  exit()

info_clusters  = clusterize(data_images, ESP_KM)

json.dumps(info_clusters)
