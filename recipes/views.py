from django.db import connection
from django.shortcuts import render

from rest_framework.decorators import action
from rest_framework import viewsets, response, generics, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Category, Recipe
from .serializers import CategorySerializer, CategoryInfoSerializer, IngredientSerializer, RecipeListSerializer, RecipeDetailSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing category instances.
    """
    queryset = Category.objects.all().order_by('order')
    serializer_class = CategorySerializer
    template_name = 'categories.html'
    ordering_fields = ['order']
    search_fields = ['name']


class RecipeViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing recipe instances.
    """
    queryset = Recipe.objects.all().order_by('-published')
    template_name = 'recipes.html'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'vegan': ['exact'],
        'likes': ['gte', 'lte'],
        'published': ['gte', 'lte']
    }    
    search_fields = ['title', 'description', 'instructions', 'category__name']
    ordering_fields = ['title', 'published', 'likes']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.query_params.get('locked') is not None:
            queryset = queryset.filter(password__isnull=False)
        return queryset

    def get_serializer_class(self):
        return RecipeListSerializer if self.action == 'list' else RecipeDetailSerializer

    @action(detail=True, methods=['get'])
    def ingredients(self, request, pk=None):
        ingredients = self.get_object().ingredient_set.all()
        return response.Response(
            IngredientSerializer(ingredients, many=True).data
        )


class CategoryRecipesView(generics.ListAPIView):
    serializer_class = RecipeListSerializer
    template_name = 'recipes.html'

    def get_queryset(self):
        return Recipe.objects.filter(
            category_id=self.kwargs.get('category_pk')
        ).order_by('-published')


class CategoryInfoViewSet(viewsets.ViewSet):
    def list(self, request):
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
            return response.Response(
                CategoryInfoSerializer(cursor.fetchall(), many=True).data
            )
