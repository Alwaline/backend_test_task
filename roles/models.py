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


class BusinessElement(models.Model):
    name = models.CharField("Элемент", max_length=100, unique=True)

    class Meta:
        verbose_name = "Бизнес-элемент"
        verbose_name_plural = "Бизнес-элементы"

    def __str__(self):
        return self.name


class AccessRoleRule(models.Model):
    role = models.ForeignKey(
        "Role",
        on_delete=models.CASCADE,
        related_name="access_rule",
        blank=False,
        null=False,
        verbose_name="Роль"
    )
    element = models.ForeignKey("BusinessElement", on_delete=models.CASCADE)
    read = models.BooleanField("Чтение своего", default=False)
    read_all = models.BooleanField("Чтение всего", default=False)
    create = models.BooleanField("Создание", default=False)
    update = models.BooleanField("Изменение своего", default=False)
    update_all = models.BooleanField("Изменение всего", default=False)
    delete = models.BooleanField("Удаление своего", default=False)
    delete_all = models.BooleanField("Удаление всего", default=False)

    class Meta:
        verbose_name = "Правило доступа"
        verbose_name_plural = "Правила доступа"
        unique_together = ("role", "element")
