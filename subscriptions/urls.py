from django.urls import path

from subscriptions.views import SubscriptionViewSet

urlpatterns = [
    path(
        "subscriptions/",
        SubscriptionViewSet.as_view(
            {
                "get": "list",
            }
        ),
        name="subscriptions",
    ),
    path(
        "subscription/<str:pk>",
        SubscriptionViewSet.as_view(
            {
                "get": "get_subscription_by_app",
                "put": "update_subscription_by_app",
                "delete": "destroy",
            }
        ),
        name="subscription",
    ),
]
