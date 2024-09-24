from django.db import models
from .ingredient import Ingredient
from .recipe import Recipe


class IngredientForRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.ingredient} for {self.recipe}"
