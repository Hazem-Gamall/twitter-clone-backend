from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from .serializers import PostSerializer, UpdatePostSerializer
from .models import Post
from rest_framework import permissions, status, response, exceptions
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser

# Create your views here.


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return UpdatePostSerializer
        return PostSerializer

    @action(methods=["GET"], detail=False)
    def search(self, request):
        query = request.query_params.get("q")
        posts = self.paginate_queryset(
            self.queryset.filter(text__icontains=query).order_by("-creation")
        )
        return response.Response(self.get_serializer(posts, many=True).data)


class PostRepliesViewSet(viewsets.ViewSet):
    queryset = Post.objects.all()

    def list(self, request, post_pk):
        try:
            post = self.queryset.get(id=post_pk)
        except:
            raise exceptions.ValidationError(
                {"post": "The id provided does not match any known post"}
            )
        print(post.replies.all())
        serialized_replies = PostSerializer(post.replies.all(), many=True).data
        return response.Response(serialized_replies)
