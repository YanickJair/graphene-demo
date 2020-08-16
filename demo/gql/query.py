import graphene

import graphene_django.filter as filter

import demo.gql.node as node

class Query(graphene.AbstractType):
    users   = filter.DjangoFilterConnectionField(node.UserNode)
    user    = graphene.relay.Node.Field(node.UserNode)

    products = filter.DjangoFilterConnectionField(node.ProductNode)
    product  = graphene.relay.Node.Field(node.ProductNode)

    product_categories  = filter.DjangoFilterConnectionField(node.ProductCategoryNode)
    product_categorie   = graphene.relay.Node.Field(node.ProductCategoryNode)