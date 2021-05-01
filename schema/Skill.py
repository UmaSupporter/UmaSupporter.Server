import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from models.skill import Skill, SkillBuffType, SkillGrade, SkillDistanceType, SkillOperationType


class SkillType(SQLAlchemyObjectType):
    class Meta:
        model = Skill
        exclude_fields = ("grade_id", "buff_type_id", "distance_type_id", "operation_type_id")


class SkillBuffTypeType(SQLAlchemyObjectType):
    class Meta:
        model = SkillBuffType


class SkillGradeType(SQLAlchemyObjectType):
    class Meta:
        model = SkillGrade


class SkillDistanceTypeType(SQLAlchemyObjectType):
    class Meta:
        model = SkillDistanceType


class SkillOperationTypeType(SQLAlchemyObjectType):
    class Meta:
        model = SkillOperationType


class SkillQuery(graphene.ObjectType):
    skill_name = graphene.Field(SkillType,
                              name=graphene.String())

    skill = graphene.List(SkillType)

    def resolve_skill_name(self, info, name: str):
        return SkillType.get_query(info).filter(Skill.name == name).first()

    def resolve_skill(self, info):
        query = SkillType.get_query(info)
        return query.all()
