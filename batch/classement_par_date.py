from exif import Image
import datetime
import os
import sys
import shutil

path = sys.argv[1]

date_image = {}


def get_exif_datetime(image_path):
    # Fonction pour lire les métadonnées EXIF d'une image
    try:
        with open(image_path, 'rb') as image_file:
            my_image = Image(image_file)
            if my_image.has_exif:
                return datetime.datetime.strptime(my_image.datetime, "%Y:%m:%d %H:%M:%S")
    except Exception:
        pass
    return None


for root, dirs, files in os.walk(path):
    # Parcours des fichiers pour récupérer les dates EXIF
    for file in files:
        file_path = os.path.join(root, file)
        exif_datetime = get_exif_datetime(file_path)
        if exif_datetime:
            date_image[file_path] = exif_datetime

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
