from django.urls import path

from api.views import (RegisterView, LoginView, OrdersListView, OrderDetailView, UserListView, UserDetailView)

urlpatterns = [
    path("auth/register/", RegisterView.as_view()),
    path("auth/login/", LoginView.as_view()),
    path("users/", UserListView.as_view()),
    path("users/<int:pk>/", UserDetailView.as_view()),
    path("orders/", OrdersListView.as_view()),  # можно добавить и users/<int:pk>/orders
    path("orders/<int:pk>/", OrderDetailView.as_view()),
]
