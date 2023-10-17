from django.shortcuts import render, HttpResponse
from rest_framework import viewsets
from .serializers import UserSerializer
from .models import UserProfile


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = UserProfile.objects.all()
