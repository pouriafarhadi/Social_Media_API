from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.api.serializers import ProfileSerializer
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
