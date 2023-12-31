from rest_framework import permissions


class IsOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.get_user():
            return True
        return False


class IsOwnerOrSafeMethod(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user == obj.get_user():
            return True
        return False
