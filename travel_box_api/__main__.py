
from flask import Flask, jsonify, send_from_directory, request

import numpy as np

from travel_box_api.conf.strategy_sequences import SEQUENCES
from travel_box_api.strategy.strategy_manager import StrategyManager
from travel_box_api.utils.get_map_service import get_cluster_by_location

import base64

app = Flask(__name__)

strategy_manager = StrategyManager()

# Dynamic 
for method, routes in SEQUENCES.items():
    for route, config in routes.items():
        strategies = config.get("STRATEGIES", [])

        def endpoint_function(route=route, strategies=strategies):
            def handler(**kwargs):
                args = np.array([list(s.values()) for s in strategies if type(s) is dict]).flatten().tolist()
                if "data" in args:
                    response = strategy_manager.run_sequence(strategies, data=request.json, **kwargs)
                else:
                    response = strategy_manager.run_sequence(strategies, **kwargs)
                return jsonify(response)
            return handler
        endpoint_name = f"{method}_{route.replace('/', '_')}".strip('_')
        app.route(route, methods=[method], endpoint=endpoint_name)(endpoint_function())


@app.route('/photos/<path:filename>')
def serve_photos(filename):
    # Using request args for path will expose you to directory traversal attacks
    return send_from_directory('../photos', filename)


@app.route('/sorted/<path:filename>')
def serve_sorted(filename):
    # Using request args for path will expose you to directory traversal attacks
    return send_from_directory('../sorted', filename)


@app.route('/get_cluster_by_location/<location_b64>')
def get_cluster_by_location_api(location_b64):
    location = base64.b64decode(location_b64).decode()
    return get_cluster_by_location(location)


if __name__ == "__main__":
    app.run()
