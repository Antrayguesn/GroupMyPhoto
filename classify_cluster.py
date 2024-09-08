import json
import sys

from jinja2 import Environment, FileSystemLoader, select_autoescape

in_path = sys.argv[1]

env = Environment(
    loader=FileSystemLoader("."),
    autoescape=select_autoescape()
)

template = env.get_template("index.html.jinja")


with open(f"{in_path}/clusters_metadata.json", "r") as database:
  datapoints = json.load(database)





#for cluster, metadata in datapoint.items():
#    print(f"Cluster : {cluster}")
#    if "display_name" in metadata:
#      print(f"{metadata["display_name"]}")
#    contient = input("Contient : ")
#    country = input("Country : ")
#    region = input("Region : ")
#    place = input("Place : ")
#    extra = input("extra: ")


print(template.render(datapoints=datapoints))