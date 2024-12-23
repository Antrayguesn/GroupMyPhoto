import sys
import json
import copy

from group.clusterization import clusterize
from group.load_images import load_images_from_dir
from group.image_data import distance

ESP_KM = 4

path = None

try:
    path = sys.argv[1]
except KeyError:
    print("Usage: python classify_photo input_dir [cluster_metadata]")


clusters = None
try:
    with open(sys.argv[2]) as clusters_path:
        clusters = json.load(clusters_path)
except:
    clusters = None


def update_clusters_with_coord(path: str, cluster_metadata: dict) -> dict:
    exclude_file = [item for image in cluster_metadata.values() for item in image["photos"]]
    data_images = load_images_from_dir(path, exclude_file)

    if not data_images:
        print(f"Can't found : {path}")
        return
    for path, image in copy.deepcopy(data_images).items():
        # We can compute distance if image have not coord data
        if image.coord is None:
            continue
        for id_cluster, cluster in copy.deepcopy(cluster_metadata).items():
            d = distance(image.coord, cluster["centroid"])
            if d < ESP_KM:
                cluster_metadata[id_cluster]["photos"][image.sha256] = image.toJSON()
                del data_images[path]

    new_clusters = clusterize(data_images, ESP_KM)
    cluster_metadata.update(new_clusters)

    return cluster_metadata

def create_clusters_from_path(path: str) -> dict:
    data_images = load_images_from_dir(path)

    if not data_images:
        print(f"Can't found : {path}")
        return

    return clusterize(data_images, ESP_KM)

if clusters is None:
    clusters_metadata = create_clusters_from_path(path)
else:
    clusters_metadata = update_clusters_with_coord(path, clusters)

print(json.dumps(clusters_metadata))
