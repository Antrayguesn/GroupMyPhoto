from strategy.group_photo_by_location_strategy import GroupPhotosByLocationStrategy
from strategy.photo_time_metrics_strategy import PhotoTimeMetricsStrategy
from strategy.find_urban_cluster_strategy import FindUrbanClusterStrategy
from strategy.compute_centroid_strategy import ComputeCentroidStrategy
from strategy.find_place_name_strategy import FindPlaceNameStrategy
from strategy.compute_farest_distance_strategy import ComputeFarestDistanceStrategy
from strategy.build_location_prop_strategy import BuildLocationPropStrategy
from strategy.merge_cluster_same_location_strategy import MergeClusterSameLocationStrategy
from strategy.import_from_dir_strategy import ImportFromDirStrategy
from strategy.search_cluster_coord_strategy import SearchClusterCoordStrategy
from strategy.get_clusters_map_strategy import GetClusterMapStrategy
from strategy.update_cluster_strategy import UpdateClusterStrategy
from strategy.export_photo_location_gpx import ExportPhotosGPXStrategy
from strategy.get_clusters_map_strategy import GetClusterMapStrategy
from strategy.delete_photo_from_cluster_strategy import DeletePhotoFromClusterStrategy
from strategy.add_photo_tags_strategy import AddPhotoTagsStrategy
from strategy.get_clusters_stat_strategy  import GetClustersStatStrategy 

from utils.singleton import Singleton
from utils.manage_json_file import read_json_file
from utils.manage_json_file import write_json_file

from error.cluster_file_json_error import CantFindClusterJson


from data.log import INFO_LOADING_DATA, INFO_WRITING_DATA, INFO_END_PROCESS, INFO_RUN_STRATEGIES, log


class StrategyManager(metaclass=Singleton):
    def __init__(self):
        self.SERVICE_CODE = "100"
        self.clusters = None
        self.STRATEGIES = {GroupPhotosByLocationStrategy.__name__: GroupPhotosByLocationStrategy(),
                           PhotoTimeMetricsStrategy.__name__: PhotoTimeMetricsStrategy(),
                           FindPlaceNameStrategy.__name__: FindPlaceNameStrategy(),
                           ComputeCentroidStrategy.__name__: ComputeCentroidStrategy(),
                           FindUrbanClusterStrategy.__name__: FindUrbanClusterStrategy(),
                           ComputeFarestDistanceStrategy.__name__: ComputeCentroidStrategy(),
                           BuildLocationPropStrategy.__name__: BuildLocationPropStrategy(),
                           MergeClusterSameLocationStrategy.__name__: MergeClusterSameLocationStrategy(),
                           ImportFromDirStrategy.__name__: ImportFromDirStrategy(),
                           GetClusterMapStrategy.__name__: GetClusterMapStrategy(),
                           SearchClusterCoordStrategy.__name__: SearchClusterCoordStrategy(),
                           UpdateClusterStrategy.__name__: UpdateClusterStrategy(),
                           ExportPhotosGPXStrategy.__name__: ExportPhotosGPXStrategy(),
                           DeletePhotoFromClusterStrategy.__name__: DeletePhotoFromClusterStrategy(),
                           AddPhotoTagsStrategy.__name__: AddPhotoTagsStrategy(),
                           GetClustersStatStrategy.__name__: GetClustersStatStrategy()
                           }

    def load_data(self):
        """
        Charge les données nécessaires pour le traitement.
        """
        try:
            self.clusters = read_json_file()
        except CantFindClusterJson:
            self.clusters = None

    def process(self):
        """
        Traite les données chargées.

        Raises:
            NotImplementedError: Cette méthode doit être implémentée par les sous-classes.
        """
        raise NotImplementedError("La méthode 'process' doit être implémentée par les sous-classes.")

    def save_results(self):
        """
        Sauvegarde les résultats du traitement.
        """
        write_json_file(self.clusters)

    def run_sequence(self, sequence, **kwargs):
        log(INFO_RUN_STRATEGIES, f"Run strategies {sequence}", self.SERVICE_CODE)

        log(INFO_LOADING_DATA, "Loading data ...", "000")
        self.load_data()

        return_strategy = None
        strategy_running = None

        for strategy in sequence:
            if type(strategy) is dict:
                for strat, args in strategy.items():
                    strategy_running = self.STRATEGIES[strat]
                    try:
                        params = {arg: kwargs[arg] for arg in args}
                        return_strategy = strategy_running.run(clusters=self.clusters, **params)
                    except KeyError as e:
                        log("ERROR_0002", f"Can found arg {e}", "000")
                        raise KeyError

            elif type(strategy) is str:
                strategy_running = self.STRATEGIES[strategy]
                return_strategy = strategy_running.run(self.clusters)
            else:
                log("ERROR_0001", "Paramater not reconized {strategy}", self.SERVICE_CODE)
            self.clusters = strategy_running.clusters

        log(INFO_WRITING_DATA, "Writing data", "000")
        self.save_results()

        log(INFO_END_PROCESS, "End of process", "000")
        return return_strategy
