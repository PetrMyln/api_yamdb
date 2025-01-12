from rest_framework import permissions
from rest_framework.response import Response

class NotAnyOne(permissions.BasePermission):
    def has_permission(self, request, view):
        print(1)
        return request.user.is_admin

class Admin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin or request.user.is_moderator

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin or request.user.is_moderator


class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )


class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and request.user.is_admin))



class UserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)
    
