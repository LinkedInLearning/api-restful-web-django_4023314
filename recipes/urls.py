from rest_framework import routers

from .views import CategoryViewSet, RecipeViewSet, CategoryInfoViewSet

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'recipes'   , RecipeViewSet)
router.register(r'info'      , CategoryInfoViewSet, basename='category-info')

urlpatterns = router.urls