from django.db import models
from django.contrib.auth.models import User
from .meal_types import MealType


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    meal_type = models.ForeignKey(MealType, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    author_favorite = models.BooleanField()
    favorites = models.IntegerField()
    time = models.IntegerField()
    servings = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return self.title
