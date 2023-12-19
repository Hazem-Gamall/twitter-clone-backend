from django.urls import path
from .views import NotificationsAPIView

urlpatterns = [path("notifications/<int:pk>/viewed/", NotificationsAPIView.as_view())]
