from rest_framework.response import Response
from rest_framework import viewsets, exceptions
from user_profile.models import UserProfile
from main.permissions import IsOwner
from posts.serializers import PostSerializer
from rest_framework import status
from posts.models import Post
from django.core.exceptions import ObjectDoesNotExist


# TODO: generify
class UserPostsRepostsViewSet(viewsets.GenericViewSet):
    permission_classes = [IsOwner]
    queryset = UserProfile.objects.all()
    serializer_class = PostSerializer

    def list(self, request, repost_user__username):
        username = repost_user__username
        respoted_posts = self.queryset.get(user__username=username).posts.filter(
            repost=True
        )
        serialized_reposted_posts = self.get_serializer(respoted_posts, many=True).data
        return Response(serialized_reposted_posts)

    def create(self, request, repost_user__username):
        if "post" not in request.data:
            raise exceptions.ValidationError({"post": "required field"})

        username = repost_user__username

        try:
            incoming_post = Post.objects.get(id=request.data.pop("post"))
        except ObjectDoesNotExist:
            return Response(
                {"post": "the post id provided doesn't exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            resource_user = self.queryset.get(user__username=username)
            self.check_object_permissions(request, resource_user)

            if not resource_user.posts.filter(embed=incoming_post).exists():
                repost_post = Post.objects.create(
                    user=resource_user,
                    repost=True,
                    embed=incoming_post,
                )
                return Response(
                    self.get_serializer(
                        repost_post,
                    ).data
                )
            else:
                # TODO: ambigious behaviour, enacpsulate in its own endpoint
                resource_user.posts.filter(embed=incoming_post).delete(),

        except ObjectDoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)

        return Response(status=status.HTTP_200_OK)
