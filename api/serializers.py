from rest_framework import serializers

from business_logic.models import Orders
from roles.models import Role, BusinessElement, AccessRoleRule
from users.models import User


class RegisterUserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "patronymic",
            "email",
            "password1",
            "password2",
        )

    def validate(self, data):
        if data.get("password") != data.get("password2"):
            raise serializers.ValidationError("Пароли не совпадают")
        return data

    def create(self, validated_data):
        password = validated_data.pop("password1")
        validated_data.pop("password2")
        return User.objects.create_user(password=password, **validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "patronymic",
            "email",
        )
        read_only_fields = ("is_active", "role")


class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):

        user = User.objects.filter(email=data["email"]).first()
        if not user:
            raise serializers.ValidationError("Пользователя с таким email не существует")
        if not user.check_password(data["password"]):
            raise serializers.ValidationError("Неверный логин или пароль")
        data["user"] = user
        return data


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ("id", "name", "owner")


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ("id", "name")
        read_only_fields = ("id",)


class BusinessElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessElement
        fields = ("id", "name")
        read_only_fields = ("id",)


class AccessRoleRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessRoleRule
        fields = (
            "id",
            "role",
            "element",
            "read",
            "read_all",
            "create",
            "update",
            "update_all",
            "delete",
            "delete_all",
        )
        read_only_fields = ("id",)
