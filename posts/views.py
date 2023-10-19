from django.shortcuts import render
from rest_framework import viewsets
from .serializers import PostSerializer, UpdatePostSerializer
from .models import Post
from rest_framework import permissions

# Create your views here.


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return UpdatePostSerializer
        return PostSerializer
