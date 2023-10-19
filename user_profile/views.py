from django.shortcuts import render, HttpResponse
from rest_framework import viewsets, mixins

from user_profile.permissions import IsAuthenticatedOrCreateOrOptions
from .serializers import UserRegistirationSerializer, UserSerializer
from .models import UserProfile
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrCreateOrOptions]
    queryset = UserProfile.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return UserRegistirationSerializer
        return UserSerializer
