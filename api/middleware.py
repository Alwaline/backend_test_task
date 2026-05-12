from django.http import JsonResponse
from rest_framework import status

from users.models import User
from utils.jwt_utils import decode_token

EXEMPT_URLS = [
    "/auth/login/",
    "/auth/register/",
]

def authentication_middleware(get_response):
    def middleware(request):
        if request.path in EXEMPT_URLS:
            return get_response(request)

        auth_header = request.headers.get("token")
        if not auth_header.startswith("Bearer "):
            return JsonResponse({"error": "Token is missing"}, status=status.HTTP_400_BAD_REQUEST)

        token = auth_header.split(" ")[1]
        user_id = decode_token(token)["user_id"]
        if not user_id:
            return JsonResponse({"error": "Token is invalid"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({"error": "User does not exist"}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return JsonResponse({"error": "User is inactive"}, status=status.HTTP_401_UNAUTHORIZED)
        request.user = user

        response = get_response(request)

        return response
    return middleware