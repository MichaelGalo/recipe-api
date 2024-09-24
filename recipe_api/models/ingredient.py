from django.db import models
from .grocery_subtype import GrocerySubType


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    grocerySubTypeId = models.ForeignKey(GrocerySubType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
