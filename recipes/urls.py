from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView 

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from django.urls import path, include
from . import views


router = routers.DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'recipes'   , views.RecipeViewSet)

urlpatterns = [
  path('', include(router.urls)),
  path('info/', views.category_info, name='category-info'),
  path('ingredients/<int:pk>/',
       views.IngredientView.as_view(), name='ingredient-detail'),
  path('categories/<int:category_pk>/recipes/',
       views.CategoryRecipesView.as_view(), name='category-recipes'),

  path('token/'        , TokenObtainPairView .as_view(), name='token_obtain_pair'),
  path('token/refresh/', TokenRefreshView    .as_view(), name='token_refresh'),
  path('token/verify/' , TokenVerifyView     .as_view(), name='token_verify'),

  path('schema/'           , SpectacularAPIView    .as_view(), name='schema'),
  path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
  path('schema/redoc/'     , SpectacularRedocView  .as_view(url_name='schema'), name='redoc'),
]