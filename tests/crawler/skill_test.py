import pytest

from crawler.skill import *


@pytest.fixture(scope="module")
def uma_soup():
    r = requests.get("https://gamewith.jp/uma-musume/article/show/266048")
    if r.status_code != 200:
        raise Exception("Gamewith server seems down")
    yield BeautifulSoup(r.text, 'lxml')


@pytest.fixture(scope="module")
def card_soup():
    r = requests.get("https://gamewith.jp/uma-musume/article/show/257458")
    if r.status_code != 200:
        raise Exception("Gamewith server seems down")
    yield BeautifulSoup(r.text, 'lxml')


def test_get_uma_skill_list(uma_soup):
    expect = [
        {'category': '固有スキル', 'name': '最強の名をかけて'},
        {'category': '初期スキル', 'name': '直線巧者'},
        {'category': '初期スキル', 'name': 'スタミナキープ'},
        {'category': '初期スキル', 'name': '深呼吸'},
        {'category': '覚醒スキル', 'name': '秋ウマ娘◯'},
        {'category': '覚醒スキル', 'name': 'クールダウン'},
        {'category': '覚醒スキル', 'name': 'ペースアップ'},
        {'category': '覚醒スキル', 'name': 'ハヤテ一文字'}
    ]
    actual = get_skill_list(uma_soup)

    assert expect == actual


def test_get_card_skill_list(card_soup):
    expect = [
        {'category': '育成イベント', 'name': '先行直線◯'},
        {'category': '育成イベント', 'name': '一陣の風'},
        {'category': '所持スキル', 'name': 'ポジションセンス'},
        {'category': '所持スキル', 'name': '垂れウマ回避'},
        {'category': '所持スキル', 'name': '臨機応変'},
        {'category': '所持スキル', 'name': 'イナズマステップ'},
        {'category': '所持スキル', 'name': '軽やかステップ'},
        {'category': '所持スキル', 'name': '巧みなステップ'}
    ]
    actual = get_skill_list(card_soup)

    assert  expect == actual
