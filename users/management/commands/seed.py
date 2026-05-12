from django.core.management.base import BaseCommand
from users.models import User
from roles.models import Role, AccessRoleRule, BusinessElement


class Command(BaseCommand):
    help = "Заполнить БД тестовыми данными"

    def handle(self, *args, **kwargs):
        # Роли
        admin_role,   _ = Role.objects.get_or_create(name=Role.RoleName.ADMIN)
        manager_role, _ = Role.objects.get_or_create(name=Role.RoleName.MANAGER)
        user_role,    _ = Role.objects.get_or_create(name=Role.RoleName.USER)
        guest_role,   _ = Role.objects.get_or_create(name=Role.RoleName.GUEST)
        self.stdout.write("Роли созданы")

        # Бизнес-элементы
        orders_el,  _ = BusinessElement.objects.get_or_create(name="orders")
        users_el,   _ = BusinessElement.objects.get_or_create(name="users")
        roles_el,   _ = BusinessElement.objects.get_or_create(name="roles")
        self.stdout.write("Бизнес-элементы созданы")

        # Правила доступа — админ
        for element in [orders_el, users_el, roles_el]:
            AccessRoleRule.objects.get_or_create(
                role=admin_role, element=element,
                defaults=dict(
                    read=True, read_all=True,
                    create=True,
                    update=True, update_all=True,
                    delete=True, delete_all=True,
                )
            )

        # Правила доступа — менеджер
        AccessRoleRule.objects.get_or_create(
            role=manager_role, element=orders_el,
            defaults=dict(
                read=True, read_all=True,
                create=True,
                update=True, update_all=True,
                delete=False, delete_all=False,
            )
        )
        AccessRoleRule.objects.get_or_create(
            role=manager_role, element=users_el,
            defaults=dict(
                read=True, read_all=True,
                create=False,
                update=False, update_all=False,
                delete=False, delete_all=False,
            )
        )

        # Правила доступа — пользователь
        AccessRoleRule.objects.get_or_create(
            role=user_role, element=orders_el,
            defaults=dict(
                read=True, read_all=False,
                create=True,
                update=True, update_all=False,
                delete=True, delete_all=False,
            )
        )

        # Правила доступа — гость
        AccessRoleRule.objects.get_or_create(
            role=guest_role, element=orders_el,
            defaults=dict(
                read=True, read_all=False,
                create=False,
                update=False, update_all=False,
                delete=False, delete_all=False,
            )
        )
        self.stdout.write("Правила доступа созданы")

        # Тестовые пользователи
        if not User.objects.filter(email="admin@example.com").exists():
            User.objects.create_user(
                email="admin@example.com",
                password="admin123",
                first_name="Админ",
                last_name="Админов",
                role=admin_role,
            )

        if not User.objects.filter(email="manager@example.com").exists():
            User.objects.create_user(
                email="manager@example.com",
                password="manager123",
                first_name="Менеджер",
                last_name="Менеджеров",
                role=manager_role,
            )

        if not User.objects.filter(email="user@example.com").exists():
            User.objects.create_user(
                email="user@example.com",
                password="user123",
                first_name="Пользователь",
                last_name="Пользователев",
                role=user_role,
            )

        self.stdout.write(self.style.SUCCESS("Готово! Тестовые данные загружены."))