import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

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


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    support_card = graphene.List(SupportCardType,
                                 card_name=graphene.String(default_value=None),
                                 rare_degree=graphene.String(default_value=None))

    support_card_id = graphene.Field(SupportCardType,
                                     uuid=graphene.Int(required=True))

    def resolve_support_card_id(self, info, uuid: int):
        return SupportCardType.get_query(info).filter(SupportCard.uuid == uuid).first()

    def resolve_support_card(self, info, **kwargs):
        query = SupportCardType.get_query(info)

        card_name = kwargs.get('card_name')
        if card_name:
            query = query.filter(SupportCard.card_name == card_name)

        rare_degree = kwargs.get('rare_degree')
        if rare_degree:
            query = query.filter(SupportCard.rare_degree == rare_degree)

        return query.all()


schema = graphene.Schema(query=Query, types=[SupportCardType])
