from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from recipe_api.views import register_user, login_user, current_user, RecipeView

router = routers.DefaultRouter(trailing_slash=False)
# example below of a new route
router.register(r"recipes", RecipeView, basename="recipes")

urlpatterns = [
    path("", include(router.urls)),
    path("register", register_user),
    path("login", login_user),
    path("current_user", current_user, name="current_user"),
]
