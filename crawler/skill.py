from typing import List, Dict

import requests
from bs4 import BeautifulSoup


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
