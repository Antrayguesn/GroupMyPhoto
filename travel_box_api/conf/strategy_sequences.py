# Request's data are passed by the data arg

SEQUENCES = {
    "GET": {
        "/group_photo_by_location": {
            "STRATEGIES": [
                "GroupPhotosByLocationStrategy",
                "BuildLocationPropStrategy",
                "ImportFromDirStrategy",
                "FindUrbanClusterStrategy",
                "ComputeCentroidStrategy",
                "FindPlaceNameStrategy",
                "SearchClusterCoordStrategy",
                "PhotoTimeMetricsStrategy",
                "ComputeFarestDistanceStrategy",
                "BuildLocationPropStrategy",
                "MergeClusterSameLocationStrategy"
            ]
        },
        "/batch/find_urban_clusters": {
            "STRATEGIES": [
                "FindUrbanClusterStrategy",
                "ComputeCentroidStrategy"
            ]
        },
        "/batch/find_place_name": {
            "STRATEGIES": [
                "FindPlaceStrategy"
            ]
        },
        "/batch/search_cluster_coord_info": {
            "STRATEGIES": [
                "SearchClusterCoordStrategy"
            ]
        },
        "/batch/export_as_gpx": {
            "STRATEGIES": [
                "ExportPhotosGPXStrategy"
            ]
        },
        "/cluster/<uuid:cluster_id>": {
            "STRATEGIES": [
                {"GetClusterStrategy": ["cluster_id"]}
            ]
        },
        "/clusters/": {
            "STRATEGIES": [
                "GetClustersStrategy"
            ]
        },
        "/map_cluster": {
            "STRATEGIES": [
                "GetClusterMapStrategy"
            ]
        },
        "/stat_clusters": {
            "STRATEGIES": [
                "GetClustersStatStrategy"
            ]
        },
    },
    "POST": {
        "/photo/add_tags/<string:photo_id>": {
            "STRATEGIES": [
                {"AddPhotoTagsStrategy": ["photo_id", "data"]},
            ]
        }
    },
    "UPDATE": {
        "/cluster/<string:cluster_id>": {
            "STRATEGIES": [
                {"UpdateClusterStrategy": ["cluster_id", "data"]},
                "BuildLocationPropStrategy",
                "MergeClusterSameLocationStrategy",
                "ComputeCentroidStrategy",
                "ComputeFarestDistanceStrategy",
            ]
        }
    },
    "DELETE": {
        "/cluster/<string:cluster_id>/<string:photo_id>": {
            "STRATEGIES": [
                {"DeletePhotoFromClusterStrategy": ["cluster_id", "photo_id"]},
                "ComputeCentroidStrategy",
                "ComputeFarestDistanceStrategy",
            ]
        }
    }
}