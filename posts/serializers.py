from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from main.serializer_validation_mixins import ReadOnlyOrUnkownFieldErrorMixin
from .models import Media, Post
from user_profile.models import UserProfile


class MediaSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = "__all__"


class UpdatePostSerializer(
    ReadOnlyOrUnkownFieldErrorMixin, serializers.ModelSerializer
):
    class Meta:
        model = Post
        exclude = ["user", "repost", "embed"]

    def update(self, instance, validated_data):
        if "replies" in validated_data:
            replies = validated_data.pop("replies")
            instance.replies.add(*replies)

        instance.update(**validated_data)
        return instance


class PostSerializer(ReadOnlyOrUnkownFieldErrorMixin, serializers.ModelSerializer):
    media = MediaSerialzer(many=True, allow_null=True, required=False)
    post_user = serializers.SerializerMethodField("get_post_user")
    username = serializers.CharField(
        max_length=35, source="user__user__username", required=False
    )
    replies_count = serializers.SerializerMethodField("get_replies_count")
    likes_count = serializers.SerializerMethodField("get_likes_count")
    liked_by_user = serializers.SerializerMethodField("get_liked_by_user")

    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ["post_user"]
        extra_kwargs = {
            "user": {"write_only": True, "required": False},
            "username": {"write_only": True, "requrequiredired": False},
        }

    def get_replies_count(self, obj):
        return obj.replies.count()

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_post_user(self, obj):
        return {
            "id": obj.id,
            "name": obj.user.user.first_name,
            "username": obj.user.user.username,
            "avatar": obj.user.avatar.url if obj.user.avatar else None,
        }

    def get_liked_by_user(self, obj: Post):
        if hasattr(self, "context") and "user" in self.context:
            return obj.likes.filter(user=self.context["user"]).exists()

        return False

    def create(self, validated_data):
        if "user__user__username" in validated_data:
            username = validated_data.pop("user__user__username")
            try:
                user = UserProfile.objects.get(user__username=username)
            except:
                raise ValidationError(
                    {
                        "username": [
                            f"Invalid username '{username}' - object does not exist."
                        ]
                    }
                )
            print("user", user)
            post = Post.objects.create(user=user, **validated_data)
        elif "user" in validated_data:
            post = Post.objects.create(**validated_data)
        else:
            raise ValidationError("You must provied a user or username field")

        if "media" in validated_data:
            media_data = validated_data.pop("media")
            Media.objects.create(
                post=post,
                **media_data,
            )

        return post
