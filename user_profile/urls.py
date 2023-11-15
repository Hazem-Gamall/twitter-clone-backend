from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework_nested.routers import NestedSimpleRouter

router = routers.SimpleRouter()
router.register(r"users", views.UserViewSet)

posts_router = NestedSimpleRouter(router, r"users", lookup="posts")
posts_router.register(r"posts", views.UserPostsViewSet, basename="user-posts")

likes_router = NestedSimpleRouter(router, r"users", lookup="likes")
likes_router.register(r"likes", views.UserPostsLikesViewSet, basename="user-likes")

repost_router = NestedSimpleRouter(router, r"users", lookup="repost")
repost_router.register(r"repost", views.UserPostsRepostsViewSet, basename="user-repost")

followers_router = NestedSimpleRouter(router, r"users", lookup="followers")
followers_router.register(
    r"followers", views.UserFollowersViewSet, basename="user-followers"
)

following_router = NestedSimpleRouter(router, r"users", lookup="following")
following_router.register(
    r"following", views.UserFollowingViewSet, basename="user-following"
)

chats_router = NestedSimpleRouter(router, r"users", lookup="chats")
chats_router.register(r"chats", views.UserChatsViewSet, basename="user-chats")

urlpatterns = [
    path(r"", include(router.urls)),
    path(r"", include(posts_router.urls)),
    path(r"", include(likes_router.urls)),
    path(r"", include(repost_router.urls)),
    path(r"", include(followers_router.urls)),
    path(r"", include(following_router.urls)),
    path(r"", include(chats_router.urls)),
]
