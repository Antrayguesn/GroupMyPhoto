from batch.group_photo_by_location_batch import GroupPhotosByLocationBatch
from batch.photo_time_metrics_batch import PhotoTimeMetricsBatch
from batch.find_urban_cluster_batch import FindUrbanClusterBatch
from batch.compute_centroid_batch import ComputeCentroidBatch
from batch.find_place_name_batch import FindPlaceNameBatch
from batch.compute_farest_distance_batch import ComputeFarestDistance
from batch.build_location_prop_batch import BuildLocationPropBatch
from batch.merge_cluster_same_location import MergeClusterSameLocation

from utils.merge_cluster_service import merge_clusters, move_photo_from_cluster_to_cluster, create_cluster
from utils.get_map_service import get_map, get_cluster_by_location

from flask import Flask, jsonify, render_template, send_from_directory, request
from utils.manage_json_file import read_json_file, write_json_file

import base64

app = Flask(__name__)


@app.route('/cluster/<uuid:id_cluster>')
def get_cluster(id_cluster):
    try:
        return jsonify(read_json_file()[str(id_cluster)])
    except KeyError:
        return jsonify({"error": "Unable to found the cluster with the key"}), 404


@app.route('/cluster/<uuid:id_cluster>', methods=['POST'])
def set_cluster(id_cluster):
    data = request.json
    clusters = read_json_file()
    try:
        clusters[str(id_cluster)].update(data)
    except KeyError:
        return jsonify({"error": "Unable to found the cluster with the key"}), 404
    write_json_file(clusters)
    BuildLocationPropBatch().run()
    MergeClusterSameLocation().run()
    return {}


@app.route('/clusters')
def get_clusters():
    return jsonify(read_json_file())


@app.route('/batch/group_photo_by_location')
def group_photo_by_location():
    GroupPhotosByLocationBatch().run()
    return jsonify(read_json_file())


@app.route('/batch/find_urban_cluster')
def find_urban_cluster():
    FindUrbanClusterBatch().run()
    ComputeCentroidBatch().run()
    return jsonify(read_json_file())


@app.route('/batch/time_metrics')
def get_cluster_time_metrics():
    PhotoTimeMetricsBatch().run()
    return jsonify(read_json_file())


@app.route('/batch/find_plave_name')
def find_place_name():
    FindPlaceNameBatch().run()
    return jsonify(read_json_file())


@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")


@app.route('/photos/<path:filename>')
def serve_photos(filename):
    # Using request args for path will expose you to directory traversal attacks
    return send_from_directory('photos', filename)


@app.route('/merge_clusters/<uuid:id_cluster_1>/<uuid:id_cluster_2>', methods=["POST"])
def merge_clusters_api(id_cluster_1, id_cluster_2):
    merge_clusters(id_cluster_1, id_cluster_2)
    ComputeCentroidBatch().run()
    ComputeFarestDistance().run()
    return {}


@app.route('/move_photo_cluster/<uuid:id_cluster_1>/<uuid:id_cluster_2>/<string:image>', methods=["POST"])
def move_photo(id_cluster_1, id_cluster_2, image):
    move_photo_from_cluster_to_cluster(image, id_cluster_1, id_cluster_2)
    ComputeCentroidBatch().run()
    ComputeFarestDistance().run()
    return {}


@app.route('/cluster/<string:cluster_name>', methods=["POST"])
def create_cluster_api(cluster_name):
    create_cluster(cluster_name)
    return {}


@app.route('/get_cluster_by_location/<location_b64>')
def get_cluster_by_location_api(location_b64):
    location = base64.b64decode(location_b64).decode()
    return get_cluster_by_location(location)


@app.route('/map_cluster')
def get_map_api():
    map = get_map()
    return map


app.run()
