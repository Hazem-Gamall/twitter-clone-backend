from rest_framework.views import APIView
from chat.models import Chat, Message
from main.permissions import IsOwner
from chat.permissions import IsMessageReceiver
from sse.renderers import ServerSentEventRenderer
from .generators import ChatGenerator
from django.http.response import StreamingHttpResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status


class MessageSeenAPIView(APIView):
    queryset = Message.objects.all()
    permission_classes = [IsMessageReceiver]

    def get(self, request, pk):
        try:
            message = self.queryset.get(id=pk)
            self.check_object_permissions(request, message)
            message.seen = True
            message.save()
        except ObjectDoesNotExist:
            raise ValidationError("No message exists with the given pk")

        return Response(status=status.HTTP_200_OK)


class ChatSSEAPIView(APIView):
    queryset = Chat.objects.all()
    permission_classes = [IsOwner]
    renderer_classes = [ServerSentEventRenderer]

    def get(self, request):
        generator = ChatGenerator(request).get_generator()
        response = StreamingHttpResponse(generator, content_type="text/event-stream")
        response["X-Accel-Buffering"] = "no"  # Disable buffering in nginx
        response["Cache-Control"] = "no-cache"  # Ensure clients don't cache the data
        return response
