from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from . import views

urlpatterns = [
    path("token/", views.HTTPOnlyTokenObtainPairView.as_view()),
    path("token/refresh/", views.CookieTokenRefreshView.as_view()),
]
