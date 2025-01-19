import json
import os

from travel_box_api.error.cluster_file_json_error import CantFindClusterJson
from travel_box_api.error.cluster_file_json_error import CantReadClusterJson

PATH_TO_DATA_FILE_VAR = "TB_PATH_TO_DATA_FILE_DIR"
DEFAULT_DATA_FILE = "."


def read_json_file() -> dict:
    path_to_data_file = os.environ.get(PATH_TO_DATA_FILE_VAR, DEFAULT_DATA_FILE)
    try:
        with open(f"{path_to_data_file}/data.json", "r") as clusters_json_file:
            clusters = json.load(clusters_json_file)
    except FileNotFoundError:
        raise CantFindClusterJson()
    except Exception:
        raise CantReadClusterJson()
    return clusters


def write_json_file(clusters: dict):
    path_to_data_file = os.environ.get(PATH_TO_DATA_FILE_VAR, DEFAULT_DATA_FILE)
    with open(f"{path_to_data_file}/data.json", "w") as clusters_json_file:
        json.dump(clusters, clusters_json_file)
