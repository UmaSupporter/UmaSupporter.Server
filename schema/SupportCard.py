import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from models import SupportCard, CardEvent, CardEventChoice


class SupportCardType(SQLAlchemyObjectType):
    class Meta:
        model = SupportCard
        interfaces = (relay.Node,)
        exclude = ("gamewith_wiki_id",)


class CardEventType(SQLAlchemyObjectType):
    class Meta:
        model = CardEvent
        interfaces = (relay.Node,)


class CardEventChoiceType(SQLAlchemyObjectType):
    class Meta:
        model = CardEventChoice
        interfaces = (relay.Node,)
