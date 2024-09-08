from datetime import datetime
import json
import sys

from xml.dom import minidom
import xml.etree.ElementTree as ET

datapoint = {}

in_path = sys.argv[1]

with open(f"{in_path}/clusters_metadata.json", "r") as database:
  datapoint = json.load(database)

#sorted_metadata = sorted(datapoint, key=lambda x: float(x["datetime"]))
sorted_metadata = sorted(datapoint.items(), key=lambda x: x[1]["datetime"])

def export_as_track() :
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
  trkSeg = ET.SubElement(trk, "trkseg")
   
  for cluster_id, point in sorted_metadata:
    point = datapoint[cluster_id]

    trk_point = ET.SubElement(trkSeg, "trkpt")
    trk_point.set('lon', "{}".format(point["centroid"][1]))
    trk_point.set('lat', "{}".format(point["centroid"][0]))

    trk_time = ET.SubElement(trk_point, "time")
    t = datetime.fromtimestamp(point["datetime"]).isoformat()
    #trk_time.text = str(point["datetime"])
    trk_time.text = str(t)

    trk_name = ET.SubElement(trk_point, "name")
    try:
      trk_name.text = point["display_name"]
    except KeyError:
      trk_name.text = cluster_id


    trk_name = ET.SubElement(trk_point, "desc")
    trk_name.text = cluster_id


  return minidom.parseString(ET.tostring(gpx, encoding='utf-8', method='xml')).toprettyxml(indent="  ")

def export_as_points() :
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
   
  for cluster_id, point in sorted_metadata:
    point = datapoint[cluster_id]

    trk_point = ET.SubElement(trk, "wpt")
    trk_point.set('lon', "{}".format(point["centroid"][1]))
    trk_point.set('lat', "{}".format(point["centroid"][0]))

    trk_time = ET.SubElement(trk_point, "time")
    t = datetime.fromtimestamp(point["datetime"]).isoformat()
    trk_time.text = str(t)

    trk_name = ET.SubElement(trk_point, "name")
    try:
      trk_name.text = point["display_name"]
    except KeyError:
      trk_name.text = cluster_id


    trk_name = ET.SubElement(trk_point, "desc")
    trk_name.text = cluster_id


  return minidom.parseString(ET.tostring(gpx, encoding='utf-8', method='xml')).toprettyxml(indent="  ")


print(export_as_points())
