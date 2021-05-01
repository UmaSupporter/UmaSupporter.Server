import json
from typing import List

import requests
from bs4 import BeautifulSoup

from models.card import CardEventChoice
from models.uma import UmaEvent, UmaEventChoice


def iter_card_uri():
    r = requests.get("https://gamewith.jp/uma-musume/article/show/255035")
    soup = BeautifulSoup(r.text, 'lxml')
    card_list_table = soup.find('div', {"class": "uma_support_table"})
    rows: List[BeautifulSoup] = card_list_table.find_all('tr')
    for row in rows:
        if not row.find('td'):
            continue

        yield row.find('td').find('a')['href']


def iter_char_name():
    with open('csvjson.json') as json_file:
        json_data = json.load(json_file)
        for data in json_data:
            yield {
                data['jp']: data['kr']
            }


def iter_uma_choice():
    for choice in UmaEventChoice.query.all():
        yield choice


def iter_uma_event():
    for event in UmaEvent.query.all():
        yield event


def iter_card_event_choice():
    for choice in CardEventChoice.query.all():
        yield choice