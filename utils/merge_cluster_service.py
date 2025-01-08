import copy
import uuid

from utils.manage_json_file import read_json_file, write_json_file


def merge_clusters(id_cluster_1, id_cluster_2):
    """
    merge cluster_2 in cluster_1
    """
    clusters = read_json_file()
    clusters[str(id_cluster_1)]["photos"].update(clusters[str(id_cluster_2)]["photos"])
    del clusters[str(id_cluster_2)]
    write_json_file(clusters)


def move_photo_from_cluster_to_cluster(image, id_cluster_1, id_cluster_2):
    """
      Move the photo from cluster_1 to cluster_2
    """
    clusters = read_json_file()
    clusters[str(id_cluster_2)]["photos"][image] = copy.deepcopy(clusters[str(id_cluster_1)]["photos"][image])
    del clusters[str(id_cluster_1)]["photos"][image]
    write_json_file(clusters)


def create_cluster(cluster_name):
    clusters = read_json_file()
    uuid_cluster = str(uuid.uuid4())
    clusters[uuid_cluster] = {}
    clusters[uuid_cluster]["place"] = cluster_name
    clusters[uuid_cluster]["photos"] = {}
    write_json_file(clusters)
