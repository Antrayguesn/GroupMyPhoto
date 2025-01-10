from utils.manage_json_file import read_json_file


def get_map():
    clusters = read_json_file()
    path_map = {}

    for cluster_id, cluster in clusters.items():
        if "location" in cluster:
            levels = cluster["location"].split("/")
            current_level = path_map

            for level in levels:
                if level not in current_level:
                    current_level[level] = {}
                current_level = current_level[level]

    return path_map


def get_map_location_cluster():
    clusters = read_json_file()

    return {c.location: c_id for c_id, c in clusters.items()}


def get_cluster_by_location(location):
    clusters = read_json_file()

    for c_id, c in clusters.items():
        if location == c["location"]:
            c.update({"cluster_id": c_id})
            return c

    return {}
