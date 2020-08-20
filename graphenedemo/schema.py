import asyncio

import graphene
import channels_graphql_ws

import demo.gql.query as query
import demo.gql.mutation as mutation

class DemoSubscription(channels_graphql_ws.Subscription):
    event = graphene.String()

    class Arguments:
        arg1 = graphene.String()
        arg2 = graphene.String()

    @staticmethod
    def subscribe(root, info, arg1, arg2):
        return ["group42"]
    
    @staticmethod
    def publish(payload, info, arg1, arg2):
        return DemoSubscription(event="Somethin has happened!")

class Subscription(graphene.ObjectType):
    demo_subscription = DemoSubscription.Field()

class Query(graphene.ObjectType, query.Query):
    pass

class Mutation(graphene.ObjectType, mutation.Mutation):
    pass

schema = graphene.Schema(
    query=Query,
    mutation=Mutation
)

DemoSubscription.broadcast(
    # Subscription group to notify clients in.
    group='group42',
    # Dict delivered to the `publish` method.
    payload={},
)
