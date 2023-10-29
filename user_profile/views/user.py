from rest_framework import viewsets
from user_profile.models import UserProfile
from user_profile.permissions import IsAuthenticatedOrCreateOrOptions
from user_profile.serializers import UserProfileSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.decorators import action


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrCreateOrOptions]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    lookup_field = "user__username"
