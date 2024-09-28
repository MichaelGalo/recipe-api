from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from recipe_api.views import (
    register_user,
    login_user,
    current_user,
    RecipeView,
    GrocerySubTypeView,
    MealTypeViewSet,
    IngredientViewSet,
)

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"recipes", RecipeView, basename="recipes")
router.register(r"grocery_subtypes", GrocerySubTypeView, basename="subtypes")
router.register(r"meal_types", MealTypeViewSet, basename="meal_types")
router.register(r"ingredients", IngredientViewSet, basename="ingredients")

urlpatterns = [
    path("", include(router.urls)),
    path("register", register_user),
    path("login", login_user),
    path("current_user", current_user, name="current_user"),
]

# Still need to test:
