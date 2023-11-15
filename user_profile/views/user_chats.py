from rest_framework.response import Response
from rest_framework import viewsets, exceptions
from chat.models import Chat, Message
from user_profile.permissions import IsOwner
from chat.serializers import (
    CreateChatSerializer,
    RetrieveChatSerializer,
    CreateMessageSerializer,
    RetrieveMessageSerializer,
)
from rest_framework import status
from rest_framework.decorators import action
from user_profile.models import UserProfile
from django.db import IntegrityError
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist


class UserChatsViewSet(viewsets.GenericViewSet):
    queryset = UserProfile.objects.all()
    permission_classes = [IsOwner]

    def get_serializer_class(self):
        if self.action == "messages":
            return RetrieveMessageSerializer
        if self.action in ["list", "retrieve"]:
            return RetrieveChatSerializer
        if self.action == "create":
            return CreateChatSerializer

    def list(self, request, chats_user__username):
        username = chats_user__username
        try:
            resource_user = self.queryset.get(user__username=username)
            print("chat res user", resource_user)
            chats = self.paginate_queryset(resource_user.chats)
            return Response(self.get_serializer(chats, many=True).data)
        except ObjectDoesNotExist:
            raise exceptions.ValidationError(
                {"username": "The username provided did not match any know users."}
            )

    def create(self, request, chats_user__username):
        username = chats_user__username
        resource_user = self.queryset.get(user__username=username)
        # self.check_object_permissions(request, resource_user)
        if "username" not in request.data:
            raise exceptions.ValidationError({"username": "Required field"})
        username_to_chat_with = request.data["username"]
        try:
            user_to_chat_with = self.queryset.get(user__username=username_to_chat_with)
            print("old chatss", Chat.objects.filter())
            deserialized_chat = self.get_serializer(
                data={
                    "first_user_profile": resource_user.id,
                    "second_user_profile": user_to_chat_with.id,
                }
            )
            if deserialized_chat.is_valid():
                chat = deserialized_chat.save()
                return Response(self.get_serializer(chat).data)
            raise exceptions.ValidationError(deserialized_chat.errors)

        except ObjectDoesNotExist:
            raise exceptions.ValidationError(
                {"username": "The username provided did not match any know users."}
            )

        except IntegrityError:
            raise exceptions.ValidationError(
                "You already converse with the user of the username provided."
            )

    def retrieve(self, request, chats_user__username, pk=None):
        print(pk)
        username = chats_user__username
        resource_user = self.queryset.get(user__username=username)
        requested_chat = resource_user.chats.filter(id=pk)
        if not requested_chat.exists():
            return Response(
                {"You don't have permission to access this chat"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return Response(self.get_serializer(requested_chat[0]).data)

    @action(methods=["GET"], detail=False, url_path=r"(?P<chat_id>[^/.]+)/messages")
    def messages(self, request, chats_user__username, chat_id):
        username = chats_user__username
        resource_user = self.queryset.get(user__username=username)
        requested_chat = resource_user.chats.filter(id=chat_id)
        print("requested chat", requested_chat)
        if not requested_chat.exists():
            return Response(
                {"You don't have permission to access this chat"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return Response(
            self.paginate_queryset(
                self.get_serializer(requested_chat[0].messages, many=True).data
            )
        )

    # @action(
    #     methods=["DELETE"],
    #     detail=False,
    #     url_path=r"(?P<unfollow_username>[^/.]+)",
    # )
    # def unfollow(self, request, following_user__username, unfollow_username):
    #     username = following_user__username
    #     try:
    #         resource_user = self.queryset.get(user__username=username)
    #         user_to_unfollow = self.queryset.get(user__username=unfollow_username)

    #         resource_user.following.get(user_profile=user_to_unfollow).delete()
    #     except ObjectDoesNotExist as e:
    #         raise exceptions.ValidationError(e)

    #     return Response(status=status.HTTP_204_NO_CONTENT)
