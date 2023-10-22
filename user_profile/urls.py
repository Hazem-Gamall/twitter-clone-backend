from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework_nested.routers import NestedSimpleRouter

router = routers.SimpleRouter()
router.register(r"users", views.UserViewSet)

posts_router = NestedSimpleRouter(router, r"users", "post")

urlpatterns = router.urls
