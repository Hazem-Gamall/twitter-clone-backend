from rest_framework import serializers
from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    model = UserProfile