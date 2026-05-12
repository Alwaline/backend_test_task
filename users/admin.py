from django.contrib import admin

from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "patronymic")}),
        ("Permissions", {
            "fields": (
                "is_active",
                "role"
            ),
        }),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2"),
        }),
    )
    list_display = ("email", "first_name", "last_name", "is_active", "role")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)