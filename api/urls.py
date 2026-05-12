from django.urls import path, include
from rest_framework import routers

from api.views import (RegisterView, LoginView, OrdersListView, OrderDetailView, UserListView, UserDetailView,
                       RoleViewSet, BusinessElementViewSet, AccessRoleRuleViewSet, MeView)

router = routers.DefaultRouter()
router.register("roles", RoleViewSet, basename="roles")
router.register("elements", BusinessElementViewSet, basename="elements")
router.register("access-rules", AccessRoleRuleViewSet, basename="access-rules")

urlpatterns = [
    path("auth/register/", RegisterView.as_view()),
    path("auth/login/", LoginView.as_view()),
    path("users/", UserListView.as_view()),
    path("users/<int:pk>/", UserDetailView.as_view()),
    path("orders/", OrdersListView.as_view()),  # можно добавить и users/<int:pk>/orders
    path("orders/<int:pk>/", OrderDetailView.as_view()),
    path("users/<int:pk>/", UserListView.as_view()),
    path("admin/", include(router.urls)),
    path("auth/me/", MeView.as_view()),
]
