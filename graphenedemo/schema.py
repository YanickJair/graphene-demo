import asyncio

import graphene

import demo.gql.query as query
import demo.gql.mutation as mutation

class Query(graphene.ObjectType, query.Query):
    pass

class Mutation(graphene.ObjectType, mutation.Mutation):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
