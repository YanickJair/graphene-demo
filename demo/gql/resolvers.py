from django.db import transaction

from django.contrib.auth.models import User

import graphene

import demo.gql.node as node

import demo.models as models

class CreateProductCategory(graphene.relay.ClientIDMutation):
    class Input:
        name = graphene.NonNull(graphene.String)
    
    category = graphene.Field(node.ProductCategoryNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        transaction.set_autocommit(False)
        category = None
        try:
            category = models.ProductCategory(name = input.get("name"))
            category.save()
            transaction.commit()
        except:
            transaction.rollback()
        return CreateProductCategory(category=category)

class CreateProduct(graphene.relay.ClientIDMutation):
    class Input:
        name = graphene.NonNull(graphene.String)
        category = graphene.NonNull(graphene.ID)
        price = graphene.NonNull(graphene.Float)

    product = graphene.Field(node.ProductNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        transaction.set_autocommit(False)
        product = None
        try:
            category = node.get_node_id(input.get("category"), node.ProductCategoryNode)
            category = models.ProductCategory.objects.filter(id = category)

            if category.exists():
                category = category.get()
                product = models.Product(
                    name=input.get("name"),
                    category=category,
                    price=input.get("price")
                )
                product.save()
                transaction.commit()
            else:
                raise Exception("Product Category Not Found")
        except:
            transaction.rollback()
        return CreateProduct(product=product)


""" 
Two possible actions allowed on manage favorites
"""
class ActionType(graphene.Enum):
    ADD = "Add"
    REMOVE = "Remove"

    @property
    def description(self):
        if self == ActionType.ADD:
            return "Add a new Product to Favorite list"
        return "Remove Product from Favorite list"


""" 
Manage Favorites a user can either add a product to te list or remove one from the list
"""
class ManageFavorites(graphene.relay.ClientIDMutation):
    class Input:
        user = graphene.NonNull(graphene.ID)
        product = graphene.NonNull(graphene.ID)
        action = graphene.NonNull(ActionType)
    
    favorite = graphene.Field(node.FavoritesNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        transaction.set_autocommit(False)
        favorite = None

        try:
            product = node.get_node_id(input.get("product"), node.ProductNode)
            product = models.Product.objects.filter(id = product)

            if product.exists():
                user = node.get_node_id(input.get("user"), node.UserNode)
                user = User.objects.filter(id = user)

                if user.exists():
                    product = product.get()
                    user = user.get()

                    if input.get('action') == ActionType.ADD:
                        favorite = models.Favorites(
                            user=user,
                            product=product
                        )
                        favorite.save()
                    else:
                        models.Favorites.objects.filter(
                            user=user,
                            product=product
                        ).delete()
                    transaction.commit()
                else:
                    raise Exception("User Not Found")
            else:
                raise Exception("Product Not Found")
        except:
            transaction.rollback()
        return ManageFavorites(favorite=favorite)

""" 
Create a new product's comment
"""
class Comment(graphene.relay.ClientIDMutation):
    class Input:
        user = graphene.NonNull(graphene.ID)
        product = graphene.NonNull(graphene.ID)
        text = graphene.NonNull(graphene.String)

    comment = graphene.Field(node.CommentNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        transaction.set_autocommit(False)
        comment = None

        try:
            product = node.get_node_id(input.get("product"), node.ProductNode)
            product = models.Product.objects.filter(id = product)

            if product.exists():
                user = node.get_node_id(input.get("user"), node.UserNode)
                user = User.objects.filter(id = user)

                if user.exists():
                    product = product.get()
                    user = user.get()

                    comment = models.Comment(
                        user=user,
                        product=product,
                        text=input.get("text")
                    )
                    comment.save()
                    transaction.commit()
                else:
                    raise Exception("User Not Found")
            else:
                raise Exception("Product Not Found")
        except:
            transaction.rollback()
        return Comment(commt = comment)