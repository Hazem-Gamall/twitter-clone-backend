from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView


# Create your views here.
class HttpOnlyTokenObtainPairView(TokenObtainPairView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        response = super().post(request, *args, **kwargs)
        token = response.data["refresh"]
        del response.data["refresh"]
        response.set_cookie("refreshToken", token, httponly=True)
        return response
