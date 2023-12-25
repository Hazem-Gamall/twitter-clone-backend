from .models import Chat, Message
from rest_framework import serializers
from user_profile.serializers import UserProfileSerializer


class CreateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class RetrieveMessageSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer()
    chat_users = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = "__all__"

    def get_chat_users(self, obj: Message):
        return [
            obj.chat.first_user_profile.user.id,
            obj.chat.second_user_profile.user.id,
        ]


class CreateChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = "__all__"


class RetrieveChatSerializer(serializers.ModelSerializer):
    first_user_profile = UserProfileSerializer()
    second_user_profile = UserProfileSerializer()
    last_message = RetrieveMessageSerializer()

    class Meta:
        model = Chat
        fields = "__all__"
