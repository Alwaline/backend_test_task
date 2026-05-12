from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from business_logic.models import Orders
from roles.models import Role, AccessRoleRule, BusinessElement
from users.models import User
from utils.jwt_utils import create_token
from .permissions import HasPermission, IsAdminPermission
from .serializers import (RegisterUserSerializer, LoginUserSerializer, OrderSerializer, UserSerializer,
                          AccessRoleRuleSerializer, RoleSerializer, BusinessElementSerializer)


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
        return Response({"token": token}, status=status.HTTP_200_OK)


class UserListView(APIView):
    permission_classes = [HasPermission("users", "read_all")]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserDetailView(APIView):
    permission_classes = [HasPermission("users", "read")]

    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request, pk):
        user = User.objects.get(pk=pk)
        if request.user != user:
            perm = HasPermission("users", "update_all")().has_permission(request, self)
            if not perm:
                return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        user = User.objects.get(pk=pk)
        if request.user != user:
            perm = HasPermission("users", "delete_all")().has_permission(request, self)
            if not perm:
                return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        user.is_active = False
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrdersListView(APIView):
    permission_classes = [HasPermission("orders", "read_all")]

    def get(self, request):
        orders = Orders.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        perm = HasPermission("orders", "create")().has_permission(request, self)
        if not perm:
            return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        serializer = OrderSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderDetailView(APIView):
    permission_classes = [HasPermission("orders", "read")]

    def get_object(self, pk):
        try:
            return Orders.objects.get(pk=pk)
        except Orders.DoesNotExist:
            return None

    def get(self, request, pk):
        order = self.get_object(pk)
        if not order:
            return Response({"error": "Заказ не найден"}, status=status.HTTP_404_NOT_FOUND)

        if order.owner != request.user:
            perm = HasPermission("orders", "read_all")().has_permission(request, self)
            if not perm:
                return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        serializer = OrderSerializer(order)

        return Response(serializer.data)

    def patch(self, request, pk):
        order = self.get_object(pk)
        if not order:
            return Response({"error": "Заказ не найден"}, status=status.HTTP_404_NOT_FOUND)
        if order.owner != request.user:
            perm = HasPermission("orders", "update_all")().has_permission(request, self)
            if not perm:
                return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        serializer = OrderSerializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        order = self.get_object(pk)
        if not order:
            return Response({"error": "Заказ не найден"}, status=status.HTTP_404_NOT_FOUND)
        if order.owner != request.user:
            perm = HasPermission("orders", "delete_all")().has_permission(request, self)
            if not perm:
                return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RoleViewSet(IsAdminPermission, viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    def get_queryset(self):
        self.check(self.request)
        return super().get_queryset()


class BusinessElementViewSet(IsAdminPermission, viewsets.ModelViewSet):
    queryset = BusinessElement.objects.all()
    serializer_class = BusinessElementSerializer

    def get_queryset(self):
        self.check(self.request)
        return super().get_queryset()


class AccessRoleRuleViewSet(IsAdminPermission, viewsets.ModelViewSet):
    queryset = AccessRoleRule.objects.all()
    serializer_class = AccessRoleRuleSerializer

    def get_queryset(self):
        self.check(self.request)
        return super().get_queryset()
