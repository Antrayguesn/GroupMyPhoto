import os
from data.image_data import ImageData
import data.log


def load_images_from_dir(path, exclude_list: list = []):
    """Load images and extract their EXIF data using ImageData class"""
    data.log.log(data.log.INFO_LOADING_PHOTO, f"Loading photo data from path : {path}")
    data_images = {}
    for root, _, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                image_data = ImageData(file_path)
                if image_data.sha256 in exclude_list:
                    #data.log.log(data.log.DEBUG_PHOTO_ALREADY_EXIST, f"Photo {image_data.path} already exist")
                    continue
            except Exception as e:
                # We dont want stop the process for a unexcept error
                # Just log and trace
                data.log.log(data.log.WARNING_UNEXECPT_ERROR, f"UNEXECPT ERROR : {e}", file_path=file_path)
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
