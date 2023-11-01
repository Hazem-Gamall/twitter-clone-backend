from rest_framework.response import Response
from rest_framework import viewsets, exceptions
from user_profile.models import UserProfile
from user_profile.permissions import IsOwner
from posts.serializers import PostSerializer
from rest_framework import status
from posts.models import Post


class UserPostsLikesViewSet(viewsets.GenericViewSet):
    permission_classes = [IsOwner]
    queryset = UserProfile.objects.all()
    serializer_class = PostSerializer

    def list(self, request, likes_user__username):
        username = likes_user__username
        liked_posts = self.queryset.get(user__username=username).liked_posts.all()
        serialized_liked_posts = self.get_serializer(
            liked_posts,
            many=True,
        ).data
        return Response(serialized_liked_posts)

    def create(self, request, likes_user__username):
        if "post" not in request.data:
            raise exceptions.ValidationError({"post": "required field"})
        if "like" not in request.data:
            raise exceptions.ValidationError({"like": "required field"})

        username = likes_user__username

        try:
            post = Post.objects.get(id=request.data.pop("post"))
        except:
            return Response(
                {"post": "the post id provided doesn't exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if request.data["like"]:
            self.queryset.get(user__username=username).liked_posts.add(post)
        else:
            if post in self.queryset.get(user__username=username).liked_posts.all():
                self.queryset.get(user__username=username).liked_posts.remove(post)
        return Response(
            self.get_serializer(
                post,
            ).data
        )
