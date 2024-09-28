from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from recipe_api.models import RecipeLike, Recipe
from django.contrib.auth.models import User


class RecipeLikeSerializer(serializers.ModelSerializer):
    """JSON serializer for RecipeLike"""

    class Meta:
        model = RecipeLike
        fields = ("id", "recipe_Id", "user_Id")


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
        """Handle GET requests for all items"""
        try:
            recipe_likes = RecipeLike.objects.all()
            serializer = RecipeLikeSerializer(recipe_likes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(str(ex))
