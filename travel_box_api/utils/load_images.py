import os
from travel_box_api.data.image_data import ImageData
from travel_box_api.data.log import log, INFO_LOADING_PHOTO, WARNING_UNEXECPT_ERROR, DEBUG_PHOTO_CURRENTLY_PROCESS


def load_images_from_dir(path, exclude_list: list = []):
    """Load images and extract their EXIF data using ImageData class"""
    log(INFO_LOADING_PHOTO, f"Loading photo data from path : {path}", path=path)
    data_images = {}
    for root, _, files in os.walk(path):
        for file_photo in files:
            file_path = os.path.join(root, file_photo)
            log(DEBUG_PHOTO_CURRENTLY_PROCESS, f"Trying to load {file_path}", photo_path=file_path)
            if not file_photo.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue
            try:
                image_data = ImageData(file_path)
                log(DEBUG_PHOTO_CURRENTLY_PROCESS, f"Photo loaded {image_data.sha256}", hash=image_data.sha256)
                if image_data.sha256 in exclude_list:
                    continue
            except Exception as e:
                # We dont want stop the process for a unexcept error
                # Just log and trace
                log(WARNING_UNEXECPT_ERROR, f"UNEXECPT ERROR : {e}", file_path=file_path)
                continue

            data_images[file_path] = image_data
    return data_images


def load_images_from_paths_list(paths_list: list):
    data_images = {}
    for path in paths_list:
        try:
            image_data = ImageData(path)
        except Exception:
            continue

        data_images[path] = image_data
    return data_images
