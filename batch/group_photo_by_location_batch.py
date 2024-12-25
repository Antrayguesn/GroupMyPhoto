import copy

from utils.clusterization import clusterize
from utils.load_images import load_images_from_dir
from utils.geo_function import distance
from batch.batch import Batch

ESP_KM = 4


class GroupPhotosByLocationBatch(Batch):
    def _update_clusters_with_coord(self, path: str) -> dict:
        exclude_file = [item for image in self.clusters.values() for item in image["photos"]]
        data_images = load_images_from_dir(path, exclude_file)

        if not data_images:
            print(f"Can't found : {path}")
            return self.clusters

        for path, image in copy.deepcopy(data_images).items():
            # We can compute distance if image have not coord data
            for id_cluster, cluster in copy.deepcopy(self.clusters).items():
                if image.coord is None:
                    if "periode" in cluster:
                        for periode in cluster["periode"]:
                            # On calcule si la photo a été prise en meme temps que d'autre photo du cluster
                            image_datetime = image.datetime.timestamp()
                            if image_datetime > periode[0] - 3600 and image_datetime < periode[1] + 3600:
                                print(id_cluster)
                                print(image.path)
                                self.clusters[id_cluster]["photos"][image.sha256] = image.toJSON()
                else:
                    d = distance(image.coord, cluster["centroid"])
                    if d < ESP_KM:
                        self.clusters[id_cluster]["photos"][image.sha256] = image.toJSON()
                        del data_images[path]

        new_clusters = clusterize(data_images, ESP_KM)
        self.clusters.update(new_clusters)

        return self.clusters

    def _create_clusters_from_path(self, path: str) -> dict:
        data_images = load_images_from_dir(path)
        print(data_images)

        if not data_images:
            print(f"Can't found : {path}")
            return

        return clusterize(data_images, ESP_KM)

    def process(self):
        if self.clusters is None:
            self.clusters = self._create_clusters_from_path("photos")
        else:
            self.clusters = self._update_clusters_with_coord("photos")
