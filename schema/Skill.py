from graphene_sqlalchemy import SQLAlchemyObjectType

from models import Skill


class SkillType(SQLAlchemyObjectType):
    class Meta:
        model = Skill
