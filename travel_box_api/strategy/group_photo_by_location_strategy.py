import copy

from utils.clusterization import clusterize
from utils.load_images import load_images_from_dir
from utils.geo_function import distance
from strategy.strategy import Strategy

from data.log import DEBUG_PHOTO_ALREADY_DELETED, ERROR_NO_PHOTO_PATH, DEBUG_ADD_PHOTO_IN_CLUSTER, WARNING_NO_CENTROID

ESP_KM = 4


class GroupPhotosByLocationStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.STRATEGY_CODE = "006"

    def _update_clusters_with_coord(self, path: str) -> dict:
        exclude_file = [item for image in self.clusters.values() for item in image["photos"]]
        data_images = load_images_from_dir(path, exclude_file)

        if not data_images:
            self.log(ERROR_NO_PHOTO_PATH, f"Can't found {path}", path=path)
            return self.clusters

        for path, image in copy.deepcopy(data_images).items():
            # We can compute distance if image have not coord data
            for id_cluster, cluster in copy.deepcopy(self.clusters).items():
                if image.coord is None:
                    pass
                    # if "periode" in cluster:
                    #     for periode in cluster["periode"]:
                    #         # On calcule si la photo a été prise en meme temps que d'autre photo du cluster
                    #         image_datetime = image.datetime.timestamp()
                    #         if image_datetime > periode[0] - 3600 and image_datetime < periode[1] + 3600:
                    #             self.clusters[id_cluster]["photos"][image.sha256] = image.toJSON()
                elif "centroid" in cluster and cluster["centroid"] is not None:
                    d = distance(image.coord, cluster["centroid"])
                    if d < ESP_KM:
                        self.log(DEBUG_ADD_PHOTO_IN_CLUSTER, f"Add photo {image.path} to {id_cluster}", cluster_id=id_cluster, photo_path=image.path)
                        self.clusters[id_cluster]["photos"][image.sha256] = image.toJSON()
                        try:
                            del data_images[path]
                        except KeyError:
                            self.log(DEBUG_PHOTO_ALREADY_DELETED, f"The photo {path} as already been deleted from the photo list")
                            pass
                else:
                    self.log(WARNING_NO_CENTROID, f"Can't find the centroid for cluster {id_cluster}", id_cluster=id_cluster, location=cluster.get("location", ""))

        new_clusters = clusterize(data_images, ESP_KM)
        self.clusters.update(new_clusters)

        return self.clusters

    def _create_clusters_from_path(self, path: str) -> dict:
        data_images = load_images_from_dir(path)

        if not data_images:
            print(f"Can't found : {path}")
            return

        return clusterize(data_images, ESP_KM)

    def process(self):
        if self.clusters is None:
            self.clusters = self._create_clusters_from_path("photos")
        else:
            self.clusters = self._update_clusters_with_coord("photos")
