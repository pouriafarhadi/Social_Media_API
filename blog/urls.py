from rest_framework_nested import routers

from .api import views

router = routers.DefaultRouter()
router.register("posts", views.PostViewSet, basename="posts")
posts_routs = routers.NestedDefaultRouter(router, r"posts", lookup="post")
posts_routs.register("comments", views.CommentViewSet, basename="post-comments")
urlpatterns = router.urls + posts_routs.urls
