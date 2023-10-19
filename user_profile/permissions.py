from rest_framework import permissions


class IsAuthenticatedOrCreateOrOptions(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if request.method in ["POST", "OPTIONS"]:
            return True
        return super().has_permission(request, view)
