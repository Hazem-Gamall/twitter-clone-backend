from rest_framework.response import Response
from rest_framework import viewsets, exceptions
from user_profile.models import UserProfile
from main.permissions import IsOwner
from rest_framework.decorators import action
from notifications.serializers import NotificationsSerializer
from user_profile.models import UserProfile
from django.core.exceptions import ObjectDoesNotExist


class UserNotificationsViewSet(viewsets.GenericViewSet):
    queryset = UserProfile.objects.all()
    permission_classes = [IsOwner]
    serializer_class = NotificationsSerializer

    def list(self, request, notifications_user__username):
        username = notifications_user__username
        try:
            resource_user = self.queryset.get(user__username=username)
            notifications = self.paginate_queryset(resource_user.notifications.all())
            return Response(self.get_serializer(notifications, many=True).data)
        except ObjectDoesNotExist:
            raise exceptions.ValidationError(
                {"username": "The username provided did not match any know users."}
            )
