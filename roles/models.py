from django.db import models

class Role(models.Model):
    class RoleName(models.TextChoices):
        ADMIN = "admin", "Администратор"
        MANAGER = "manager", "Менеджер"
        USER = "user", "Пользователь"
        GUEST = "guest", "Гость"

    name = models.CharField(
        "Роль",
        max_length=100,
        unique=True,
        choices=RoleName.choices,
    )

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"

    def __str__(self):
        return self.name