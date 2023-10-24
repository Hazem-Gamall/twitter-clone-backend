from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework_nested.routers import NestedSimpleRouter

router = routers.SimpleRouter()
router.register(r"users", views.UserViewSet)

posts_router = NestedSimpleRouter(router, r"users", lookup="posts")
posts_router.register(r"posts", views.UserPostsViewset, basename="user-posts")

urlpatterns = [path(r"", include(router.urls)), path(r"", include(posts_router.urls))]
