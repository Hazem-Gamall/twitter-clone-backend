from rest_framework.permissions import BasePermission
from chat.models import Message


class IsChatParticipant(BasePermission):
    def has_object_permission(self, request, obj):
        print("chat", obj)
        return (
            request.user.id in obj["chat_users"]
            and request.user.id != obj["author"]["user"]["id"]
        )


class IsMessageReceiver(BasePermission):
    def has_object_permission(self, request, view, obj: Message):
        return (
            request.user.id in obj.chat_users and request.user.id != obj.author.user.id
        )
