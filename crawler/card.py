import shutil
from os import path

import requests
from bs4 import BeautifulSoup

from database import db_session
from models.card import SupportCard, CardEvent, CardEventChoice
from translator import translate
from utils import download_image


def get_support_card(uri: str, soup: BeautifulSoup):
    wiki_id = int(uri.split('/')[-1])

    h3 = soup.find('h3')
    card_name = h3.text.replace('の性能', '')
    illust_uri = h3.find_next_sibling('img')['data-original']
    image_filename = download_image(illust_uri)

    card_table: BeautifulSoup = soup.find_all('table')[1]
    card_field = card_table.find_all('td')
    rare_degree = card_field[0].text
    card_type = card_field[1].text
    second_name = card_field[2].text

    support_card = SupportCard(
        card_name=card_name,
        card_name_kr=card_name,
        card_type=card_type,
        card_type_kr=card_type,
        card_image=image_filename,
        gamewith_wiki_id=wiki_id,
        rare_degree=rare_degree,
        second_name=second_name,
        second_name_kr=second_name
    )
    db_session.add(support_card)
    return support_card


def get_card_event(soup: BeautifulSoup, support_card: SupportCard, update: bool = False):
    choice_tables = soup.find_all('div', {"class": "uma_choice_table"})
    for choice_table in choice_tables:
        title = choice_table.find_previous_sibling('h3').text
        card_event = CardEvent(title=title,
                               title_kr=title,
                               support_card=support_card)
        event_from_db = db_session.query(CardEvent).filter_by(
            support_card_id=card_event.support_card_id,
            title=card_event.title).first()

        if event_from_db and update:
            card_event = event_from_db

        get_card_event_choice(choice_table, card_event, update)
        db_session.add(card_event)


def get_card_event_choice(soup: BeautifulSoup, card_event: CardEvent, update: bool = False):
    tr_tags = soup.find_all('tr')
    for tr in tr_tags:
        title = tr.find('th').text
        effect = tr.find('td').get_text(separator="\n")
        card_event_choice = CardEventChoice(title=title,
                                            title_kr=title,
                                            effect=effect,
                                            effect_kr=effect,
                                            event=card_event)
        event_from_db = db_session.query(CardEventChoice).filter_by(
            title=card_event_choice.title,
            effect=card_event_choice.effect,
            event_id=card_event_choice.event_id).first()
        if not event_from_db:
            db_session.add(card_event_choice)


def crawl_new_card(uri: str, update: bool = False):
    # https://gamewith.jp/uma-musume/article/show/266299
    r = requests.get(uri)
    if r.status_code != 200:
        return False

    soup = BeautifulSoup(r.text, 'lxml')
    card = get_support_card(uri, soup)

    card_from_db = db_session.query(SupportCard).filter_by(
            second_name=card.second_name,
            card_name=card.card_name,
            rare_degree=card.rare_degree).first()

    if card_from_db and update:
        card = card_from_db
    elif card_from_db:
        return False

    get_card_event(soup, card, update)
    db_session.commit()

    translate()

    return True
