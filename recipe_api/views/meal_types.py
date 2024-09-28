from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from recipe_api.models import MealType


class MealTypeViewSet(viewsets.ViewSet):
    """ViewSet for the MealType model"""

    class MealTypeSerializer(serializers.ModelSerializer):
        """JSON serializer for meal types"""

        class Meta:
            model = MealType
            fields = ("id", "name")

    def list(self, request):
        """GET all meal types"""
        meal_types = MealType.objects.all()
        serializer = self.MealTypeSerializer(meal_types, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """GET a single meal type"""
        try:
            meal_type = MealType.objects.get(pk=pk)
            serializer = self.MealTypeSerializer(meal_type)
            return Response(serializer.data)
        except MealType.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """POST a new meal type"""
        serializer = self.MealTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """PUT (update) an existing meal type"""
        try:
            meal_type = MealType.objects.get(pk=pk)
            serializer = self.MealTypeSerializer(meal_type, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except MealType.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """DELETE a meal type"""
        try:
            meal_type = MealType.objects.get(pk=pk)
            meal_type.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except MealType.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
