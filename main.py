import shutil
from os import path

import requests
from bs4 import BeautifulSoup

from database import db_session
from models import SupportCard


def download_image(url: str, filename: str):
    r = requests.get(url, stream=True)
    save_path = path.join('..', 'static', filename)
    if r.status_code != 200:
        raise ConnectionError(f"Cannot download image: {save_path}")
    with open(save_path, 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)


def get_illust_url(article_url: str):
    r = requests.get(article_url)
    if r.status_code != 200:
        raise ConnectionError(f"Cannot load page: {article_url}")

    soup = BeautifulSoup(r.text, 'lxml')
    image_soup = soup.find('img', {'alt': 'イラスト'})
    image_url = image_soup['data-original']
    return image_url


def main():
    base_url = "https://img.gamewith.jp/img/"

    for instance in db_session.query(SupportCard).order_by(SupportCard.uuid):
        print(instance.card_name)
        url = base_url + instance.card_image
        download_image(url, instance.card_image)


if __name__ == '__main__':
    main()
