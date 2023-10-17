from django.shortcuts import render, HttpResponse
from rest_framework import viewsets
from .serializers import UserSerializer
from .models import UserProfile
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User


# Create your views here.
class UserRegisterationViewSet(
    viewsets.mixins.CreateModelMixin, viewsets.GenericViewSet
):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
