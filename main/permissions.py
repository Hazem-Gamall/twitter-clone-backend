from rest_framework import permissions


class IsOwner(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if request.user == obj.get_user():
            return True
        return False
