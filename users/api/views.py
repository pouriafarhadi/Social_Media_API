from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.api.serializers import ProfileSerializer, UserSerializer, FollowSerializer
from users.models import Profile


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=["GET", "PUT"], permission_classes=[IsAuthenticated])
    def me(self, request):
        (myprofile, create) = Profile.objects.get_or_create(user_id=request.user.id)
        if request.method == "GET":
            serialized = ProfileSerializer(myprofile)
            return Response(serialized.data)
        elif request.method == "PUT":
            serializer = ProfileSerializer(instance=myprofile, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    @action(detail=False, methods=["GET"], permission_classes=[IsAuthenticated])
    def followings(self, request):
        profile = self.request.user.profile
        following_profiles = profile.following.all()
        serializer = UserSerializer(following_profiles, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"], permission_classes=[IsAuthenticated])
    def followers(self, request):
        user = self.request.user
        followers = User.objects.filter(profile__following=user)
        serializer = UserSerializer(followers, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["POST"], permission_classes=[IsAuthenticated])
    def follow(self, request):
        serializer = FollowSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user_to_follow = User.objects.get(
                    pk=serializer.validated_data["user_id"]
                )
                profile = self.request.user.profile
                profile.following.add(user_to_follow)
                profile.save()
                return Response(
                    {"status": f"Following {user_to_follow.username}"},
                    status=status.HTTP_200_OK,
                )
            except User.DoesNotExist:
                return Response(
                    {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def unfollow(self, request):
        serializer = FollowSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user_to_unfollow = User.objects.get(
                    pk=serializer.validated_data["user_id"]
                )
                profile = self.request.user.profile
                if user_to_unfollow in profile.following.all():
                    profile.following.remove(user_to_unfollow)
                    return Response(
                        {"status": f"Unfollowed {user_to_unfollow.username}"},
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"error": "You are not following this user"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            except User.DoesNotExist:
                return Response(
                    {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
