from rest_framework.views import APIView
from chat.models import Chat
from main.permissions import IsOwner
from sse.renderers import ServerSentEventRenderer
from .generators import ChatGenerator
from django.http.response import StreamingHttpResponse


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
