import graphene

from models import SupportCard, Umamusume
from schema.SupportCard import SupportCardType
from schema.Umamusume import UmamusumeType


class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    support_card = graphene.List(SupportCardType,
                                 card_name=graphene.String(default_value=None),
                                 rare_degree=graphene.String(default_value=None))

    support_card_id = graphene.Field(SupportCardType,
                                     uuid=graphene.Int(required=True))

    umamusume = graphene.List(UmamusumeType,
                              uma_name=graphene.String(default_value=None),
                              rare_degree=graphene.Int(default_value=None))

    umamusume_id = graphene.Field(UmamusumeType,
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
