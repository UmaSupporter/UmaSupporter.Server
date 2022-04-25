import os

import pytest

from crawler.umamusume import *


@pytest.fixture(scope="module")
def soup1():
    r = requests.get("https://gamewith.jp/uma-musume/article/show/266048")
    if r.status_code != 200:
        raise Exception("Gamewith server seems down")
    yield BeautifulSoup(r.text, "lxml")


@pytest.fixture(scope="module")
def soup2():
    r = requests.get("https://gamewith.jp/uma-musume/article/show/292755")
    if r.status_code != 200:
        raise Exception("Gamewith server seems down")
    yield BeautifulSoup(r.text, "lxml")


@pytest.fixture(scope="module")
def soup3():
    r = requests.get("https://gamewith.jp/uma-musume/article/show/257397")
    if r.status_code != 200:
        raise Exception("Gamewith server seems down")
    yield BeautifulSoup(r.text, "lxml")


@pytest.fixture(scope="module")
def soup4():
    r = requests.get("https://gamewith.jp/uma-musume/article/show/257412")
    if r.status_code != 200:
        raise Exception("Gamewith server seems down")
    yield BeautifulSoup(r.text, "lxml")


def test_umamusume_info_table(soup1):
    data = get_umamusume_info_table(soup1)
    expect = {
        "初期レア": "星3",
        "名称": "エンド・オブ・スカイ",
        "入手方法": "ウマ娘ガチャから入手",
        "固有二つ名": "名優",
        "おすすめ距離": "長距離、中距離",
        "おすすめ脚質": "逃げ、先行",
    }
    assert data == expect


def test_umamusume_name(soup1):
    actual = get_umamusume_name(soup1)
    expect = "メジロマックイーン(新衣装)"
    assert actual == expect


# 通常イベント(選択肢あり)
# 勝負服イベント
# お出かけイベント
# レース後イベント


def test_umamusume_event1(soup1):
    # https://gamewith.jp/uma-musume/article/show/266048
    #
    actual = get_umamusume_event(soup1)
    expect = {"title": "孤島の女王", "event_choice": {"食料": "スピード+10", "体力": "スタミナ+10"}}
    assert actual[0] == expect
    assert len(actual) == 12 + 3 + 5 + 10


def test_umamusume_event2(soup2):
    # https://gamewith.jp/uma-musume/article/show/292755
    actual = get_umamusume_event(soup2)
    expect = {
        "title": "呪いのカメラ",
        "event_choice": {"現代のカメラは大丈夫": "賢さ+10", "魂を取り返せばいい": "スキルPt+30"},
    }
    assert actual[0] == expect
    assert len(actual) == 12 + 3 + 5 + 15


def test_umamusume_event3(soup3):
    # https://gamewith.jp/uma-musume/article/show/257397
    actual = get_umamusume_event(soup3)
    expect = {
        "title": "マヤちんのレース講座☆",
        "event_choice": {
            "バテないようにスタミナをつけよう！": "スタミナ+10\nスキルPt+15",
            "ライバルを追い抜かすコツを掴もう！": "『直線巧者』のヒントLv+1",
        },
    }
    assert actual[0] == expect
    assert len(actual) == 12 + 3 + 5 + 12


def test_umamusume_event4(soup4):
    # https://gamewith.jp/uma-musume/article/show/257412
    actual = get_umamusume_event(soup4)
    expect = {
        "title": "昼下がりの恩返し",
        "event_choice": {"食べることを楽しもう！": "体力+5\n賢さ+5", "何も言う事はない！": "『ペースキープ』のヒントLv+1"},
    }
    assert actual[0] == expect
    assert len(actual) == 12 + 3 + 5 + 10


def test_umamusume_event_choice():
    fixture = (
        '<div class="uma_choice_table">'
        "<table><tr><th>やった、やったぞーっ！！</th>"
        "<td>体力-15<br/>5種ステータスからランダムに1種を+5<br/>スキルPt+30</td></tr>"
        "<tr><th>更なる高みを目指そう！</th>"
        "<td>体力-5~20<br/>5種ステータスからランダムに1種を+5~10<br/>スキルPt+30~45</td></tr>"
        "</table></div>"
    )

    soup1 = BeautifulSoup(fixture, "lxml")
    actual = get_umamusume_event_choice(soup1)
    expect = {
        "やった、やったぞーっ！！": "体力-15\n5種ステータスからランダムに1種を+5\nスキルPt+30",
        "更なる高みを目指そう！": "体力-5~20\n5種ステータスからランダムに1種を+5~10\nスキルPt+30~45",
    }

    assert actual == expect


def test_umamusume_illust_url(soup1):
    actual = get_umamusume_illust_url(soup1)
    expect = "https://img.gamewith.jp/article_tools/uma-musume/gacha/i_30.png"

    assert actual == expect


def test_integration():
    crawl_new_umamusume("https://gamewith.jp/uma-musume/article/show/266048")
