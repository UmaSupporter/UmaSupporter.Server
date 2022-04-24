import shutil
import pathlib
import boto3
from os import path, makedirs, remove

import requests


def download_image(url: str, base_path: str = 'static/images') -> str:
    r = requests.get(url, stream=True)
    filename = url.split('/')[-1]
    working_dir = pathlib.Path().resolve()
    save_dir = path.join(working_dir, base_path)
    save_path = path.join(save_dir, filename)
    if r.status_code != 200:
        raise ConnectionError(f"Cannot download image: {save_path}")

    if not path.exists(save_dir):
        makedirs(save_dir, exist_ok=False)

    with open(save_path, 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)

    s3_client = boto3.client('s3')

    response = s3_client.upload_file(save_path, "umasupporterstatic", path.join("images", filename))

    return filename


def get_gamewith_id(uri: str) -> int:
    return int(uri.split('/')[-1])
