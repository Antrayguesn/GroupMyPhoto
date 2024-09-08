import json
import sys
import requests
import time
import copy

#DUCKDUCK_URL = "https://duckduckgo.com/?q={search}&kl={locale}&format=json&kp=-2&kc=1&kaf=1"
DUCKDUCK_URL = "https://duckduckgo.com/?q={search}&format=json"
PAYS = "New Zealand"
LOCALE = "fr-fr"
LOCALE_NZ = "nz-en"
IMAGE_URL = "https://duckduckgo.com/{image}"

in_path = sys.argv[1]

with open(f"{in_path}/clusters_metadata.json") as metada_file:
  metadatas = json.load(metada_file)

new_metadatas = copy.deepcopy(metadatas)

for cluster, metadata in metadatas.items():
  # Using cache system 
  if "display_name" in metadata:
    continue

  
  location = str(metadata["centroid"]).replace("[", "").replace("]", "").replace(" ", "").replace(",", ";")
  coord = metadata["centroid"]
  print(f"Cluster en cours de traitement {cluster} - Coordonnées {location}")

  try:
    ret = requests.get(f"https://nominatim.openstreetmap.org/reverse?lat={coord[0]}&lon={coord[1]}&format=json", headers={"User-agent": "classify - v0.1"})
    res = ret.json()
    time.sleep(1)
    new_metadatas[cluster]["display_name"] = res["display_name"]

    with open(f"{in_path}/clusters_metadata_temp.json", "w") as clusters_metadata_file:
      json.dump(new_metadatas, clusters_metadata_file)
  # I have realy bad connection ... If the request timeout, we play again the scrpit again
  except:
    continue


with open(f"{in_path}/clusters_metadata.json", "w") as clusters_metadata_file:
  json.dump(new_metadatas, clusters_metadata_file)

