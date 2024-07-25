from django.contrib.auth.models import User
from rest_framework import serializers

from users.models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name"]
        read_only_fields = ["id", "username", "first_name", "last_name"]


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "following",
            "friends",
            "bio",
            "date_of_birth",
            "image",
        )
