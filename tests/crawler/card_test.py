import os

import pytest

from crawler.card import *


@pytest.fixture(scope="module")
def soup():
    r = requests.get("https://gamewith.jp/uma-musume/article/show/257456")
    if r.status_code != 200:
        raise Exception("Gamewith server seems down")
    yield BeautifulSoup(r.text, 'lxml')


def test_get_support_card(soup):
    data: SupportCard = get_support_card("https://gamewith.jp/uma-musume/article/show/257456", soup)
    expect = SupportCard(
        card_name="ウオッカ(SSR)",
        card_name_kr="ウオッカ(SSR)",
        card_type="パワー",
        card_type_kr="パワー",
        card_image="bdea10472621cb94e18cb24fc7db47e5.jpg",
        gamewith_wiki_id="257456",
        rare_degree="SSR",
        second_name="ロード・オブ・ウオッカ",
        second_name_kr="ロード・オブ・ウオッカ"
    )
    
    assert data.card_name == expect.card_name
    assert data.card_type == expect.card_type
    assert data.card_image == expect.card_image
    assert data.rare_degree == expect.rare_degree
    assert data.second_name == expect.second_name

def test_get_card_event(soup):
    data: SupportCard = get_support_card("https://gamewith.jp/uma-musume/article/show/257456", soup)
    get_card_event(soup, data)