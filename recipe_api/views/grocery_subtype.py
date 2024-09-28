from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from recipe_api.models import GrocerySubType


class GrocerySubTypeView(ViewSet):
    """GrocerySubType view set"""

    class GrocerySubTypeSerializer(serializers.ModelSerializer):
        """JSON serializer for grocery subtypes"""

        class Meta:
            model = GrocerySubType
            fields = ("id", "name")

    def create(self, request):
        """Handle POST operations for grocery subtypes"""
        try:
            grocery_subtype = GrocerySubType.objects.create(name=request.data["name"])
            serializer = self.GrocerySubTypeSerializer(grocery_subtype)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"reason": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single grocery subtype"""
        try:
            grocery_subtype = GrocerySubType.objects.get(pk=pk)
            serializer = self.GrocerySubTypeSerializer(grocery_subtype)
            return Response(serializer.data)
        except GrocerySubType.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        """Handle PUT requests for a grocery subtype"""
        try:
            grocery_subtype = GrocerySubType.objects.get(pk=pk)
            grocery_subtype.name = request.data["name"]
            grocery_subtype.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except GrocerySubType.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(str(ex))

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single grocery subtype"""
        try:
            grocery_subtype = GrocerySubType.objects.get(pk=pk)
            grocery_subtype.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except GrocerySubType.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response(
                {"message": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def list(self, request):
        """Handle GET requests to get all grocery subtypes"""
        grocery_subtypes = GrocerySubType.objects.all()
        serializer = self.GrocerySubTypeSerializer(grocery_subtypes, many=True)
        return Response(serializer.data)
