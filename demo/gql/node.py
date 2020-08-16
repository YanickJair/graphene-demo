from base64 import standard_b64decode, standard_b64encode

import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User

from demo import models

class UserNode(DjangoObjectType):
    class Meta:
        model = User
        exclude_fields = ['password']
        filter_fields = {
            'email': ['exact'],
            'username': ['exact']
        }
        interfaces = (graphene.relay.Node, )


class ProductNode(DjangoObjectType):
    class Meta:
        model = models.Product
        filter_fields = {
            'category': ['exact'],
            'price': ['exact'],
            'category__name': ['exact', 'icontains']
        }
        interfaces = (graphene.relay.Node, )

class FavoritesNode(DjangoObjectType):
    class Meta:
        model = models.Favorites
        interfaces = (graphene.relay.Node, )

class ProductCategoryNode(DjangoObjectType):
    class Meta:
        model = models.ProductCategory
        filter_fields = {
            'name': ['exact']
        }
        interfaces = (graphene.relay.Node, )

class CommentNode(DjangoObjectType):
    class Meta:
        model = models.Comment
        filter_fields = {
            'user': ['exact'],
            'product': ['exact'],
        }
        interfaces = (graphene.relay.Node, )

#* Helper function that help us get the Node/Model id
def get_node_id(id_base64, node):
    _type, _id = standard_b64decode(id_base64.encode('utf-8')).decode('utf-8').split(':')
    assert _type == node._meta.name
    return _id