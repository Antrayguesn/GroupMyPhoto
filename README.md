# TravelBox API

The TravelBox API classifies your photos based on their GPS coordinates extracted from Exif data.

TravelBox can Automatically organize all your photos based on their geographical location

And also do the reverse: start from an already organized folder and retrieve the GPS coordinates of each photo or group.

Display everything in a simple and user-friendly interface: either as an interactive map or as a list. (TravelBoxUI)


## Configuration

* `TB_IMPORTED_DIR_PATH`: Path to already sorted photos (default: "sorted/")
* `TB_UNSORTED_PHOTOS_PATH`: Path to the unsorted photos. (default "photos/")
* `TB_PATH_TO_DATA_FILE_DIR`: Path to the data file (where all information of this API are stored)

## Build
### Python

The project is built using `setuptools` (setup.py and pyproject.toml).

To build the Python package, run:

```bash
python3 -m build sdist
```

The package will be generated in the dist directory.

### Docker

After building the Python package, you can create the Docker image.

The application runs in the container using gunicorn.

To build the Docker image:

```bash
docker build -t travel_box_api .
```

To run the container:

```bash
docker run -ti -e TB_IMPORTED_DIR_PATH="/sorted" \
-e TB_UNSORTED_PHOTOS_PATH="/photos" \
-e TB_PATH_TO_DATA_FILE_DIR=/ \
-v Images/Android_Camera/Camera:/photos:ro \
-v Images/Photos/Voyage:/sorted:ro \
-v $(pwd)/data.json:/data.json \
--network host \
travel_box_api:latest
```

The container is exposed on port `5000`.

You can test the cluster mapping endpoint with:

```bash
curl http://localhost:5000/map_cluster
```

## Dynamic Routing

The dynamic router reads from the file `conf/strategy_sequence.py`. Each key in the `SEQUENCES` dictionary defines a route (URL).

Each element in the `SEQUENCES` array is parsed and executed in order when the route is called. These elements can be:

* A string representing the class to execute.
* A dictionary to pass arguments to strategies. The dictionary key specifies the strategy name, and the value is an array of argument names.

Request data should be provided in JSON format.

### Example 1: Multiple strategies on a route

This example demonstrates how to execute the `FindUrbanClusterStrategy` followed by the `ComputeCentroidStrategy` on the `/batch/find_urban_clusters` route:

```json
{
  "/batch/find_urban_clusters": {
      "STRATEGIES": [
          "FindUrbanClusterStrategy",
          "ComputeCentroidStrategy"
      ]
  }
}
```

### Example 2: Strategy with arguments

This example demonstrates how to execute the `GetClusterStrategy`, which requires a `cluster_id` argument, accessible through the `/cluster/<cluster_id>` route:

```python
{
  "/cluster/<uuid:cluster_id>": {
      "STRATEGIES": [
          {"GetClusterStrategy": ["cluster_id"]}
      ]
  }
}
```
``

## Reverse proxy

A exemple of `nginx.conf` to run the api under a reverse proxy can be found at the root of this projet.

```bash
docker run --network host --name my-custom-nginx-container -v $(pwd)/nginx.conf:/etc/nginx/nginx.conf:ro -d nginx
```
