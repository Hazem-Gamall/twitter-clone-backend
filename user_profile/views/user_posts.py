from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from user_profile.models import UserProfile
from user_profile.permissions import IsOwner
from posts.serializers import PostSerializer, MediaSerialzer, CreatePostSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from main.settings import DEBUG


class UserPostsViewSet(viewsets.GenericViewSet):
    permission_classes = [IsOwner]
    queryset = UserProfile.objects.all()
    parser_classes = [FormParser, MultiPartParser, JSONParser]
    serializer_class = PostSerializer

    def list(self, request, posts_user__username):
        username = posts_user__username

        if (
            "with_replies" in request.query_params
            and request.query_params["with_replies"] == "true"
        ):
            posts = (
                self.queryset.get(user__username=username)
                .posts.all()
                .order_by("-creation")
            )
        else:
            posts = (
                self.queryset.get(user__username=username)
                .posts.filter(reply_to__isnull=True)
                .order_by("-creation")
            )
        posts = self.paginate_queryset(posts)
        serialized_posts = self.get_serializer(
            posts,
            many=True,
        ).data
        return Response(serialized_posts)

    def create(self, request, posts_user__username):
        request_data = request.data

        print(request_data)

        username = posts_user__username
        user_posts = self.queryset.get(user__username=username).posts
        media_data = None
        print("media" in request_data)
        if "reply_to" in request_data:
            print("reply_to dict", request_data["reply_to"])
        if "media" in request_data:
            media_data = request_data.pop("media")
            print(media_data)

        post_data = {**request_data, "username": username}
        serialized_post = CreatePostSerializer(data=post_data)
        if serialized_post.is_valid():
            saved_post = serialized_post.save()
            user_posts.add(saved_post)
        else:
            return Response(serialized_post.errors, status=status.HTTP_400_BAD_REQUEST)
        if media_data:
            deserialized_media = MediaSerialzer(
                data={"file": media_data, "post": saved_post.id}
            )
            if deserialized_media.is_valid():
                saved_media = deserialized_media.save()
                print("des med", saved_media)
            else:
                return Response(
                    deserialized_media.errors, status=status.HTTP_400_BAD_REQUEST
                )
        return Response(self.get_serializer(saved_post).data)

    @action(methods=["GET"], detail=False, permission_classes=[IsOwner])
    def timeline(self, request, posts_user__username):
        username = posts_user__username
        try:
            resource_user = self.queryset.get(user__username=username)
            if not DEBUG:
                self.check_object_permissions(request, resource_user)
            timeline_posts = []
            for following in resource_user.following.all():
                timeline_posts += list(following.user_profile.posts.all())
            timeline_posts = self.paginate_queryset(timeline_posts)

            return Response(self.get_serializer(timeline_posts, many=True).data)
        except ObjectDoesNotExist:
            raise ValidationError({"username": {"Does not match any known users."}})
