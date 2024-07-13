from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "password", "email", "name")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        # Hash the password before saving
        validated_data["password"] = make_password(validated_data.get("password"))
        return super(UserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        # Hash the password before saving
        validated_data["password"] = make_password(validated_data.get("password"))
        return super(UserSerializer, self).update(instance, validated_data)