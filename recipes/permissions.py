from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_superuser


class UnlockedRecipe(BasePermission):
    def has_object_permission(self, request, view, obj):
        return not obj.password


class UnlockedIngredient(BasePermission):
    def has_object_permission(self, request, view, obj):
        return not obj.recipe.password
