from rest_framework import viewsets
from django.db.models import Q
from rest_framework.response import Response
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

    @action(methods=["GET"], detail=False)
    def search(self, request):
        query = request.query_params.get("q")

        users = self.queryset.filter(
            Q(user__username__icontains=query) | Q(user__first_name__icontains=query)
        )
        users = self.paginate_queryset(users)

        return Response(self.get_serializer(users, many=True).data)
