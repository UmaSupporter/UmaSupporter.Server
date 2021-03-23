# coding: utf-8
from database import Base

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.mysql import MEDIUMTEXT


class SupportCard(Base):
    __tablename__ = 'support_card'

    uuid = Column(Integer, primary_key=True)
    card_name = Column(String(100))
    card_type = Column(String(100))
    card_image = Column(String(100))
    gamewith_wiki_id = Column(Integer)
    rare_degree = Column(String(100))
    second_name = Column(String(200))


class CardEvent(Base):
    __tablename__ = 'card_event'

    uuid = Column(Integer, primary_key=True)
    title = Column(String(100))
    support_card_id = Column(ForeignKey('support_card.uuid'), index=True)

    support_card = relationship('SupportCard',
                                backref=backref('card_event',
                                                uselist=True,
                                                cascade='delete,all'))


class CardEventChoice(Base):
    __tablename__ = 'card_event_choice'

    uuid = Column(Integer, primary_key=True)
    title = Column(String(100))
    effect = Column(MEDIUMTEXT)
    event_id = Column(ForeignKey('card_event.uuid'), index=True)

    event = relationship(CardEvent,
                         backref=backref('card_event_choice',
                                         uselist=True,
                                         cascade='delete,all'))
