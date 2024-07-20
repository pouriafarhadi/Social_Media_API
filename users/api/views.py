from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from users.models import Profile
from users.api.serializers import ProfileSerializer


class ProfileViewSet(
    CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet
):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
