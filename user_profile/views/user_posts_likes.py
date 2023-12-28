from rest_framework.response import Response
from rest_framework import viewsets, exceptions
from user_profile.models import UserProfile
from main.permissions import IsOwner
from posts.serializers import PostSerializer
from rest_framework import status
from posts.models import Post
from django.core.exceptions import ObjectDoesNotExist


class UserPostsLikesViewSet(viewsets.GenericViewSet):
    permission_classes = [IsOwner]
    queryset = UserProfile.objects.all()
    serializer_class = PostSerializer

    def create(self, request, likes_user__username):
        if "post" not in request.data:
            raise exceptions.ValidationError({"post": "required field"})
        if "like" not in request.data:
            raise exceptions.ValidationError({"like": "required field"})

        username = likes_user__username

        try:
            post = Post.objects.get(id=request.data.pop("post"))
        except ObjectDoesNotExist:
            return Response(
                {"post": "the post id provided doesn't exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            resource_user = self.queryset.get(user__username=username)
            self.check_object_permissions(request, resource_user)
            if request.data["like"]:
                resource_user.liked_posts.add(post)
            else:
                if post in self.queryset.get(user__username=username).liked_posts.all():
                    resource_user.liked_posts.remove(post)
            return Response(
                self.get_serializer(
                    post,
                ).data
            )
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)
