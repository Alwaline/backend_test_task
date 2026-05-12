from rest_framework.permissions import BasePermission

from roles.models import BusinessElement, AccessRoleRule


def HasPermission(element_name, action):
    class Permission(BasePermission):
        def has_permission(self, request, view):
            user = request.user

            if not user or not hasattr(user, 'role') or user.role is None:
                return False

            if not user.is_authenticated:
                return False

            try:
                element = BusinessElement.objects.get(name=element_name)
                rule = AccessRoleRule.objects.get(role=user.role, element=element)
            except (BusinessElement.DoesNotExist, AccessRoleRule.DoesNotExist):
                return False

            return getattr(rule, action, False)

    return Permission
