from django.db import models
from recipe_api.models import Recipe, Ingredient


class IngredientForRecipe(models.Model):
    ingredient_Id = models.ForeignKey(
        Ingredient, related_name="recipe_ingredients", on_delete=models.CASCADE
    )
    recipe_Id = models.ForeignKey(
        Recipe, related_name="recipe_ingredients", on_delete=models.CASCADE
    )
    quantity = models.IntegerField()

    class Meta:
        unique_together = ("ingredient_Id", "recipe_Id")

    def __str__(self):
        return f"{self.quantity} of {self.ingredient.name} for {self.recipe.title}"
