from django.db import connection
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework.decorators import action, api_view, permission_classes, throttle_classes
from rest_framework import viewsets, response, generics, filters, throttling

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema

from .throttling import InfoRateThrottle
from .permissions import IsAdminOrReadOnly, UnlockedRecipe, UnlockedIngredient
from .models import Category, Recipe, Ingredient
from .serializers import CategorySerializer, CategoryInfoSerializer, IngredientFullSerializer, IngredientUrlSerializer, RecipeListSerializer, RecipeDetailSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing category instances.
    """
    queryset = Category.objects.all().order_by('order')
    serializer_class = CategorySerializer
    template_name = 'categories.html'
    ordering_fields = ['order']
    search_fields = ['name']
    permission_classes = [IsAdminOrReadOnly]

    @method_decorator(cache_page(60 * 60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


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
    permission_classes = [IsAdminOrReadOnly | UnlockedRecipe]
    throttle_classes = [throttling.UserRateThrottle, throttling.AnonRateThrottle]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.query_params.get('locked') is not None:
            queryset = queryset.filter(password__isnull=False)
        return queryset

    def get_serializer_class(self):
        return RecipeListSerializer if self.action == 'list' else RecipeDetailSerializer

    @extend_schema(
        methods=['GET'],
        summary='List ingredients for a recipe',
        responses={200: IngredientUrlSerializer(many=True)}
    )
    @extend_schema(
        methods=['POST'],
        summary='Add an ingredient to a recipe',
        request=IngredientUrlSerializer(),
        responses={201: IngredientUrlSerializer(many=False)}
    )
    @action(
        detail=True, 
        methods=['GET', 'POST'], 
        permission_classes=[IsAdminOrReadOnly | UnlockedRecipe], 
        pagination_class=None
    )
    def ingredients(self, request, pk=None):
        if request.method == 'POST':
            recipe = self.get_object()
            serializer = IngredientUrlSerializer(data=request.data, context={'request': request})
            if not serializer.is_valid():
                return response.Response(serializer.errors, status=400)
            serializer.save(recipe=recipe)
            return response.Response(serializer.data, status=201)
            
        return response.Response(
            IngredientUrlSerializer(
                self.get_object().ingredient_set.all(), 
                many=True, 
                context={'request': request}
            ).data
        )


class IngredientView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientFullSerializer
    permission_classes = [IsAdminOrReadOnly | UnlockedIngredient]


class CategoryRecipesView(generics.ListAPIView):
    serializer_class = RecipeListSerializer
    template_name = 'recipes.html'
    permission_classes = []
    throttle_classes = [throttling.UserRateThrottle,
                        throttling.AnonRateThrottle]

    def get_queryset(self):
        return Recipe.objects.filter(
            category_id=self.kwargs.get('category_pk')
        ).order_by('-published')


@api_view(['GET'])
@permission_classes([])
@throttle_classes([InfoRateThrottle])
def category_info(request):
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
