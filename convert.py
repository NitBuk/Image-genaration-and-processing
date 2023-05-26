# convert.py

##############################################################################
#                                   Imports                                  #
##############################################################################
import json
from PIL import Image
import io
from base64 import b64encode, b64decode
from pathlib import Path
from typing import List
import numpy as np


def convert_img_list_2_json(image_data: List[List[List[int]]], json_path: str):
    # Convert the list to a numpy array
    image_array = np.array(image_data, dtype=np.uint8)

    # Create a PIL image from the numpy array
    image = Image.fromarray(image_array)

    # Create a BytesIO object
    byte_io = io.BytesIO()

    # Save the PIL image to the BytesIO object as a PNG
    image.save(byte_io, format='PNG')

    # Get the byte data from the BytesIO object
    byte_data = byte_io.getvalue()

    # Base64 encode the byte data
    b64_string = b64encode(byte_data).decode('utf-8')

    # Define the dictionary to be dumped as JSON
    image_dict = {"data": [{"b64_json": b64_string}]}

    # Open the JSON file in write mode and dump the dictionary
    with open(json_path, "w") as json_file:
        json.dump(image_dict, json_file)

    return json_path


def convert_img_2_json(image_path):
    IMAGE_PATH = Path(image_path)
    JSON_FILE = IMAGE_PATH.with_suffix('.json')

    with open(IMAGE_PATH, "rb") as image_file:
        encoded_string = b64encode(image_file.read()).decode('utf-8')

    image_dict = {"data": encoded_string}

    with open(JSON_FILE, "w") as json_file:
        json.dump(image_dict, json_file)

    return JSON_FILE


def convert_json_2_png(json_name):
    JSON_FILE = json_name
    IMAGE_DIR = Path.cwd() / "images" / JSON_FILE.stem

    IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    with open(JSON_FILE, mode="r", encoding="utf-8") as file:
        response = json.load(file)
    image_files = []
    for index, image_dict in enumerate(response["data"]):
        image_data = b64decode(image_dict["b64_json"])
        image_file = IMAGE_DIR / f"{JSON_FILE.stem}-{index}.png"
        image_files.append(image_file)
        with open(image_file, mode="wb") as png:
            png.write(image_data)
    return image_files

