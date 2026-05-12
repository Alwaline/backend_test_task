from django.http import JsonResponse
from rest_framework import status
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from users.models import User, TokenBlacklist
from utils.jwt_utils import decode_token

EXEMPT_URLS = [
    "/",
    "/api/v1/auth/login/",
    "/api/v1/auth/register/",
    "/api/v1/docs/",
    "/api/v1/schema/",
]

class JWTAuthenticationMiddleware(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        if not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]

        if TokenBlacklist.objects.filter(token=token).exists():
            raise AuthenticationFailed("Token is discard")

        user_id = decode_token(token)
        if not user_id:
            return JsonResponse({"error": "Token is invalid"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({"error": "User does not exist"}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return JsonResponse({"error": "User is inactive"}, status=status.HTTP_401_UNAUTHORIZED)
        request.user = user


        return user, token

    def authenticate_header(self, request):
        return "Bearer"