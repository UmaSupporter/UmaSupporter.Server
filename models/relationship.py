from sqlalchemy import Table, Column, Integer, ForeignKey

from database import Base

card_skill_table = Table('card_and_skill', Base.metadata,
    Column('card_uuid', Integer, ForeignKey('support_card.uuid')),
    Column('skill_uuid', Integer, ForeignKey('skill.uuid'))
)

uma_skill_table = Table('uma_and_skill', Base.metadata,
    Column('uma_uuid', Integer, ForeignKey('umamusume.uuid')),
    Column('skill_uuid', Integer, ForeignKey('skill.uuid'))
)
