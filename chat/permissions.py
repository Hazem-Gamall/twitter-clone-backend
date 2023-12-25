from rest_framework.permissions import BasePermission


class IsChatParticipant(BasePermission):
    def has_object_permission(self, request, obj):
        print("chat", obj)
        return (
            request.user.id in obj["chat_users"]
            and request.user.id != obj["author"]["user"]["id"]
        )
