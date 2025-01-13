from exif import Image
from math import cos, asin, sqrt, pi
from sklearn.cluster import DBSCAN
import numpy as np
import datetime
import os
import sys
import shutil

path = sys.argv[1]

data_images = {}


class ImageData:
    path = None
    datetime = None
    coord = None
    cluster = None


def DMStoDD(degres, minutes, secondes, hemisphere):
    # Les données Lat et Lon sont exprimées en DMS (Degres minutes secondes), il faut les convertir en DD (Degres décimal) pour être exploité
    # DD = Degres + minutes / 60 + secondes / 3600
    dd = degres + (minutes / 60) + (secondes / 3600)
    # L'hemisphere définit le signe de la coordonée
    return -dd if hemisphere == "S" or hemisphere == "W" else dd


def distance(coord1, coord2):
    #https://en.wikipedia.org/wiki/Haversine_formula
    r = 6371 # km
    p = pi / 180
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    return 2 * r * asin(sqrt(a))


for root, dirs, files in os.walk(path):
    for file in files:
        file_path = f"{root}/{file}"
        with open(file_path, 'rb') as image_file:
            try:
                my_image = Image(image_file)
            except Exception:
                continue

        if my_image.has_exif:
            new_data = ImageData()
            new_date = datetime.datetime.strptime(my_image.datetime, "%Y:%m:%d %H:%M:%S")
            new_data.path = file_path

            new_data.datetime = new_date

            try:
                lat = DMStoDD(*my_image.gps_latitude, my_image.gps_latitude_ref)
                lon = DMStoDD(*my_image.gps_longitude, my_image.gps_longitude_ref)

                new_data.coord = (lat, lon)
            except AttributeError:
                pass

            data_images[file_path] = new_data

# Array numpy cast
coordinates_list = [i.coord for i in data_images.values() if i.coord]
photo_paths = [i.path for i in data_images.values() if i.coord]

coords = np.array(coordinates_list)

# Clustering by DBSCAN 

db = DBSCAN(eps=0.0015, min_samples=3, metric='haversine').fit(np.radians(coords))

labels = db.labels_

# labelize photo paths
clusters = {}
for label, path, coord in zip(labels, photo_paths, coords):
    if label not in clusters:
        clusters[label] = []
    clusters[label].append(data_images[path])
    data_images[path].cluster = label

clusters_2 = {}

for cluster_id, images_data in clusters.items():
    sorted_date_image = sorted(images_data, key=lambda item: item.datetime)
    old_date = None
    offset_cluster = 0
    for image_data in sorted_date_image:
        image_time = image_data.datetime

        if old_date is None:
            old_date = image_time

        new_date = image_time
        diff_date = new_date - old_date
        delta_sec = diff_date.total_seconds()

        if delta_sec > 3600 * 4:
            offset_cluster += 1

        new_cluster_id = cluster_id * 100 + offset_cluster
        if new_cluster_id not in clusters_2:
            clusters_2[new_cluster_id] = []
        clusters_2[new_cluster_id].append(image_data)

        old_date = new_date

cluster_centroid = {}

for cluster_id, items in clusters_2.items():
    paths = [item.path for item in items]
    cluster_coords = np.array([item.coord for item in items])
    centroid = cluster_coords.mean(axis=0)
    print(f"Cluster {cluster_id} - {centroid}:")
    cluster_centroid[cluster_id] = centroid
    try:
        os.mkdir(f"photos/{cluster_id}")
    except FileExistsError:
        pass
    for path in paths:
        try:
            dest = f"photos/{cluster_id}/{path.split("/")[-1]}"
            shutil.copy(path, dest)
        except FileNotFoundError:
            pass
        print(f"    {path}")