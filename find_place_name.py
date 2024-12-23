#!/bin/python3

"""
Find name places from coord
"""
import json
import sys
import requests
import time
import copy
import re

from group.country_code import COUNTRY_CODE

#DUCKDUCK_URL = "https://duckduckgo.com/?q={search}&kl={locale}&format=json&kp=-2&kc=1&kaf=1"
DUCKDUCK_URL = "https://duckduckgo.com/?q={search}&format=json"
PAYS = "New Zealand"
LOCALE = "fr-fr"
LOCALE_NZ = "nz-en"
IMAGE_URL = "https://duckduckgo.com/{image}"

with sys.stdin as database:
    clusters = json.load(database)

new_metadatas = copy.deepcopy(clusters)

for cluster, metadata in clusters.items():
  # Using cache system 
  if "display_name" in metadata:
    continue
  
  location = str(metadata["centroid"]).replace("[", "").replace("]", "").replace(" ", "").replace(",", ";")
  coord = metadata["centroid"]
  #print(f"Cluster en cours de traitement {cluster} - Coordonnées {location}")

  try:
    ret = requests.get(f"https://nominatim.openstreetmap.org/reverse?lat={coord[0]}&lon={coord[1]}&format=json", headers={"User-agent": "classify - v0.1", "Accept-Language": "fr-FR, en;q=0.8"})
  except KeyboardInterrupt:
    exit()
  # I have realy bad connection ... If the request timeout, we play again the scrpit again
  except:
    continue

    
  # Refaire une recherche avec le type amnety et la route trouvé
  res = ret.json()

  if "error"  in res:
    continue

  region = None
  if "city" in res["address"]:
    region = res["address"]["city"]
  elif "village" in res["address"]:
    region = res["address"]["village"]
  elif "hamlet" in res["address"]:
    region = res["address"]["hamlet"]
  elif "town" in res["address"]:
    region = res["address"]["town"]
  elif "town" in res["address"]:
    region = res["address"]["town"]
  elif "county" in res["address"]:
    region = res["address"]["county"]
  else: 
    region = ""

  country = res["address"]["country"]
  if "name" in res and res["name"]:
    place = res["name"]
  else:
    display_name = res["display_name"]
    if re.match(r"^[0-9]* ", display_name):
      place = display_name.split(",")[0]
    else:
      place = display_name.split(",")[1]


  time.sleep(1)

  try:
      new_metadatas[cluster]["continent"] = COUNTRY_CODE[res["address"]["country_code"]]["continent"]["fr"]
  except KeyError:
    print(res)
  new_metadatas[cluster]["country"] = country.strip()
  new_metadatas[cluster]["region"] = region.strip()
  new_metadatas[cluster]["place"] = place.strip()
  new_metadatas[cluster]["address"] = res["address"]

with open("grouped.json", "w") as file:
    #print(json.dumps(new_metadatas))
    json.dump(new_metadatas, file)