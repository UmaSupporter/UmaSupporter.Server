from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from models import UmaEvent, Umamusume, UmaEventChoice


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
