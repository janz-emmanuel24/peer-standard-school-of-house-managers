from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import UserViewSet, BackgroundCheckViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'background-checks', BackgroundCheckViewSet, basename='backgroundcheck')

urlpatterns = [
    path('', include(router.urls)),
]
