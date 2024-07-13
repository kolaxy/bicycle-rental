import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from users.managers import UserManager
from common.models import BaseModel


class User(AbstractUser, BaseModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    username = None
    first_name = None
    last_name = None
    name = models.CharField(
        max_length=99,
    )
    email = models.EmailField(max_length=99, unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email

    objects = UserManager()
