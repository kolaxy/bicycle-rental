from django.urls import path
from .views import UserRegistrationView, me

urlpatterns = [
    path(
        "register/", UserRegistrationView.as_view(), name="user-registration"
    ),
    path("me/", me, name="me"),
]
