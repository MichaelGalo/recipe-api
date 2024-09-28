from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from recipe_api.models import Ingredient, GrocerySubType


class IngredientViewSet(viewsets.ViewSet):
    """ViewSet for the Ingredient model"""

    class IngredientSerializer(serializers.ModelSerializer):
        """JSON serializer for ingredients"""

        grocery_sub_type_name = serializers.ReadOnlyField(
            source="grocerySubTypeId.name"
        )

        class Meta:
            model = Ingredient
            fields = ("id", "name", "grocerySubTypeId", "grocery_sub_type_name")

    def list(self, request):
        """GET all ingredients"""
        ingredients = Ingredient.objects.all()
        serializer = self.IngredientSerializer(ingredients, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """GET a single ingredient"""
        try:
            ingredient = Ingredient.objects.get(pk=pk)
            serializer = self.IngredientSerializer(ingredient)
            return Response(serializer.data)
        except Ingredient.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """POST a new ingredient"""
        serializer = self.IngredientSerializer(data=request.data)
        if serializer.is_valid():
            try:
                grocery_sub_type = GrocerySubType.objects.get(
                    pk=request.data["grocerySubTypeId"]
                )
                serializer.save(grocerySubTypeId=grocery_sub_type)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except GrocerySubType.DoesNotExist:
                return Response(
                    {"grocerySubTypeId": "Invalid GrocerySubType ID"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """PUT (update) an existing ingredient"""
        try:
            ingredient = Ingredient.objects.get(pk=pk)
            serializer = self.IngredientSerializer(
                ingredient, data=request.data, partial=True
            )
            if serializer.is_valid():
                if "grocerySubTypeId" in request.data:
                    try:
                        grocery_sub_type = GrocerySubType.objects.get(
                            pk=request.data["grocerySubTypeId"]
                        )
                        serializer.save(grocerySubTypeId=grocery_sub_type)
                    except GrocerySubType.DoesNotExist:
                        return Response(
                            {"grocerySubTypeId": "Invalid GrocerySubType ID"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                else:
                    serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Ingredient.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """DELETE an ingredient"""
        try:
            ingredient = Ingredient.objects.get(pk=pk)
            ingredient.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Ingredient.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
