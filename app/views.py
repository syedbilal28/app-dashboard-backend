from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from app.models import App
from app.serializers import AppSerializer
from plans.models import Plan
from subscriptions.models import Subscription


class AppViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    for CRUD operations on App model.
    """

    queryset = App.objects.all()
    serializer_class = AppSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def perform_create(self, serializer):

        created_app_object = serializer.save(user=self.request.user)
        free_plan = Plan.objects.get(name=Plan.FREE)
        Subscription.objects.create(
            app=created_app_object, plan=free_plan, is_active=True
        )
        return created_app_object

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
