from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from recipe_api.models import IngredientForRecipe, Ingredient, Recipe


class IngredientForRecipeSerializer(serializers.ModelSerializer):
    """JSON serializer for IngredientForRecipe"""

    class Meta:
        model = IngredientForRecipe
        fields = (
            "id",
            "ingredient_Id",
            "recipe_Id",
            "quantity",
        )


class IngredientForRecipeViewSet(ViewSet):
    """IngredientForRecipe view set"""

    def create(self, request):
        """Handle POST operations"""
        try:
            ingredient = Ingredient.objects.get(pk=request.data["ingredient_id"])
            recipe = Recipe.objects.get(pk=request.data["recipe_id"])

            ingredient_for_recipe = IngredientForRecipe.objects.create(
                ingredient_Id=ingredient,
                recipe_Id=recipe,
                quantity=request.data["quantity"],
            )
            serializer = IngredientForRecipeSerializer(ingredient_for_recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Ingredient.DoesNotExist:
            return Response(
                {"message": "Ingredient not found"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Recipe.DoesNotExist:
            return Response(
                {"message": "Recipe not found"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as ex:
            return Response({"message": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single item"""
        try:
            ingredient_for_recipe = IngredientForRecipe.objects.get(pk=pk)
            serializer = IngredientForRecipeSerializer(ingredient_for_recipe)
            return Response(serializer.data)
        except IngredientForRecipe.DoesNotExist:
            return Response(
                {"message": "IngredientForRecipe not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as ex:
            return Response({"message": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT requests"""
        try:
            ingredient_for_recipe = IngredientForRecipe.objects.get(pk=pk)
            ingredient_for_recipe.ingredient_Id = Ingredient.objects.get(
                pk=request.data["ingredient_id"]
            )
            ingredient_for_recipe.recipe_Id = Recipe.objects.get(
                pk=request.data["recipe_id"]
            )
            ingredient_for_recipe.quantity = request.data["quantity"]
            ingredient_for_recipe.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except IngredientForRecipe.DoesNotExist:
            return Response(
                {"message": "IngredientForRecipe not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Ingredient.DoesNotExist:
            return Response(
                {"message": "Ingredient not found"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Recipe.DoesNotExist:
            return Response(
                {"message": "Recipe not found"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as ex:
            return HttpResponseServerError(str(ex))

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single item"""
        try:
            ingredient_for_recipe = IngredientForRecipe.objects.get(pk=pk)
            ingredient_for_recipe.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except IngredientForRecipe.DoesNotExist:
            return Response(
                {"message": "IngredientForRecipe not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as ex:
            return Response(
                {"message": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def list(self, request):
        """Handle GET requests for all items"""
        try:
            ingredient_for_recipes = IngredientForRecipe.objects.all()
            serializer = IngredientForRecipeSerializer(
                ingredient_for_recipes, many=True
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(str(ex))
