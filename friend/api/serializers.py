from django.contrib.auth.models import User
from rest_framework import serializers

from friend.models import FriendRequest


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name"]
        read_only_fields = ["id", "username", "first_name", "last_name"]


class FriendRequestSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    sender = serializers.StringRelatedField(read_only=True)
    receiver = serializers.StringRelatedField()
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ["id", "sender", "receiver", "is_active", "timestamp"]
