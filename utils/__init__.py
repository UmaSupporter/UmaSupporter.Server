import shutil
from os import path

import requests


def download_image(url: str, base_path: str = 'static/images') -> str:
    r = requests.get(url, stream=True)
    filename = url.split('/')[-1]
    save_path = path.join(base_path, filename)
    if r.status_code != 200:
        raise ConnectionError(f"Cannot download image: {save_path}")
    with open(save_path, 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)

    return filename


def get_gamewith_id(uri: str) -> int:
    return int(uri.split('/')[-1])
