from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token
from user_profile.serializers import UserProfileSerializer


class TokenObtainPairSerializerWithUsername(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user) -> Token:
        token = super().get_token(user)
        del token["user_id"]
        token["username"] = user.username
        return token
