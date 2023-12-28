from rest_framework.permissions import BasePermission


class IsNotificationOwner(BasePermission):
    def has_object_permission(self, request, obj):
        return request.user.id == obj["receiver"]["user"]["id"]
