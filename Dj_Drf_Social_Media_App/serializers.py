from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = (
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
        )


class CurrentUserSerializer(BaseUserSerializer):
    is_active = serializers.BooleanField(read_only=True)

    class Meta(BaseUserSerializer.Meta):
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "is_active",
            "email",
        )
