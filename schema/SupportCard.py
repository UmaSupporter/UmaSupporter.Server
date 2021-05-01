import graphene
from graphene import relay, ObjectType
from graphene_sqlalchemy import SQLAlchemyObjectType

from models.relationship import CardSkill
from models.card import SupportCard, CardEvent, CardEventChoice


class CardSkillType(SQLAlchemyObjectType):
    class Meta:
        model = CardSkill


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


class SupportCardQuery(ObjectType):
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
