import graphene
from graphene import relay, ObjectType
from graphene_sqlalchemy import SQLAlchemyObjectType

from models.relationship import UmaSkill
from models.uma import Umamusume, UmaEvent, UmaEventChoice


class UmaSkillType(SQLAlchemyObjectType):
    class Meta:
        model = UmaSkill


class UmamusumeType(SQLAlchemyObjectType):
    class Meta:
        model = Umamusume
        interfaces = (relay.Node,)
        exclude = ("gamewith_wiki_id",)


class UmaEventType(SQLAlchemyObjectType):
    class Meta:
        model = UmaEvent
        interfaces = (relay.Node,)


class UmaEventChoiceType(SQLAlchemyObjectType):
    class Meta:
        model = UmaEventChoice
        interfaces = (relay.Node,)


class UmamusumeQuery(ObjectType):
    umamusume = graphene.List(UmamusumeType,
                              uma_name=graphene.String(default_value=None),
                              rare_degree=graphene.Int(default_value=None))

    umamusume_id = graphene.Field(UmamusumeType,
                                     uuid=graphene.Int(required=True))

    def resolve_umamusume_id(self, info, uuid: int):
        return UmamusumeType.get_query(info).filter(Umamusume.uuid == uuid).first()

    def resolve_umamusume(self, info, **kwargs):
        query = UmamusumeType.get_query(info)

        uma_name = kwargs.get('uma_name')
        if uma_name:
            query = query.filter(Umamusume.uma_name == uma_name or Umamusume.uma_name_kr == uma_name)

        rare_degree = kwargs.get('rare_degree')
        if rare_degree:
            query = query.filter(Umamusume.rare_degree == rare_degree)

        return query.all()
