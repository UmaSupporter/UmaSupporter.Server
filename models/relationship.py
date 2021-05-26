from sqlalchemy import Table, Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship

from database import Base
from models.enum import CardSkillCategoryEnum, UmaSkillCategoryEnum


class CardSkill(Base):
    __tablename__ = 'card_and_skill'

    card_uuid = Column(Integer, ForeignKey('support_card.uuid'), primary_key=True)
    skill_uuid = Column(Integer, ForeignKey('skill.uuid'), primary_key=True)
    category = Column(Enum(CardSkillCategoryEnum,
                       values_callable=lambda x: [str(e.value) for e in CardSkillCategoryEnum]),
                  nullable=False)
    card = relationship("SupportCard", back_populates="skills")
    skill = relationship("Skill", back_populates="cards")

    def __repr__(self):
        return f"{self.card}, {self.skill}"


class UmaSkill(Base):
    __tablename__ = 'uma_and_skill'

    uma_uuid = Column(Integer, ForeignKey('umamusume.uuid'), primary_key=True)
    skill_uuid = Column(Integer, ForeignKey('skill.uuid'), primary_key=True)
    category = Column(Enum(UmaSkillCategoryEnum,
                       values_callable=lambda x: [str(e.value) for e in UmaSkillCategoryEnum]),
                  nullable=False)
    uma = relationship("Umamusume", back_populates="skills")
    skill = relationship("Skill", back_populates="uma_tachi")

    def __repr__(self):
        return f"{self.uma}, {self.skill}"
