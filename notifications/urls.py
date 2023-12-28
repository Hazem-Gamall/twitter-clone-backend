from django.urls import path
from .views import NotificationsAPIView, NotificationSSEAPIView

urlpatterns = [
    path("notifications/<int:pk>/viewed/", NotificationsAPIView.as_view()),
    path("notifications/sse/", NotificationSSEAPIView.as_view()),
]
