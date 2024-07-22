from rest_framework_nested import routers

from .api import views

router = routers.DefaultRouter()
router.register("profiles", views.ProfileViewSet)

urlpatterns = router.urls
