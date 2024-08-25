from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

from subscriptions.models import Subscription
from subscriptions.serializers import SubscriptionSerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing subscriptions.
    """
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the subscriptions
        for the currently authenticated user.
        """
        return Subscription.objects.filter(app__user=self.request.user)

    @action(detail=True, methods=['get'])
    def get_subscription_by_app(self, request, pk=None):
        """
        Retrieve a specific subscription by the app ID.
        """
        try:
            subscription = Subscription.objects.get(
                app__id=pk, app__user=request.user
            )
            serializer = self.get_serializer(subscription)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Subscription.DoesNotExist:
            return Response(
                {"error": "Subscription not found for this app."},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['put'])
    def update_subscription_by_app(self, request, pk=None):
        """
        Update a specific subscription by the app ID.
        """
        try:
            subscription = Subscription.objects.get(
                app__id=pk, app__user=request.user
            )
        except Subscription.DoesNotExist:
            return Response(
                {"error": "Subscription not found for this app."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(
            subscription, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        subscription = self.get_object()
        subscription.cancel_subscription()
        return Response(status=200)