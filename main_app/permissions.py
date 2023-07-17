from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    """Ограничение модератора"""
    message = 'Доступ ограничен'

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return request.method in ['GET', 'PUT', 'PATCH']


class IsOwner(permissions.BasePermission):
    """Права доступа владельца записи и модератора"""
    message = 'Доступ ограничен'

    def has_object_permission(self, request, view, obj):
        if request.user == obj.user:
            return request.method in ['GET', 'PUT', 'PATCH', 'DELETE']
        return False
