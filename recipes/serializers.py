from .models import Category, Recipe, Ingredient
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class RecipeListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Recipe
        exclude = ['password', 'instructions']

    imageUrl = serializers.CharField(source='image.url', read_only=True)

class RecipeDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'

    likes = serializers.IntegerField(read_only=True)
    image = serializers.CharField()
    categoryName = serializers.CharField(source='category.name', read_only=True)
    published = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    password = serializers.CharField(write_only=True, required=False)
    veganTitle = serializers.SerializerMethodField()
    ingredients = serializers.SerializerMethodField()

    def get_veganTitle(self, obj):
        return "Vegan" if obj.vegan else "Non-Vegan"
    
    def get_ingredients(self, obj):
        ingredients = obj.ingredient_set.all()
        return IngredientSerializer(ingredients, many=True).data


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['name', 'optional']


class CategoryInfoSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'category_id': instance[0],
            'category_name': instance[1],
            'recipes': instance[2],
            'likes': instance[3]
        }
    