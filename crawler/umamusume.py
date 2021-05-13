from typing import Dict, List

import requests
from bs4 import BeautifulSoup

from database import db_session
from models.uma import Umamusume, UmaEvent, UmaEventChoice
from translator import translate
from utils import get_gamewith_id, download_image


def get_umamusume_event_choice(soup: BeautifulSoup) -> Dict:
    results = {}
    trs: List[BeautifulSoup] = soup.find_all('tr')
    for tr in trs:
        key = tr.find('th').text
        value = tr.find('td').get_text(separator="\n")
        results[key] = value

    return results


def get_umamusume_event(soup: BeautifulSoup) -> List[Dict]:
    results = []
    bs_divs: List[BeautifulSoup] = soup.find_all('div', {"class": "uma_choice_table"})
    for div in bs_divs:
        title = div.find_previous_sibling('h4').text
        event_choice = get_umamusume_event_choice(div)
        results.append({
            'title': title,
            'event_choice': event_choice
        })

        if div.find_next_sibling().name == "h3":
            break
    return results


def get_umamusume_info_table(soup: BeautifulSoup) -> Dict:
    results = {}
    bs_table = soup.find_all('table')[1]
    for row in bs_table.findAll('tr'):
        key = row.find('th').text
        value = row.find('td').text
        results[key] = value

    return results


def get_umamusume_name(soup: BeautifulSoup) -> str:
    h3 = soup.find('h3').text
    return h3.replace('の評価', '')


def get_umamusume_illust_url(soup: BeautifulSoup) -> str:
    # before https://img.gamewith.jp/article_tools/uma-musume/gacha/ikusei_main_30.png
    # after https://img.gamewith.jp/article_tools/uma-musume/gacha/i_30.png
    illust = soup.find('h3').find_next_sibling('img')['data-original']
    index = illust.split('/')[-1].replace('ikusei_main_', '').replace('.png', '')
    return f"https://img.gamewith.jp/article_tools/uma-musume/gacha/i_{index}.png"


def get_rare_degree(value: str) -> int:
    return int(value.replace('星', ''))


def crawl_new_umamusume(uri: str, update: bool = False):
    r = requests.get(uri)
    if r.status_code != 200:
        return False

    soup = BeautifulSoup(r.text, 'lxml')
    gamewith_id = get_gamewith_id(uri)
    illust = get_umamusume_illust_url(soup)
    filename = download_image(illust)

    uma_name = get_umamusume_name(soup)
    umamusume = get_umamusume_info_table(soup)
    umamusume_events = get_umamusume_event(soup)

    umamusume_model = Umamusume(uma_name=uma_name,
                                uma_name_kr=uma_name,
                                second_name=umamusume['二つ名'],
                                second_name_kr=umamusume['二つ名'],
                                uma_image=filename,
                                gamewith_wiki_id=gamewith_id,
                                rare_degree=get_rare_degree(umamusume['初期レア']))

    model_from_db = db_session.query(Umamusume).filter_by(
            second_name=umamusume_model.second_name,
            uma_name=umamusume_model.uma_name,
            rare_degree=umamusume_model.rare_degree).first()

    if model_from_db and update:
        umamusume_model = model_from_db
    elif model_from_db:
        return False

    db_session.add(umamusume_model)
    print('get umamusume')
    for event in umamusume_events:
        umamusume_event_model = UmaEvent(title=event['title'],
                                         title_kr=event['title'],
                                         umamusume=umamusume_model)

        if umamusume_model.uuid:
            model_from_db = db_session.query(UmaEvent).filter_by(
                title=umamusume_event_model.title,
                umamusume=umamusume_event_model.umamusume).first()

        if model_from_db and not update:
            continue

        db_session.add(umamusume_event_model)
        print('get event')

        for key, value in event['event_choice'].items():
            umamusume_event_choices = UmaEventChoice(title=key,
                                                     title_kr=key,
                                                     effect=value,
                                                     effect_kr=value,
                                                     event=umamusume_event_model)
            if umamusume_event_model.uuid:
                model_from_db = db_session.query(UmaEventChoice).filter_by(
                    title=umamusume_event_choices.title,
                    event_id=umamusume_event_choices.event_id,
                ).first()

            if not model_from_db:
                db_session.add(umamusume_event_choices)
            else:
                model_from_db.effect = umamusume_event_choices.effect
                model_from_db.effect_kr = umamusume_event_choices.effect_kr
                db_session.add(model_from_db)

    print(umamusume_model.__dict__)
    db_session.commit()

    translate()

    return True
