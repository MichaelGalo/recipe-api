from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from recipe_api.models import RecipeLike, Recipe
from django.contrib.auth.models import User
from django.db.models import F, Q


# TODO: Add recipe serializer and import statement of the model
class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ("id", "title", "body", "meal_type", "user")  #  maybe add other info


class RecipeLikeSerializer(serializers.ModelSerializer):
    """JSON serializer for RecipeLike"""

    recipe = RecipeSerializer(source="recipe_Id", read_only=True)

    class Meta:
        model = RecipeLike
        fields = ("id", "recipe_Id", "user_Id", "recipe")


class RecipeLikeViewSet(ViewSet):
    """RecipeLike view set"""

    def create(self, request):
        """Handle POST operations"""
        try:
            recipe = Recipe.objects.get(pk=request.data["recipe_Id"])
            user = User.objects.get(pk=request.data["user_Id"])

            recipe_like = RecipeLike.objects.create(recipe_Id=recipe, user_Id=user)
            serializer = RecipeLikeSerializer(recipe_like)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Recipe.DoesNotExist:
            return Response(
                {"message": "Recipe not found"}, status=status.HTTP_400_BAD_REQUEST
            )
        except User.DoesNotExist:
            return Response(
                {"message": "User not found"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as ex:
            return Response({"message": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single item"""
        try:
            recipe_like = RecipeLike.objects.get(pk=pk)
            serializer = RecipeLikeSerializer(recipe_like)
            return Response(serializer.data)
        except RecipeLike.DoesNotExist:
            return Response(
                {"message": "RecipeLike not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            return Response({"message": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT requests"""
        try:
            recipe_like = RecipeLike.objects.get(pk=pk)
            recipe_like.recipe_Id = Recipe.objects.get(pk=request.data["recipe_Id"])
            recipe_like.user_Id = User.objects.get(pk=request.data["user_Id"])
            recipe_like.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except RecipeLike.DoesNotExist:
            return Response(
                {"message": "RecipeLike not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Recipe.DoesNotExist:
            return Response(
                {"message": "Recipe not found"}, status=status.HTTP_400_BAD_REQUEST
            )
        except User.DoesNotExist:
            return Response(
                {"message": "User not found"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as ex:
            return HttpResponseServerError(str(ex))

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single item"""
        try:
            recipe_like = RecipeLike.objects.get(pk=pk)
            recipe_like.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except RecipeLike.DoesNotExist:
            return Response(
                {"message": "RecipeLike not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            return Response(
                {"message": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def list(self, request):
        """Handle GET requests for all items with filtering"""
        try:
            # Get the required user_id from query parameters
            user_id = request.query_params.get("userId")

            # If user_id is not provided, return a bad request response
            if user_id is None:
                return Response(
                    {"error": "userId is required"}, status=status.HTTP_400_BAD_REQUEST
                )

            # Filter recipe likes by the given user_id
            recipe_likes = RecipeLike.objects.select_related(
                "recipe_Id", "user_Id"
            ).filter(user_Id=user_id)

            # Filter for recipes liked by the user but not authored by them
            liked_not_authored = request.query_params.get("likedNotAuthored")
            if liked_not_authored and liked_not_authored.lower() == "true":
                recipe_likes = recipe_likes.filter(~Q(recipe_Id__user=F("user_Id")))

            # Filter for recipes liked by the user and authored by them
            liked_and_authored = request.query_params.get("likedAndAuthored")
            if liked_and_authored and liked_and_authored.lower() == "true":
                recipe_likes = recipe_likes.filter(recipe_Id__user=F("user_Id"))

            serializer = RecipeLikeSerializer(recipe_likes, many=True)
            return Response(serializer.data)
        except Exception as ex:
            return Response(
                {"error": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
