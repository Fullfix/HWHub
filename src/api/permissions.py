from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import permissions


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user.is_admin

class UserIsOwnerOrReadOnlyProfile(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (obj.id == request.user.profile.id)


class UserIsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (obj.id == request.user.id)

class UserIsOwnerOrAdminHomework(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (obj.publisher.id == request.user.id) or request.user.is_staff