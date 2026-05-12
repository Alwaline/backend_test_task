from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from utils.jwt_utils import create_token
from .serializers import (RegisterUserSerializer, LoginUserSerializer)


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token = create_token(user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)