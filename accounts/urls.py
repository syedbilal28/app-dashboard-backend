"""
URLs module for Accounts app containing URL patterns
for mapping URLs to appropriate views, allowing for
easy navigation and organization of the app's functionality
"""
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenRefreshView,
    TokenObtainPairView
)


urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", TokenBlacklistView.as_view(), name="token_blacklist_logout"),
]