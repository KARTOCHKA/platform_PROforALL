from rest_framework import permissions


class IsUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in ['GET', 'PUT', 'PATCH']

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        return request.user == obj
