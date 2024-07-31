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
    followers = serializers.SerializerMethodField(read_only=True)

    def get_followers(self, obj):
        followers = User.objects.filter(profile__following=obj.user)
        serializer = UserSerializer(followers, many=True)
        return serializer.data

    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "following",
            "followers",
            "friends",
            "bio",
            "date_of_birth",
            "image",
        )


class FollowSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
