from database import db_session
from models.iterator import iter_card_event_choice, iter_uma_choice


def change_field(original: str):
    value = original
    value = value.replace('体力', '체력')
    value = value.replace('スピード', '스피드')
    value = value.replace('スタミナ', '스태미나')
    value = value.replace('賢さ', '지능')
    value = value.replace('根性', '근성')
    value = value.replace('パワー', '파워', )
    value = value.replace('スキルPt', '스킬포인트')
    value = value.replace('の絆ゲージ', '의 인연 게이지')
    value = value.replace('連続イベント終了', '연쇄 이벤트 종료')
    value = value.replace('のヒント', '의 힌트')
    value = value.replace('ヒント', '의 힌트')
    value = value.replace('ランダムで', '랜덤으로 ')
    value = value.replace('やる気アップ', '의욕 상승')
    value = value.replace('やる気ダウン', '의욕 하락')
    value = value.replace('やる気DOWN', '의욕 하락')
    value = value.replace('になる', '가 된다')
    value = value.replace('Lvアップ', '레벨 업')
    value = value.replace('以下から', '이하는 ')
    value = value.replace('獲得', '획득')
    value = value.replace('最大値', '최대치')
    value = value.replace('もしくは', '혹은 ')
    value = value.replace('※次回イベントが発生しない', '※다음 이벤트가 발생하지 않는다')
    value = value.replace('※失敗時に', '실패 시 ')
    value = value.replace('減少', ' 감소')
    value = value.replace('※成功で次回イベントが発生', '※성공 시 다음 이벤트 발생')
    value = value.replace('※連続イベントが終了し、', '※연속 이벤트가 끝나고, ')
    value = value.replace('ヒントを1つ取得', '힌트 1개 획득')
    value = value.replace('が不可', '이 불가')
    value = value.replace('とお出かけ可能に', '와 외출이 가능해진다')
    value = value.replace('状態異常が治る', '상태 이상 회복')
    value = value.replace('種ステータスを', ' 종류의 스테이터스가')
    value = value.replace('の場合がある', ' 의 경우가 있다')
    value = value.replace('桐生院トレーナー', '키류인 아오이')
    value = value.replace('直前のトレーニングに応じたステータス', '직전에 트레이닝했던 스테이터스')
    value = value.replace('種ステータスからランダムに1種を', '종류의 스테이터스 중에 랜덤으로 1개를 ')
    value = value.replace('ランダム能力', '랜덤한 스탯 ')
    value = value.replace('ファン', '팬')
    value = value.replace('(ランダム)', '(랜덤)')

    return value


def translator(original: str):
    # for char in iter_char_name():
    #     jp = list(char.keys())[0]
    #     kr = char[jp]
    #     original = original.replace(jp, kr)
    return change_field(original)


def translate():
    for choice in iter_card_event_choice():
        value = translator(choice.effect)
        choice.effect_kr = value

    for choice in iter_uma_choice():
        value = translator(choice.effect)
        choice.effect_kr = value

    db_session.commit()