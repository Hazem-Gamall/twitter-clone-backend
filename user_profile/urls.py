from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"user", views.UserRegisterationViewSet, basename="user")
urlpatterns = [path("", include(router.urls))]
