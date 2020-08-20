from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

class ProductCategory(models.Model):
    name = models.CharField(max_length=80)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=150)
    category = models.OneToOneField(ProductCategory, on_delete=models.CASCADE)
    price = models.FloatField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text
    
class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        """ 
        Let's make sure one user don't add product to favorites twice by defining a constraint
        """
        constraints = [
            models.UniqueConstraint(
                name="unique_favorite_user",
                fields=["user", "product"]
            )
        ]