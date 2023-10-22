from rest_framework.response import Response
from rest_framework import viewsets, mixins
from user_profile.models import UserProfile
from rest_framework.decorators import action
from user_profile.permissions import IsAuthenticatedOrCreateOrOptions
from .serializers import UserProfileSerializer
from posts.serializers import PostSerializer


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrCreateOrOptions]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = "user__username"

    @action(["GET"], detail=False, url_path="(?P<user__username>[^/.]+)/posts")
    def posts(self, request, user__username):
        posts = self.queryset.get(user__username=user__username).posts.all()
        serialized_posts = PostSerializer(posts, many=True).data
        return Response(serialized_posts)
