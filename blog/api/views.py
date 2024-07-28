from django.db.models import Q
from rest_framework import status
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

    @action(detail=True, methods=SAFE_METHODS, permission_classes=[IsAuthenticated])
    def info(self, request, pk=None):
        data = self.serializer_class(self.get_object()).data
        return Response(data)

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

    @action(
        detail=False, methods=SAFE_METHODS, permission_classes=[IsAuthenticated]
    )  # todo : test this function
    def followings(self, request):
        profile = request.user.profile
        followingsIds = [i for i in profile.following.all()]
        self.queryset = Post.objects.filter(author_id__in=followingsIds)
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    @action(
        detail=False,
        url_path="user/(?P<user_id>\d+)",
        methods=SAFE_METHODS,
        permission_classes=[IsAuthenticated],
    )
    def user_posts(self, request, user_id=None):
        posts = Post.objects.filter(author_id=user_id)
        serializer = self.serializer_class(posts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=SAFE_METHODS, permission_classes=[IsAuthenticated])
    def liked(self, request):
        liked_posts = Post.objects.filter(likes=request.user)
        serializer = self.serializer_class(liked_posts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=SAFE_METHODS, permission_classes=[IsAuthenticated])
    def saved(self, request):
        saved_posts = Post.objects.filter(saves=request.user)
        serializer = self.serializer_class(saved_posts, many=True)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=SAFE_METHODS,
        url_path="search",
        permission_classes=[IsAuthenticated],
    )
    def search(self, request):
        query = request.query_params.get("q", None)
        if not query:
            return Response(
                {"detail": "Please provide a search query."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        search_results = Post.objects.filter(
            Q(title__icontains=query) | Q(author__username__icontains=query)
        )
        serializer = self.serializer_class(search_results, many=True)
        return Response(serializer.data)


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
