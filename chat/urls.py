from django.urls import path
from .views import ChatSSEAPIView, MessageAPIView

urlpatterns = [
    path("chats/sse/", ChatSSEAPIView.as_view()),
    path("chats/messages/<int:pk>/", MessageAPIView.as_view()),
]
