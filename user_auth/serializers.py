from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken
from user_profile.serializers import UserProfileSerializer


class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None

    def validate(self, attrs):
        attrs["refresh"] = self.context["request"].COOKIES.get("refresh_token")
        if attrs["refresh"]:
            return super().validate(attrs)
        else:
            raise InvalidToken("No valid token found in cookie 'refresh_token'")
