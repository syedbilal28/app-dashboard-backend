from django.urls import path

from app.views import AppViewSet

urlpatterns = [
    path(
        "apps/",
        AppViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
        name="apps",
    ),
    path(
        "app/<str:pk>",
        AppViewSet.as_view({"get": "retrieve", "delete": "destroy", "put": "update"}),
        name="app",
    ),
]
