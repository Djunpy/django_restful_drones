from rest_framework import permissions


class IsCurrentUserOwnerOrReadOnly(permissions.BasePermission):
    """Права доступа к дрону"""
    def has_object_permission(self, request, view, obj):
        # Вернет Tru если http метод read_only,
        # иначе уточнит является ли пользователь владельцем
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.owner == request.user