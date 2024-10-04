from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from recipe_api.models import Recipe, MealType, RecipeLike
from django.contrib.auth.models import User
from rest_framework.decorators import action


class RecipeView(ViewSet):
    """Recipe view set"""

    def create(self, request):
        """Handle POST operations"""
        try:
            meal_type = MealType.objects.get(pk=request.data["mealTypeId"])
            user = User.objects.get(pk=request.data["userId"])

            recipe = Recipe.objects.create(
                title=request.data["title"],
                body=request.data["body"],
                meal_type=meal_type,
                user=user,
                author_favorite=request.data["authorFavorite"],
                favorites=request.data["favorites"],
                time=request.data["time"],
                servings=request.data["servings"],
                date=request.data["date"],
            )
            serializer = RecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"reason": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single recipe"""
        try:
            recipe = Recipe.objects.get(pk=pk)
            serializer = RecipeSerializer(recipe)
            return Response(serializer.data)
        except Recipe.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        """Handle PUT requests for a recipe"""
        try:
            recipe = Recipe.objects.get(pk=pk)
            meal_type = MealType.objects.get(pk=request.data["meal_type"])
            user = User.objects.get(pk=request.data["user"])

            recipe.title = request.data["title"]
            recipe.body = request.data["body"]
            recipe.meal_type = meal_type
            recipe.user = user
            recipe.author_favorite = request.data["author_favorite"]
            recipe.favorites = request.data["favorites"]
            recipe.time = request.data["time"]
            recipe.servings = request.data["servings"]
            recipe.date = request.data["date"]
            recipe.save()

            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Recipe.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(str(ex))

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single recipe"""
        try:
            recipe = Recipe.objects.get(pk=pk)
            recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Recipe.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response(
                {"message": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def list(self, request):
        """Handle GET requests to get all recipes"""
        recipes = Recipe.objects.all()

        # Add filtering options
        meal_type = request.query_params.get("meal_type", None)
        if meal_type is not None:
            recipes = recipes.filter(meal_type__id=meal_type)

        user = request.query_params.get("userId", None)
        if user is not None:
            recipes = recipes.filter(user__id=user)

        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def favorites(self, request):
        """Handle GET requests for favorite recipes"""
        try:
            user_id = request.query_params.get("userId")
            if user_id is None:
                return Response(
                    {"error": "userId is required"}, status=status.HTTP_400_BAD_REQUEST
                )

            author_favorite = request.query_params.get("authorFavorite")

            if author_favorite and author_favorite.lower() == "true":
                # Return recipes created by the user and marked as author_favorite
                recipes = Recipe.objects.filter(user__id=user_id, author_favorite=True)
            else:
                # Return recipes liked by the user but not created by them
                liked_recipe_ids = RecipeLike.objects.filter(
                    user_Id=user_id
                ).values_list("recipe_Id", flat=True)
                recipes = Recipe.objects.filter(id__in=liked_recipe_ids).exclude(
                    user__id=user_id
                )

            serializer = RecipeSerializer(recipes, many=True)
            return Response(serializer.data)
        except Exception as ex:
            return Response(
                {"error": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "username")


class RecipeSerializer(serializers.ModelSerializer):
    """JSON serializer for recipes"""

    meal_type = serializers.ReadOnlyField(
        source="meal_type.name"
    )  # does this need dunder?
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "title",
            "body",
            "meal_type",
            "user",
            "author_favorite",
            "favorites",
            "time",
            "servings",
            "date",
        )
