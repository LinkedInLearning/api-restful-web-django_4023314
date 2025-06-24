from django.db import connection
from django.shortcuts import render

from rest_framework.decorators import action
from rest_framework import viewsets, response

from .models import Category, Recipe
from .serializers import CategorySerializer, IngredientSerializer, RecipeListSerializer, RecipeDetailSerializer


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

    @action(detail=True, methods=['get'])
    def ingredients(self, request, pk=None):
        ingredients = self.get_object().ingredient_set.all()
        return response.Response(
            IngredientSerializer(ingredients, many=True).data
        )


def get_categories_stats(connection):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                recipes_category.id, 
                recipes_category.name, 
                COUNT(*), 
                SUM(likes) 
            FROM recipes_recipe 
            INNER JOIN recipes_category 
            ON recipes_recipe.category_id = recipes_category.id 
            GROUP BY category_id
        """)
