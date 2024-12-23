from exif import Image
from math import cos, asin, sqrt, pi
import datetime
import sys
import uuid
import json
import hashlib

def DMStoDD(degres, minutes, secondes, hemisphere):
  # DD = Degres + minutes / 60 + secondes / 3600
  dd = degres + (minutes / 60) + (secondes / 3600)
  # L'hemisphere définit le signe de la coordonée
  return -dd if hemisphere == "S" or hemisphere == "W" else dd

#https://en.wikipedia.org/wiki/Haversine_formula
def distance(coord1, coord2):
  r = 6371 # km
  p = pi / 180
  
  lat1, lon1 = coord1
  lat2, lon2 = coord2

  a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
  return 2 * r * asin(sqrt(a))

class ImageData:
  def __init__(self, file_path):
    self.path = file_path
    self.datetime = None
    self.coord = None
    self.cluster = None
    self.sha256 = None
    self.load_exif_data()

  def load_exif_data(self):
    """Extract EXIF data from the image."""
    with open(self.path, 'rb') as image_file:
      my_image = Image(image_file)
      if my_image.has_exif:
        self.datetime = datetime.datetime.strptime(my_image.datetime, "%Y:%m:%d %H:%M:%S")
        self.coord = self.extract_gps_data(my_image)
      
      # On a déjà lu l'image, il faut donc remettre le pointeur à zéro
      image_file.seek(0)

      m = hashlib.sha256()

      for bloc in iter(lambda: image_file.read(4096), b""):
        m.update(bloc)
      self.sha256 = m.hexdigest()
  
  def toJSON(self):
    return {"path": self.path, "datetime": self.datetime.timestamp(), "coord": self.coord}


  def extract_gps_data(self, image):
    """Extract GPS coordinates from EXIF data and convert them to decimal degrees."""
    try:
      lat = self.DMStoDD(*image.gps_latitude, image.gps_latitude_ref)
      lon = self.DMStoDD(*image.gps_longitude, image.gps_longitude_ref)
      return lat, lon
    except AttributeError:
      return None

  # Les données Lat et Lon sont exprimées en DMS (Degres minutes secondes), il faut les convertir en DD (Degres décimal) pour être exploitées
  @staticmethod
  def DMStoDD(degrees, minutes, seconds, hemisphere):
    """Convert DMS (Degrees, Minutes, Seconds) to DD (Decimal Degrees)."""
    dd = degrees + (minutes / 60) + (seconds / 3600)
    return -dd if hemisphere in ['S', 'W'] else dd
