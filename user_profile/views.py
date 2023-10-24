from rest_framework.response import Response
from rest_framework import viewsets, exceptions
from user_profile.models import UserProfile
from rest_framework.decorators import action
from user_profile.permissions import IsAuthenticatedOrCreateOrOptions, IsOwner
from .serializers import UserProfileSerializer
from posts.serializers import PostSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import status
from posts.models import Post


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrCreateOrOptions]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    lookup_field = "user__username"


class UserPostsViewset(viewsets.ViewSet):
    permission_classes = [IsOwner]
    queryset = UserProfile.objects.all()

    def list(self, request, posts_user__username):
        username = posts_user__username

        posts = (
            self.queryset.get(user__username=username).posts.all().order_by("-creation")
        )
        serialized_posts = PostSerializer(posts, many=True).data
        return Response(serialized_posts)

    def create(self, request, posts_user__username):
        print(request.data)
        username = posts_user__username
        user_posts = self.queryset.get(user__username=username).posts
        data = {**request.data, "username": username}
        serialized_post = PostSerializer(data=data)
        if serialized_post.is_valid():
            saved_post = serialized_post.save()
            user_posts.add(saved_post)
        else:
            return Response(serialized_post.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(PostSerializer(saved_post).data)

    @action(methods=["GET"], detail=False)
    def liked_posts(self, request, posts_user__username):
        username = posts_user__username
        liked_posts = self.queryset.get(user__username=username).liked_posts.all()
        serialized_liked_posts = PostSerializer(liked_posts, many=True).data
        return Response(serialized_liked_posts)

    @liked_posts.mapping.post
    def like_post(self, request, posts_user__username):
        if "post" not in request.data:
            raise exceptions.ValidationError({"post": "required field"})
        username = posts_user__username
        try:
            post = Post.objects.get(id=request.data.pop("post"))
        except:
            return Response(
                {"post": "the post id provided doesn't exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        print(post)
        self.queryset.get(user__username=username).liked_posts.add(post)

        return Response(PostSerializer(post).data)
