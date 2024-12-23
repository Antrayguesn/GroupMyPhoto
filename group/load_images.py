import os
from group.image_data import ImageData

def load_images_from_dir(path, exclude_list: list = []):
  """Load images and extract their EXIF data using ImageData class"""
  data_images = {}
  for root, _, files in os.walk(path):
    for file in files:
      file_path = os.path.join(root, file)
      try:
        image_data = ImageData(file_path)
        if image_data.sha256 in exclude_list:
          continue
      except Exception as e:
        continue

      data_images[file_path] = image_data
  return data_images

def load_images_from_paths_list(paths_list: list):
  data_images = {}
  for path in paths_list:
    try:
      image_data = ImageData(path)
    except Exception as e:
      continue

    data_images[path] = image_data
  return data_images