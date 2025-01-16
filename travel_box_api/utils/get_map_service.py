from travel_box_api.utils.manage_json_file import read_json_file


def get_map():
    clusters = read_json_file()
    path_map = {}

    for cluster_id, cluster in clusters.items():
        if "location" in cluster:
            levels = cluster["location"].split("/")
            current_level = path_map

            for index, level in enumerate(levels):
                if level not in current_level:
                    # Initialiser chaque niveau comme un dict avec des enfants
                    current_level[level] = {"children": {}, "is_leaf": False}

                # Si on est au dernier niveau, marquer comme feuille
                if index == len(levels) - 1:
                    current_level[level]["is_leaf"] = True

                # Descendre dans la hiérarchie
                current_level = current_level[level]["children"]

    return path_map


def get_map_location_cluster():
    clusters = read_json_file()

    return {c.location: c_id for c_id, c in clusters.items()}


def get_cluster_by_location(location):
    clusters = read_json_file()

    for c_id, c in clusters.items():
        if location == c["location"]:
            c.update({"cluster_id": c_id})
            for p_id, p in c["photos"].items():
                p.update({"photo_id": p_id})
            return c

    return {}
