from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.groups.filter(name='Merchant').exists() and request.user.is_authenticated


    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author.id == request.user.id