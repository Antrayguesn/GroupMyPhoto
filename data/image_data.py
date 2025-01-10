from exif import Image
import datetime
import hashlib

from utils.geo_function import DMStoDD


class ImageData:
    def __init__(self, file_path):
        self.path = file_path
        self.datetime = None
        self.coord = None
        self.cluster = None
        self.sha256 = None
        self.exif = False
        self.load_exif_data()

    def load_exif_data(self):
        """Extract EXIF data from the image."""
        with open(self.path, 'rb') as image_file:
            my_image = Image(image_file)
            if my_image.has_exif:
                self.exif = True
                self.datetime = datetime.datetime.strptime(my_image.datetime, "%Y:%m:%d %H:%M:%S")
                self.coord = self.extract_gps_data(my_image)

            # On a déjà lu l'image, il faut donc remettre le pointeur à zéro
            image_file.seek(0)

            m = hashlib.sha256()

            for bloc in iter(lambda: image_file.read(4096), b""):
                m.update(bloc)
            self.sha256 = m.hexdigest()

    def toJSON(self):
        if self.exif:
            return {"path": self.path, "datetime": self.datetime.timestamp(), "coord": self.coord}
        else:
            return {"path": self.path}

    def extract_gps_data(self, image):
        """Extract GPS coordinates from EXIF data and convert them to decimal degrees."""
        try:
            lat = DMStoDD(*image.gps_latitude, image.gps_latitude_ref)
            lon = DMStoDD(*image.gps_longitude, image.gps_longitude_ref)
            return lat, lon
        except AttributeError:
            return None
