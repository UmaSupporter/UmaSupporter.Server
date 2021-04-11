import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from models import Buff


class BuffType(SQLAlchemyObjectType):
    class Meta:
        model = Buff


class BuffQuery(graphene.ObjectType):
    buff_with_name = graphene.Field(BuffType,
                                    name=graphene.String())

    def resolve_buff_with_name(self, info, name: str):
        return BuffType.get_query(info).filter(Buff.name == name).first()
