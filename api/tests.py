from django.test import TestCase
from rest_framework.test import APIClient

from roles.models import Role, AccessRoleRule, BusinessElement
from users.models import User


class BaseTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.defaults["SERVER_NAME"] = "localhost"
        # создаём роли
        self.admin_role = Role.objects.create(name=Role.RoleName.ADMIN)
        self.user_role = Role.objects.create(name=Role.RoleName.USER)

        # создаём бизнес-элемент
        self.orders_element = BusinessElement.objects.create(name="orders")

        # создаём правила доступа
        AccessRoleRule.objects.create(
            role=self.user_role,
            element=self.orders_element,
            read=True, read_all=False,
            create=True,
            update=True, update_all=False,
            delete=True, delete_all=False,
        )
        AccessRoleRule.objects.create(
            role=self.admin_role,
            element=self.orders_element,
            read=True, read_all=True,
            create=True,
            update=True, update_all=True,
            delete=True, delete_all=True,
        )

        # создаём пользователей
        self.admin = User.objects.create_user(
            email="admin@test.com",
            password="admin123",
            first_name="Admin",
            last_name="Admin",
            role=self.admin_role,
        )
        self.user = User.objects.create_user(
            email="user@test.com",
            password="user123",
            first_name="User",
            last_name="User",
            role=self.user_role,
        )

    def auth(self, email, password):
        response = self.client.post("/api/v1/auth/login/", {
            "email": email,
            "password": password,
        })
        token = response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")


class AuthTests(BaseTestCase):
    def test_register(self):
        response = self.client.post("/api/v1/auth/register/", {
            "email": "new@test.com",
            "password1": "newpass123",
            "password2": "newpass123",
            "first_name": "New",
            "last_name": "User",
        })
        self.assertEqual(response.status_code, 201)

    def test_register_passwords_mismatch(self):
        response = self.client.post("/api/v1/auth/register/", {
            "email": "new@test.com",
            "password1": "newpass123",
            "password2": "wrongpass",
            "first_name": "New",
            "last_name": "User",
        })
        self.assertEqual(response.status_code, 400)

    def test_login(self):
        response = self.client.post("/api/v1/auth/login/", {
            "email": "user@test.com",
            "password": "user123",
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.data)

    def test_login_wrong_password(self):
        response = self.client.post("/api/v1/auth/login/", {
            "email": "user@test.com",
            "password": "wrongpass",
        })
        self.assertEqual(response.status_code, 400)

    def test_login_nonexistent_user(self):
        response = self.client.post("/api/v1/auth/login/", {
            "email": "nobody@test.com",
            "password": "pass123",
        })
        self.assertEqual(response.status_code, 400)


class OrderTests(BaseTestCase):
    def test_get_orders_unauthorized(self):
        response = self.client.get("/api/v1/orders/")
        self.assertEqual(response.status_code, 401)

    def test_get_orders_as_user(self):
        self.auth("user@test.com", "user123")
        response = self.client.get("/api/v1/orders/")
        self.assertEqual(response.status_code, 403)

    def test_get_orders_as_admin(self):
        self.auth("admin@test.com", "admin123")
        response = self.client.get("/api/v1/orders/")
        self.assertEqual(response.status_code, 200)

    def test_create_order(self):
        self.auth("user@test.com", "user123")
        response = self.client.post("/api/v1/orders/", {"name": "Test Order"})
        self.assertEqual(response.status_code, 201)


class RoleTests(BaseTestCase):
    def test_get_roles_as_admin(self):
        self.auth("admin@test.com", "admin123")
        response = self.client.get("/api/v1/admin/roles/")
        self.assertEqual(response.status_code, 200)

    def test_get_roles_as_user(self):
        self.auth("user@test.com", "user123")
        response = self.client.get("/api/v1/admin/roles/")
        self.assertEqual(response.status_code, 403)

    def test_create_role_as_admin(self):
        self.auth("admin@test.com", "admin123")
        response = self.client.post("/api/v1/admin/roles/", {"name": "manager"})
        self.assertEqual(response.status_code, 201)
