from rest_framework import permissions


class IsAuthenticatedOrCreateOrOptions(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if request.method in ["POST", "OPTIONS"]:
            return True
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if request.method not in permissions.SAFE_METHODS and request.user != obj.user:
            return False
        return True


class IsOwner(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if request.user == obj.user.user:
            return True
        return False
