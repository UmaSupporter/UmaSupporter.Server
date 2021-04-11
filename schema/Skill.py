import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from models import Skill


class SkillType(SQLAlchemyObjectType):
    class Meta:
        model = Skill


class SkillQuery(graphene.ObjectType):
    skill_name = graphene.Field(SkillType,
                              name=graphene.String())

    skill = graphene.List(SkillType)

    def resolve_skill_name(self, info, name: str):
        return SkillType.get_query(info).filter(Skill.name == name).first()

    def resolve_skill(self, info):
        query = SkillType.get_query(info)

        return query.all()
