from django.urls import path, include
from rest_framework import routers
from . import views
from rest_framework_nested.routers import NestedSimpleRouter

router = routers.SimpleRouter()
router.register(r"posts", views.PostViewSet)

replies_router = NestedSimpleRouter(router, r"posts", lookup="post")
replies_router.register(r"replies", views.PostRepliesViewSet, basename="post-replies")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(replies_router.urls)),
]
