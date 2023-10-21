from typing import Optional, Tuple
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import Token


# class HttpOnlyJWTAuthentication(JWTAuthentication):
#     def authenticate(self, request: Request):
#         cookie = request.COOKIES.get("refreshToken")
#         return super().authenticate(request)
