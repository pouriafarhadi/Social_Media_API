from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from friend.api.serializers import UserSerializer, FriendRequestSerializer
from friend.models import FriendRequest, FriendList


def getUserId(request):
    user_id = request.user.id
    return user_id


class UsersListView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = getUserId(self.request)
        a = User.objects.exclude(id=user_id)
        return a


class FriendRequestViewSet(viewsets.ModelViewSet):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PUT")

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PATCH")

    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed("DELETE")

    def get_queryset(self):
        user_id = self.request.user.id
        return FriendRequest.objects.filter(
            Q(sender_id=user_id) | Q(receiver_id=user_id), is_active=True
        )

    @action(detail=True, methods=["post"])
    def accept(self, request, pk=None):
        friend_request = self.get_object()
        if friend_request.receiver.id == getUserId(request):
            friend_request.accept()
            return Response({"status": "Friend request accepted"})
        return Response({"status": f"Friend request not found"})

    @action(detail=True, methods=["post"])
    def decline(self, request, pk=None):
        friend_request = self.get_object()
        if friend_request.receiver.id == getUserId(request):
            friend_request.decline()
            return Response({"status": "Friend request declined"})
        return Response({"status": f"Friend request not found"})

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        friend_request = self.get_object()
        if friend_request.sender.id == getUserId(request):
            friend_request.cancel()
            return Response({"status": f"Friend request {pk} cancelled"})
        return Response({"status": f"Friend request {pk} not found"})

    def create(self, request, *args, **kwargs):
        sender_id = self.request.user.id
        try:
            receiver_id = request.data["receiver_user_id"]
        except KeyError:
            return Response(
                "provide receiver_user_id in body", status=status.HTTP_400_BAD_REQUEST
            )
        if FriendRequest.objects.filter(
            sender_id=sender_id, receiver_id=receiver_id, is_active=True
        ).exists():
            return Response(
                {"status": "Friend request already sent"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if (
            self.request.user
            in FriendList.objects.get(user_id=receiver_id).friends.all()
        ):
            return Response("already friends", status=status.HTTP_400_BAD_REQUEST)
        FriendRequest.objects.create(sender_id=sender_id, receiver_id=receiver_id)
        return Response(
            {"status": "Friend request sent"}, status=status.HTTP_201_CREATED
        )


class FriendListViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed("POST")

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PUT")

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PATCH")

    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed("DELETE")

    def get_queryset(self):
        return FriendList.objects.get(user_id=getUserId(self.request)).friends.all()

    @action(detail=True, methods=["post"])
    def unfriend(self, request, pk=None):
        user_id = getUserId(request)
        obj = self.get_object()
        friendlistUser = FriendList.objects.get(user_id=user_id)
        if obj in friendlistUser.friends.all():
            friendlistUser.unfriend(obj)
            return Response("unfriended successfully", status=status.HTTP_200_OK)
        return Response({"status": f"Friend request not found"})
