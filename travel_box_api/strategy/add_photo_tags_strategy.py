
from strategy.strategy import Strategy


class AddPhotoTagsStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.STRATEGY_CODE = "018"
    
    def __search_photo_in_clusters(self, photo_id_):
        for cluster_id, cluster in self.clusters.items():
            for photo_id, photo in cluster["photos"]:
                if photo_id == photo_id_:
                    return cluster_id


    def __add_photo_tag(self, photo_id, data):
        cluster = self.__search_photo_in_clusters(photo_id)
        try:
            self.clusters[cluster_id]["photos"][photo_id]["tags"].update(data)
        except KeyError:
            self.clusters[cluster_id]["photos"][photo_id]["tags"] = data

    def process(self, photo_id, data):
        self.__add_photo_tag(photo_id, data)