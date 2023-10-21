from django.shortcuts import render, HttpResponse
from rest_framework import viewsets, mixins
from user_profile.models import UserProfile
from rest_framework.decorators import action
from user_profile.permissions import IsAuthenticatedOrCreateOrOptions
from .serializers import UserProfileSerializer


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrCreateOrOptions]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = "user__username"
