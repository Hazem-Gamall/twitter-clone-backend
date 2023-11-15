from .models import Chat, Message
from rest_framework import serializers
from user_profile.serializers import UserProfileSerializer


class CreateChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = "__all__"


class RetrieveChatSerializer(serializers.ModelSerializer):
    first_user_profile = UserProfileSerializer()
    second_user_profile = UserProfileSerializer()

    class Meta:
        model = Chat
        fields = "__all__"


class CreateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class RetrieveMessageSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer()

    class Meta:
        model = Message
        fields = "__all__"
