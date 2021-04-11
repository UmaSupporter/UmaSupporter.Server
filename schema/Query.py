import graphene

from schema.Buff import BuffQuery
from schema.Skill import SkillQuery
from schema.SupportCard import SupportCardQuery
from schema.Umamusume import UmamusumeQuery


class Query(SupportCardQuery,
            UmamusumeQuery,
            SkillQuery,
            BuffQuery,
            graphene.ObjectType):
    node = graphene.relay.Node.Field()
