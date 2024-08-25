from rest_framework import serializers

from app.models import App
from subscriptions.serializers import SubscriptionSerializer


class AppSerializer(serializers.ModelSerializer):
    subscription = SubscriptionSerializer(required=False)

    class Meta:
        model = App
        fields = ["id", "user", "name", "description", "subscription"]
        read_only_fields = ["user", "created_at"]
