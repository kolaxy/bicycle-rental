from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView,
)
from .views import UserRegistrationView, me, UserUpdateView

urlpatterns = [
    path(
        "token/",
        TokenObtainPairView.as_view(),
        name="token-obtain-pair",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token-refresh",
    ),
    path(
        "register/", UserRegistrationView.as_view(), name="user-registration"
    ),
    path("me/", me, name="user-me"),
    path("update/", UserUpdateView.as_view(), name="user-update"),
]
