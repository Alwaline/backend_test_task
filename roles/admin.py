from django.contrib import admin

from .models import Role, AccessRoleRule

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    pass

@admin.register(AccessRoleRule)
class AccessRoleRuleAdmin(admin.ModelAdmin):
    pass
