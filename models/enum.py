import enum


class SkillGradeEnum(enum.Enum):
    normal = "노말"
    rare = "레어"
    original = "고유"


class SkillBuffTypeEnum(enum.Enum):
    endurance = "지구력"
    acceleration = "가속도"
    velocity = "속도"
    stamina = "스태미너"
    intelligence = "지능"
    guts = "근성"
    speed = "스피드"
    power = "파워"
    debuf_speed = "속도 감소"
    start = "스타트"
    provocation = "도발"
    position = "포지션"
    eyesight = "시야"
    debuf_eyesight = "시야 방해"
    debuf_stamina = "스태미너 방해"
    physical = "피지컬"


class SkillDistanceTypeEnum(enum.Enum):
    short = "단거리"
    mile = "마일"
    medium = "중거리"
    long = "장거리"
    dirt = "더트"


class SkillOperationTypeEnum(enum.Enum):
    getaway = "도주"
    preceding = "선행"
    pre_entry = "선입"
    post_entry = "후입"


class CardSkillCategoryEnum(enum.Enum):
    growth = '육성'
    belong = '소지'


class UmaSkillCategoryEnum(enum.Enum):
    origin = '고유'
    basic = '기본'
    awakening = '각성'
