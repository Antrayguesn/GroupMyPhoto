import json

from travel_box_api.error.cluster_file_json_error import CantFindClusterJson
from travel_box_api.error.cluster_file_json_error import CantReadClusterJson


def read_json_file() -> dict:
    try:
        with open("data.json", "r") as clusters_json_file:
            clusters = json.load(clusters_json_file)
    except FileNotFoundError:
        raise CantFindClusterJson()
    except Exception:
        raise CantReadClusterJson()
    return clusters


def write_json_file(clusters: dict):
    with open("data.json", "w") as clusters_json_file:
        json.dump(clusters, clusters_json_file)
