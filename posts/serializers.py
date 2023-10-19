from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from main.serializer_validation_mixins import ReadOnlyOrUnkownFieldErrorMixin
from .models import Media, Post


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

    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ["replies"]

    def create(self, validated_data):
        post = Post.objects.create(**validated_data)

        if "media" in validated_data:
            media_data = validated_data.pop("media")
            Media.objects.create(
                post=post,
                **media_data,
            )

        return post
