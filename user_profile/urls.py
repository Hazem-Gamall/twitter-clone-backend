from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework_nested.routers import NestedSimpleRouter

router = routers.SimpleRouter()
router.register(r"users", views.UserViewSet)

posts_router = NestedSimpleRouter(router, r"users", lookup="posts")
posts_router.register(r"posts", views.UserPostsViewSet, basename="user-posts")

likes_router = NestedSimpleRouter(router, r"users", lookup="likes")
likes_router.register(r"likes", views.UserLikesPostsViewSet, basename="user-likes")

repost_router = NestedSimpleRouter(router, r"users", lookup="repost")
repost_router.register(r"repost", views.UserRepostPostsViewSet, basename="user-repost")

urlpatterns = [
    path(r"", include(router.urls)),
    path(r"", include(posts_router.urls)),
    path(r"", include(likes_router.urls)),
    path(r"", include(repost_router.urls)),
]
