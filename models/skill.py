from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy.orm import relationship, backref

from database import Base
from models.enum import SkillGradeEnum, SkillBuffTypeEnum, SkillDistanceTypeEnum, SkillOperationTypeEnum


class Skill(Base):
    __tablename__ = 'skill'

    uuid = Column(Integer, primary_key=True)
    name = Column(String(100))
    name_kr = Column(String(100))
    description = Column(MEDIUMTEXT)
    condition = Column(MEDIUMTEXT)
    icon = Column(String(100))
    grade_id = Column(ForeignKey('skill_grade.uuid'), index=True)
    grade = relationship(
        'SkillGrade',
        backref=backref('skill',
                        uselist=True,
                        cascade='all, save-update'))

    buff_type_id = Column(ForeignKey('skill_buff_type.uuid'), index=True)
    buff_type = relationship(
        'SkillBuffType',
        backref=backref('skill',
                        uselist=True,
                        cascade='all, save-update'))

    distance_type_id = Column(ForeignKey('skill_distance_type.uuid'), index=True)
    distance_type = relationship(
        "SkillDistanceType",
        backref=backref("skill",
                        uselist=True,
                        cascade='all, save-update'))

    operation_type_id = Column(ForeignKey('skill_operation_type.uuid'), index=True)
    operation_type = relationship(
        "SkillOperationType",
        backref=backref("skill",
                        uselist=True,
                        cascade='all, save-update'))

    cards = relationship(
        "CardSkill",
        back_populates="skill")

    uma_tachi = relationship(
        "UmaSkill",
        back_populates="skill")

    def __init__(self, name: str, name_kr: str, description: str, condition: str, icon: str):
        self.name = name
        self.name_kr = name_kr
        self.description = description
        self.condition = condition
        self.icon = icon

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"


class SkillGrade(Base):
    __tablename__ = 'skill_grade'

    uuid = Column(Integer, primary_key=True)
    name = Column(Enum(SkillGradeEnum,
                       values_callable=lambda x: [str(e.value) for e in SkillGradeEnum]),
                  nullable=False)

    def __repr__(self):
        return f"{self.name.value}"


class SkillBuffType(Base):
    __tablename__ = 'skill_buff_type'

    uuid = Column(Integer, primary_key=True)
    name = Column(Enum(SkillBuffTypeEnum,
                       values_callable=lambda x: [str(e.value) for e in SkillBuffTypeEnum]),
                  nullable=False)

    def __repr__(self):
        return f"{self.name.value}"


class SkillDistanceType(Base):
    __tablename__ = 'skill_distance_type'

    uuid = Column(Integer, primary_key=True)
    name = Column(Enum(SkillDistanceTypeEnum,
                       values_callable=lambda x: [str(e.value) for e in SkillDistanceTypeEnum]),
                  nullable=False)

    def __repr__(self):
        return f"{self.name.value}"


class SkillOperationType(Base):
    __tablename__ = 'skill_operation_type'

    uuid = Column(Integer, primary_key=True)
    name = Column(Enum(SkillOperationTypeEnum,
                       values_callable=lambda x: [str(e.value) for e in SkillOperationTypeEnum]),
                  nullable=False)

    def __repr__(self):
        return f"{self.name.value}"
