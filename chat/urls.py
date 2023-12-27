from django.urls import path
from .views import ChatSSEAPIView, MessageSeenAPIView

urlpatterns = [
    path("chats/sse/", ChatSSEAPIView.as_view()),
    path("chats/messages/seen/<int:pk>/", MessageSeenAPIView.as_view()),
]
