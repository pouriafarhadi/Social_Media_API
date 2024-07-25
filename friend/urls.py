from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api import views

router = DefaultRouter()
router.register(r"friend_request", views.FriendRequestViewSet, basename="friendrequest")
router.register(r"friend_list", views.FriendListViewSet, basename="friendlist")
urlpatterns = [
    path("suggest_friend/", views.UsersListView.as_view(), name="suggest_friend"),
    path("", include(router.urls)),
]
