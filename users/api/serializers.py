from django.contrib.auth.models import User
from rest_framework import serializers

from users.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = Profile
        fields = (
            "id",
            "user_id",
            "following",
            "friends",
            "bio",
            "date_of_birth",
            "image",
        )
