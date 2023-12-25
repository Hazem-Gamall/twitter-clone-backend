from django.urls import path
from .views import ChatSSEAPIView

urlpatterns = [path("chats/sse/", ChatSSEAPIView.as_view())]
