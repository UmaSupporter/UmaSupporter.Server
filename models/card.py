from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy.orm import relationship, backref

from database import Base


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
    skills = relationship(
        "CardSkill",
        back_populates="card")


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
