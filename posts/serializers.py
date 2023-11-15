from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from main.serializer_validation_mixins import ReadOnlyOrUnkownFieldErrorMixin
from .models import Media, Post
from user_profile.models import UserProfile
from user_profile.serializers import MentionSerializer, UserProfileSerializer
from main import settings


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["file"] = f"{settings.MEDIA_URL}{data.get('file')}"
        return data


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


class CreatePostSerializer(
    ReadOnlyOrUnkownFieldErrorMixin, serializers.ModelSerializer
):
    media = MediaSerializer(many=True, allow_null=True, required=False)
    username = serializers.CharField(
        max_length=35, source="user__user__username", required=False
    )

    class Meta:
        model = Post
        fields = "__all__"
        extra_kwargs = {
            "user": {"write_only": True, "required": False},
            "username": {"write_only": True, "required": False},
        }

    def get_fields(self):
        fields = super().get_fields()
        fields["embed"] = PostSerializer(required=False)
        return fields

    def create(self, validated_data):
        if "user__user__username" in validated_data:
            username = validated_data.pop("user__user__username")
            try:
                user = UserProfile.objects.get(user__username=username)
            except:
                raise ValidationError(
                    {
                        "username": f"Invalid username '{username}' - object does not exist."
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


class PostUserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="user.first_name")
    username = serializers.CharField(source="user.username")

    class Meta:
        model = UserProfile
        fields = ["id", "name", "username", "avatar"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["avatar"] = f"{settings.MEDIA_URL}{data.get('avatar')}"
        return data


class PostSerializer(ReadOnlyOrUnkownFieldErrorMixin, serializers.ModelSerializer):
    media = MediaSerializer(many=True, allow_null=True, required=False)
    post_user = serializers.SerializerMethodField("get_post_user")
    username = serializers.CharField(
        max_length=35, source="user__user__username", required=False
    )
    replies_count = serializers.SerializerMethodField("get_replies_count")
    repost_count = serializers.SerializerMethodField("get_repost_count")
    likes_count = serializers.SerializerMethodField("get_likes_count")
    liked_by_user = serializers.SerializerMethodField("get_liked_by_user")
    reposted_by_user = serializers.SerializerMethodField("get_reposted_by_user")
    post_mentions = MentionSerializer(many=True)

    class Meta:
        model = Post
        fields = "__all__"
        extra_kwargs = {
            "user": {"write_only": True, "required": False},
            "username": {"write_only": True, "required": False},
        }

    def get_fields(self):
        fields = super().get_fields()
        fields["embed"] = PostSerializer(required=False)
        fields["reply_to"] = PostSerializer(required=False)
        return fields

    def get_replies_count(self, obj):
        return obj.replies.count()

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_post_user(self, obj):
        return PostUserSerializer(instance=obj.user).data

    def get_liked_by_user(self, obj: Post):
        return obj.likes.filter(user=self.context["request"].user).exists()

    def get_reposted_by_user(self, obj: Post):
        return self.context["request"].user.profile.posts.filter(embed=obj).exists()

    def get_repost_count(self, obj: Post):
        return obj.reposts.count()
