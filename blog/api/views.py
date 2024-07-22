from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from blog.api.permissions import IsPostAuthor
from blog.api.serializers import PostSerializer, CommentSerializer
from blog.models import Post, Comment


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated, IsPostAuthor]

    @action(detail=False, methods=SAFE_METHODS)
    def mine(self, request):
        self.queryset = Post.objects.filter(author=request.user)
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):  # to perform like and unlike functionality
        post = self.get_object()
        user = request.user
        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
            return Response({"detail": "Post unliked"})
        post.likes.add(user)
        return Response({"detail": "Post liked."})

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def save(self, request, pk=None):
        post = self.get_object()
        user = request.user
        if post.saves.filter(id=user.id).exists():
            post.saves.remove(user)
            return Response({"detail": "Post unsaved"})
        post.saves.add(user)
        return Response({"detail": "Post saved."})


class CommentViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_pk = self.kwargs.get("post_pk")
        if self.action == "list":
            return Comment.objects.filter(post_id=post_pk, reply__isnull=True)
        return Comment.objects.filter(post_id=post_pk)

    def get_object(self):
        queryset = self.get_queryset()
        obj = queryset.filter(pk=self.kwargs.get("pk")).first()
        if obj is None:
            raise NotFound("Comment not found")
        return obj

    def get_serializer_context(self):
        return {
            "post_id": self.kwargs["post_pk"],
            "request": self.request,
        }

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None, post_pk=None):
        comment = self.get_object()
        user = request.user
        if comment.likes.filter(id=user.id).exists():
            comment.likes.remove(user)
            return Response({"detail": "Comment unliked"})
        comment.likes.add(user)
        return Response({"detail": "Comment liked."})
