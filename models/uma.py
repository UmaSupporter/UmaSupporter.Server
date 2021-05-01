from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy.orm import relationship, backref

from database import Base
from models.relationship import UmaSkill


class Umamusume(Base):
    __tablename__ = 'umamusume'

    uuid = Column(Integer, primary_key=True)
    uma_name = Column(String(100))
    uma_name_kr = Column(String(100))
    second_name = Column(String(200))
    second_name_kr = Column(String(200))
    uma_image = Column(String(100))
    gamewith_wiki_id = Column(Integer)
    rare_degree = Column(Integer)
    skills = relationship(
        "UmaSkill",
        back_populates="uma")

    def __init__(self,
                 uma_name: str,
                 uma_name_kr: str,
                 second_name: str,
                 second_name_kr: str,
                 uma_image: str,
                 gamewith_wiki_id: int,
                 rare_degree: int):
        self.uma_name = uma_name
        self.uma_name_kr = uma_name_kr
        self.second_name = second_name
        self.second_name_kr = second_name_kr
        self.uma_image = uma_image
        self.gamewith_wiki_id = gamewith_wiki_id
        self.rare_degree = rare_degree


class UmaEvent(Base):
    __tablename__ = 'uma_event'

    uuid = Column(Integer, primary_key=True)
    title = Column(String(100))
    title_kr = Column(String(100))
    umamusume_id = Column(ForeignKey('umamusume.uuid'), index=True)

    umamusume = relationship('Umamusume',
                                backref=backref('uma_event',
                                                uselist=True,
                                                cascade='delete,all'))

    def __init__(self, title: str, title_kr: str, umamusume: Umamusume):
        self.title = title
        self.title_kr = title_kr
        self.umamusume = umamusume
        self.umamusume_id = umamusume.uuid


class UmaEventChoice(Base):
    __tablename__ = 'uma_event_choice'

    uuid = Column(Integer, primary_key=True)
    title = Column(String(100))
    title_kr = Column(String(100))
    effect = Column(MEDIUMTEXT)
    effect_kr = Column(MEDIUMTEXT)
    event_id = Column(ForeignKey('uma_event.uuid'), index=True)

    event = relationship(UmaEvent,
                         backref=backref('uma_event_choice',
                                         uselist=True,
                                         cascade='delete,all'))

    def __init__(self, title: str, title_kr: str, effect: str, effect_kr: str, event: UmaEvent):
        self.title = title
        self.title_kr = title_kr
        self.effect = effect
        self.effect_kr = effect_kr
        self.event = event
        self.event_id = event.uuid
