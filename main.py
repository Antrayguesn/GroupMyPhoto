import os

from batch.group_photo_by_location_batch import GroupPhotosByLocationBatch
from batch.photo_time_metrics_batch import PhotoTimeMetricsBatch
from batch.find_urban_cluster_batch import FindUrbanClusterBatch
from batch.compute_centroid_batch import ComputeCentroidBatch
from batch.find_place_name_batch import FindPlaceNameBatch

from flask import Flask, jsonify, request, render_template, send_file, send_from_directory
from utils.manage_json_file import read_json_file

app = Flask(__name__)


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


app.run()
