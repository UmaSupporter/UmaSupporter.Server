from typing import List, Dict

import requests
from bs4 import BeautifulSoup

from models import UmaSkillCategoryEnum, CardSkillCategoryEnum


def get_skill_name(soup: BeautifulSoup) -> List[Dict]:
    result = []
    category = soup.find_previous_sibling('h3').text
    if category == "固有ボーナス":
        return result
    trs: List[BeautifulSoup] = soup.find_all('tr')
    for tr in trs:
        result.append({
            'category': category,
            'name': tr.find('td').find('a').text
        })

    return result


def get_skill_list(soup: BeautifulSoup) -> List[Dict]:
    result = []
    bs_divs: List[BeautifulSoup] = soup.find_all('div', {"class": "uma_skill_table"})
    for div in bs_divs:
        skill_list = get_skill_name(div)
        result += skill_list
    return result


def crawl_umamusume_skill(uri: str) -> List[Dict]:
    r = requests.get(uri)
    if r.status_code != 200:
        return False

    soup = BeautifulSoup(r.text, 'lxml')
    return get_skill_list(soup)


def crawl_card_skill(uri: str) -> List[Dict]:
    r = requests.get(uri)
    if r.status_code != 200:
        return False

    soup = BeautifulSoup(r.text, 'lxml')
    return get_skill_list(soup)


def skill_name_polyfill(name: str) -> str:
    if name == 'win Q.E.D':
        return '∴win Q.E.D.'
    if name == 'G00 1stF∞':
        return 'G00 1st.F∞;'
    if name == 'LookatCurren':
        return '#LookatCurren'
    return name


def get_uma_skill_category(category: str) -> UmaSkillCategoryEnum:
    if category == '固有スキル':
        return UmaSkillCategoryEnum.origin
    if category == '初期スキル':
        return UmaSkillCategoryEnum.basic
    if category == '覚醒スキル':
        return UmaSkillCategoryEnum.awakening
    raise ValueError


def get_card_skill_category(category: str) -> CardSkillCategoryEnum:
    if category == '育成イベント':
        return CardSkillCategoryEnum.growth
    if category == '所持スキル':
        return CardSkillCategoryEnum.belong
    raise ValueError