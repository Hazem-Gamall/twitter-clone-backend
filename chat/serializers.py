from .models import Chat, Message
from rest_framework import serializers
from user_profile.serializers import UserProfileSerializer


class CreateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class RetrieveMessageSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer()
    chat_users = serializers.ReadOnlyField()

    class Meta:
        model = Message
        fields = "__all__"


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
