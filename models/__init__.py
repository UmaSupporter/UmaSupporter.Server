# coding: utf-8
from database import Base, engine

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.mysql import MEDIUMTEXT


class SupportCard(Base):
    __tablename__ = 'support_card'

    uuid = Column(Integer, primary_key=True)
    card_name = Column(String(100))
    card_name_kr = Column(String(100))
    card_type = Column(String(100))
    card_type_kr = Column(String(100))
    card_image = Column(String(100))
    gamewith_wiki_id = Column(Integer)
    rare_degree = Column(String(100))
    second_name = Column(String(200))
    second_name_kr = Column(String(200))


class CardEvent(Base):
    __tablename__ = 'card_event'

    uuid = Column(Integer, primary_key=True)
    title = Column(String(100))
    title_kr = Column(String(100))
    support_card_id = Column(ForeignKey('support_card.uuid'), index=True)

    support_card = relationship('SupportCard',
                                backref=backref('card_event',
                                                uselist=True,
                                                cascade='delete,all'))


class CardEventChoice(Base):
    __tablename__ = 'card_event_choice'

    uuid = Column(Integer, primary_key=True)
    title = Column(String(100))
    title_kr = Column(String(100))
    effect = Column(MEDIUMTEXT)
    effect_kr = Column(MEDIUMTEXT)
    event_id = Column(ForeignKey('card_event.uuid'), index=True)

    event = relationship(CardEvent,
                         backref=backref('card_event_choice',
                                         uselist=True,
                                         cascade='delete,all'))


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


Base.metadata.create_all(engine)
