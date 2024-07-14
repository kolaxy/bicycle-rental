from django.contrib.auth import get_user_model
from rest_framework import permissions
from users.models import User

User = get_user_model()


class IsRentalOwnerOrSuperuser(permissions.BasePermission):
    """
    The user is the owner of the rental or superuser.
    """

    def has_object_permission(self, request, view, obj):
        return obj.renter == request.user or request.user.is_superuser

