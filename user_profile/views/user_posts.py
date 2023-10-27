from rest_framework.response import Response
from rest_framework import viewsets
from user_profile.models import UserProfile
from user_profile.permissions import IsOwner
from posts.serializers import PostSerializer, MediaSerialzer, CreatePostSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import status


class UserPostsViewSet(viewsets.ViewSet):
    permission_classes = [IsOwner]
    queryset = UserProfile.objects.all()
    parser_classes = [FormParser, MultiPartParser, JSONParser]

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
        serialized_posts = PostSerializer(
            posts, many=True, context={"user": request.user}
        ).data
        return Response(serialized_posts)

    def create(self, request, posts_user__username):
        request_data = request.data.dict()

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
        return Response(PostSerializer(saved_post).data)
