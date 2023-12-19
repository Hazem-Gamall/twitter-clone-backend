from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from notifications.models import Notification
from main.permissions import IsOwner
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError
from .sse_renderer import ServerSentEventRenderer
from rest_framework.renderers import JSONRenderer
from django.http import StreamingHttpResponse
from .redis_generator import listen_to_channel


# Create your views here.
class NotificationsAPIView(APIView):
    queryset = Notification.objects.all()
    permission_classes = [IsOwner]

    def get(self, request, pk):
        try:
            notification = self.queryset.get(id=pk)
            self.check_object_permissions(request, notification)
            notification.viewed = True
            notification.save()
        except ObjectDoesNotExist:
            raise ValidationError("No notification exists with the given pk")

        return Response(status=status.HTTP_200_OK)


class NotificationSSEAPIView(APIView):
    queryset = Notification.objects.all()
    permission_classes = [IsOwner]
    renderer_classes = [ServerSentEventRenderer]
    authentication_classes = []

    def get(self, request):
        generator = listen_to_channel(
            lambda user_id, message: message["receiver"]["user"]["id"] == user_id,
            request.user.id,
        )
        response = StreamingHttpResponse(generator, content_type="text/event-stream")
        response["X-Accel-Buffering"] = "no"  # Disable buffering in nginx
        response["Cache-Control"] = "no-cache"  # Ensure clients don't cache the data
        return response
