from exif import Image
import datetime
import os
import sys
import shutil

from utils.load_images import load_images_from_dir
from utils.geo_function import distance
from batch.batch import Batch

date_image = {}


class GroupPhotosByLocationBatch(Batch):
    def process(self):
        data_image = load_images_from_dir("photos/")
      
        # Tri des images par date
        sorted_date_image = sorted(date_image.items(), key=lambda item: item[1])
      
        # Organisation des images par répertoires basés sur le temps
        old_date = None
        for image_path, image_time in sorted_date_image:
            if old_date is None or (image_time - old_date).total_seconds() > 3600 * 2:
                dir_name = os.path.join("photos", image_time.strftime("%Y-%m-%d_%H:%M:%S"))
                os.makedirs(dir_name, exist_ok=True)
                old_date = image_time
      
            dest_path = os.path.join(dir_name, os.path.basename(image_path))
            try:
                shutil.copy(image_path, dest_path)
            except FileNotFoundError:
                continue
    