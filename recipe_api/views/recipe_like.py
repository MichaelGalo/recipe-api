from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from recipe_api.models import RecipeLike, Recipe
from django.contrib.auth.models import User
from django.db.models import F, Q
from rest_framework.decorators import action


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
        """Handle GET requests for RecipeLikes and AuthorFavorites with specific filtering"""
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
                serializer = RecipeSerializer(recipes, many=True)
            else:
                # Return recipes liked by the user but not created by them
                recipe_likes = (
                    RecipeLike.objects.filter(user_Id=user_id)
                    .exclude(recipe_Id__user__id=user_id)
                    .select_related("recipe_Id", "user_Id")
                )
                serializer = RecipeLikeSerializer(recipe_likes, many=True)

            return Response(serializer.data)
        except Exception as ex:
            return Response(
                {"error": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=["GET"])
    def check_like(self, request):
        recipe_id = request.query_params.get("recipe_id")
        user_id = request.query_params.get("user_id")

        if not recipe_id or not user_id:
            return Response(
                {"error": "Both recipe_id and user_id are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            like = RecipeLike.objects.filter(
                recipe_Id_id=recipe_id, user_Id_id=user_id
            ).first()
            return Response(
                {"is_liked": like is not None, "like_id": like.id if like else None}
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
