import re
import json
from typing import List

import requests
from bs4 import BeautifulSoup

from database import db_session
from models import SupportCard, CardEventChoice, CardEvent, Skill, UmaEvent, Umamusume
from models.iterator import iter_card_uri, iter_uma_event
from translator import translate
from utils import download_image


def get_illust_url(article_url: str):
    r = requests.get(article_url)
    if r.status_code != 200:
        raise ConnectionError(f"Cannot load page: {article_url}")

    soup = BeautifulSoup(r.text, 'lxml')
    image_soup = soup.find('img', {'alt': 'イラスト'})
    image_url = image_soup['data-original']
    return image_url


def crawl_all_uma():
    r = requests.get("https://gamewith.jp/uma-musume/article/show/253241")
    soup = BeautifulSoup(r.text, 'lxml')
    uma_list_table = soup.find('div', {"class": "umamusume-ikusei-ichiran"})
    rows: List[BeautifulSoup] = uma_list_table.find_all('tr')
    for row in rows:
        uma_info_a_tag = row.find('a')
        if not uma_info_a_tag:
            continue

        uma_info_uri = uma_info_a_tag['href']
        print(uma_info_uri)

        if uma_info_uri == "https://gamewith.jp/uma-musume/article/show/266048":
            continue

        payload = {
            "root_password": "tngh167",
            "new_card_uri": uma_info_uri
        }
        header = {
            "Content-Type": "application/json"
        }
        p = requests.post("http://localhost:5000/ops/new/uma", headers=header, data=json.dumps(payload))
        if p.text != "ok":
            print(p.text)
            break


def change_card_event_choice(soup: BeautifulSoup):
    choice_tables = soup.find_all('div', {"class": "uma_choice_table"})
    for table in choice_tables:
        tr_tags = table.find_all('tr')
        event_title = table.find_previous_sibling('h3').text
        event = CardEvent.query.filter(CardEvent.title == event_title).first()
        for tr in tr_tags:
            title = tr.find('th').text
            choice: CardEventChoice = \
                CardEventChoice.query.filter(CardEventChoice.title == title) \
                    .filter(CardEventChoice.event == event).first()
            if choice:
                effect = tr.find('td').get_text(separator="\n")
                choice.effect = effect
                choice.effect_kr = effect
                print(choice.uuid)
            else:
                print('something went wrong')

    db_session.commit()


def change_card_event_bulk():
    for uri in iter_card_uri():
        r = requests.get(uri)
        soup = BeautifulSoup(r.text, 'lxml')
        change_card_event_choice(soup)


def search_skill():
    choices: List[CardEventChoice] = CardEventChoice.query.all()
    for choice in choices:
        skill = re.findall("(『.*?』)", choice.effect)


def dump_new_card():
    for uri in iter_card_uri():
        payload = {
            "root_password": "tngh167",
            "new_card_uri": uri
        }
        header = {
            "Content-Type": "application/json"
        }
        p = requests.post("http://localhost:5000/ops/new/card", headers=header, data=json.dumps(payload))
        if p.text != "ok":
            print(p.text)
            break


def download_skill_image():
    for i in range(100):
        uri = f"https://img.gamewith.jp/article_tools/uma-musume/gacha/i_skill{i}.png"
        download_image(uri)


def get_skill_icon(name: str, grade_value: str, type_value: str, float_value: str):
    if int(grade_value) < 0:
        return -1, -1

    grade_data = {
        "340": 2,
        "508": 1,
        "334": 1,
        "394": 1,
        "262": 0,
        "240": 2,
        "217": 0,
        "180": 2,
        "174": 0,
        "129": 0,
        "85": 0,
        "461": 1
    }
    grade = grade_data[grade_value]

    type_data = {
        "지구력": 0,
        "가속도": 1,
        "속도": 2,
        "스태미너": 3,
        "지능": 4,
        "근성": 5,
        "스피드": 6,
        "파워": 7,
        "속도 감소": 8,
        "스타트": 9,
        "도발": 10,
        "포지션": 11,
        "시야 ": 12,
        "시야 방해": 13,
        "스태미너 방해": 14,
        "피지컬": 15,
    }

    type_number = type_data[type_value]
    if type_number == 3 and int(float_value) < 0:
        type_number = 14

    if name == "ラッキーセブン" or name == "スーパーラッキーセブン":
        type_number = 15

    return grade, type_number


def read_skill_csv():
    import csv
    with open('skill.csv', newline='') as csvfile:
        spamreader = csv.DictReader(csvfile)
        for row in spamreader:
            icon = get_skill_icon(row['Name'], row['Grade Value'], row['Type 1'], row['Float Value 1'])
            name = row['Name']
            name_kr = row['NameKr']
            description = row['Description']
            condition = row['Condition']
            if icon[0] > -1 or icon[1] > -1:
                icon_uri = f"i_skill{icon[0]}_{icon[1]}.png"
                skill = Skill(name, name_kr, description, condition, icon_uri)
                db_session.add(skill)
    db_session.commit()


def read_uma_event_csv():
    import csv
    with open('data_table/uma_event.csv', newline='') as csvfile:
        spamreader = csv.DictReader(csvfile)
        for row in spamreader:
            uuid = int(row['uuid'])
            title_kr = row['title_kr']
            event = UmaEvent.query.filter(UmaEvent.uuid == uuid).first()
            event.title_kr = title_kr

    db_session.commit()

def remove_same_data():
    buffer = set([])
    for event in iter_uma_event():
        mapper = (event.title, event.umamusume_id)
        if mapper in buffer:
            print(event.__dict__)
            db_session.delete(event)
        else:
            buffer.add(mapper)
    db_session.commit()

def remove_by_gamewith(wiki_id):
    obj = Umamusume.query.filter(Umamusume.gamewith_wiki_id == wiki_id).first()
    if not obj:
       obj = SupportCard.query.filter(SupportCard.gamewith_wiki_id == wiki_id).first()
    db_session.delete(obj)
    db_session.commit()


def main():
    translate()
    # remove_by_gamewith(272325)
    # remove_same_data()

if __name__ == '__main__':
    main()
