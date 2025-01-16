from datetime import datetime
import base64

import xml.etree.ElementTree as ET

from travel_box_api.strategy.strategy import Strategy

from travel_box_api.data.log import DEBUG_NO_KEY_COORD


class ExportPhotosGPXStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.STRATEGY_CODE = "015"

    def __export_as_points(self):
        # Création de l'élément
        gpx = ET.Element("gpx")
        gpx.set("version", "1.1")
        gpx.set("creator", "Aigyre Consult")
        gpx.set("xsi:schemaLocation", "http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd")
        gpx.set("xmlns", "http://www.topografix.com/GPX/1/1")
        gpx.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        trk = ET.SubElement(gpx, "trk")
        trkName = ET.SubElement(trk, "name")
        trkName.text = "LazyGrouping"

        for cluster_id, cluster in self.clusters.items():
            trk_cluster = None
            try:
                trk_cluster = ET.SubElement(trk, "wpt")
                trk_cluster.set('lon', "{}".format(cluster["centroid"][1]))
                trk_cluster.set('lat', "{}".format(cluster["centroid"][0]))
            except KeyError as e:
                self.log(DEBUG_NO_KEY_COORD, f"Can't find key {e} for cluster {cluster_id}", cluster_id=cluster_id)
                continue

            trk_time = ET.SubElement(trk_cluster, "time")
            try:
                t = datetime.fromtimestamp(cluster["datetime"]).isoformat()
                trk_time.text = str(t)
            except KeyError as e:
                self.log(DEBUG_NO_KEY_COORD, f"Can't find key {e}", cluster_id=cluster_id)
                pass

            trk_name = ET.SubElement(trk_cluster, "name")
            try:
                trk_name.text = cluster["location"]
            except KeyError:
                trk_name.text = cluster_id

            trk_name = ET.SubElement(trk_cluster, "desc")
            trk_name.text = cluster_id

        return ET.tostring(gpx)

    def process(self, **kwargs):
        gpx = self.__export_as_points()
        gpx_b64 = base64.b64encode(gpx).decode()
        return {"file": gpx_b64}
