from django.db import models
from django.contrib.auth.models import User
from .recipe import Recipe


class RecipeLike(models.Model):
    recipe_Id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user_Id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} likes {self.recipe}"
