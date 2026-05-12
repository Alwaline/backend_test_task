from django.core.management.base import BaseCommand
from users.models import User
from roles.models import Role

class Command(BaseCommand):
    help = "create admin user"

    def handle(self, *args, **options):
        email = input("Email: ")
        password = input("Password: ")
        first_name = input("First Name: ")
        last_name = input("Last Name: ")

        admin_role, _ = Role.objects.get_or_create(name="Admin")

        user = User.objects.create_user(
            email,
            password,
            first_name=first_name,
            last_name=last_name,
            role=admin_role,
        )

        self.stdout.write(self.style.SUCCESS(f"Created user: {user.email}"))
