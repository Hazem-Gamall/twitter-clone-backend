from rest_framework.response import Response
from rest_framework import viewsets, exceptions
from user_profile.models import UserProfile
from user_profile.permissions import IsOwner
from user_profile.serializers import UserFollowersSerializer
from rest_framework import status
from user_profile.models import UserProfile


class UserFollowersViewSet(viewsets.GenericViewSet):
    queryset = UserProfile.objects.all()

    def list(self, request, followers_user__username):
        username = followers_user__username
        followers = self.paginate_queryset(
            self.queryset.get(user__username=username).followers.all()
        )
        return Response(
            UserFollowersSerializer(
                followers,
                many=True,
            ).data
        )
