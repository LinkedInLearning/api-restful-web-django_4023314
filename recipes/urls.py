from rest_framework import routers

from .views import CategoryViewSet, RecipeViewSet

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'recipes'   , RecipeViewSet)

urlpatterns = router.urls