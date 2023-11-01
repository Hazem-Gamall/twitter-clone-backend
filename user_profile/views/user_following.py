from rest_framework.response import Response
from rest_framework import viewsets, exceptions
from user_profile.models import UserProfile, UserFollowing
from user_profile.permissions import IsOwner
from posts.serializers import PostSerializer
from rest_framework import status
from rest_framework.decorators import action
from posts.models import Post
from user_profile.serializers import UserProfileSerializer, UserFollowingSerializer
from user_profile.models import UserProfile
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist


class UserFollowingViewSet(viewsets.GenericViewSet):
    queryset = UserProfile.objects.all()
    permission_classes = [IsOwner]

    def list(self, request, following_user__username):
        username = following_user__username
        try:
            resource_user = self.queryset.get(user__username=username)
            following = self.paginate_queryset(resource_user.following.all())
            return Response(UserFollowingSerializer(following, many=True).data)
        except ObjectDoesNotExist:
            raise exceptions.ValidationError(
                {"username": "The username provided did not match any know users."}
            )

    def create(self, request, following_user__username):
        username = following_user__username
        resource_user = self.queryset.get(user__username=username)
        # self.check_object_permissions(request, resource_user)
        if "username" not in request.data:
            raise exceptions.ValidationError({"username": "Required field"})
        username_to_follow = request.data["username"]
        try:
            user_to_follow = self.queryset.get(user__username=username_to_follow)
            UserFollowing.objects.create(
                user_profile=user_to_follow, following_user_profile=resource_user
            )
        except ObjectDoesNotExist:
            raise exceptions.ValidationError(
                {"username": "The username provided did not match any know users."}
            )

        except IntegrityError:
            raise exceptions.ValidationError(
                "You already follow the user with the username provided."
            )

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=["DELETE"],
        detail=False,
        url_path=r"(?P<unfollow_username>[^/.]+)",
    )
    def unfollow(self, request, following_user__username, unfollow_username):
        username = following_user__username
        try:
            resource_user = self.queryset.get(user__username=username)
            user_to_unfollow = self.queryset.get(user__username=unfollow_username)

            resource_user.following.get(user_profile=user_to_unfollow).delete()
        except ObjectDoesNotExist as e:
            raise exceptions.ValidationError(e)

        return Response(status=status.HTTP_204_NO_CONTENT)
