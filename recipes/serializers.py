from .models import Category, Recipe, Ingredient
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class RecipeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        exclude = ['password', 'instructions']


class RecipeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        exclude = ['password']


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['name', 'optional']
