from utils.manage_json_file import read_json_file
from utils.manage_json_file import write_json_file

from error.cluster_file_json_error import CantFindClusterJson


class Batch:
    """
    Classe mère représentant une stratégie de traitement par lots.
    """

    def __init__(self):
        """
        Initialise un objet Batch avec les répertoires d'entrée et de sortie.
        """
        self.clusters = None

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

    def run(self):
        """
        Exécute la stratégie complète de traitement par lots.
        """
        print("Chargement des données...")
        self.load_data()
        print("Traitement des données...")
        self.process()
        print("Enregistrement des résultats...")
        self.save_results()
        print("Traitement terminé.")
