from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.dialects.mysql import MEDIUMTEXT

from database import Base


class Buff(Base):
    __tablename__ = 'buff'

    uuid = Column(Integer, primary_key=True)
    name = Column(String(100))
    name_kr = Column(String(100))
    effect_kr = Column(MEDIUMTEXT)
    is_debuff = Column(Boolean())

    def __init__(self, name: str, name_kr: str, effect_kr: str, is_debuff: bool):
        self.name = name
        self.name_kr = name_kr
        self.effect_kr = effect_kr
        self.is_debuff = is_debuff
