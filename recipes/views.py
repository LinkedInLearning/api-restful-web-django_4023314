from django.shortcuts import render

from .models import Category, Recipe
from .serializers import CategorySerializer, RecipeListSerializer, RecipeDetailSerializer
from rest_framework import viewsets

class CategoryViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing category instances.
    """
    queryset = Category.objects.all().order_by('order')
    serializer_class = CategorySerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing recipe instances.
    """
    queryset = Recipe.objects.all().order_by('-published')
    
    def get_serializer_class(self):
        return RecipeListSerializer if self.action == 'list' else RecipeDetailSerializer
