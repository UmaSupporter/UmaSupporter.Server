import graphene

from schema.Query import Query

schema = graphene.Schema(query=Query)

