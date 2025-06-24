from rest_framework import routers
from django.urls import path, include
from . import views

router = routers.DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'recipes'   , views.RecipeViewSet)
router.register(r'info'      , views.CategoryInfoViewSet, basename='category-info')

urlpatterns = [
  path('', include(router.urls)),
  path('ingredients/<int:pk>/',
       views.IngredientView.as_view(), name='ingredient-detail'),
  path('categories/<int:category_pk>/recipes/',
       views.CategoryRecipesView.as_view(), name='category-recipes'),
]