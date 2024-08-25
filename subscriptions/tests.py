from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from subscriptions.models import Subscription, App, Plan
from django.contrib.auth.models import User

class SubscriptionViewSetTests(APITestCase):
    def setUp(self):

        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.free_plan = Plan.objects.create(name='Free', price=0)
        self.standard_plan = Plan.objects.create(name='Standard', price=10)
        self.pro_plan = Plan.objects.create(name='Pro', price=25)

        self.app = App.objects.create(name='Test App', description='Test App Description', user=self.user)

        self.subscription = Subscription.objects.create(app=self.app, plan=self.free_plan, is_active=True)

        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)

        self.list_url = reverse('subscriptions')
        self.retrieve_url = reverse('subscription', args=[self.subscription.id])
        self.update_url = reverse('subscription', args=[self.subscription.id])
        self.destroy_url = reverse('subscription', args=[self.subscription.id])

    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

    def test_list_subscriptions(self):
        self.authenticate()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_subscription_by_app(self):
        self.authenticate()
        response = self.client.get(reverse('subscription', args=[self.app.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['plan'], self.free_plan.id)

    def test_update_subscription_by_app(self):
        self.authenticate()
        data = {'plan': self.standard_plan.id}
        response = self.client.put(reverse('subscription', args=[self.app.id]), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['plan'], self.standard_plan.id)

    def test_soft_delete_subscription(self):
        self.authenticate()
        response = self.client.delete(self.destroy_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.subscription.refresh_from_db()
        self.assertFalse(self.subscription.is_active)

    def test_get_subscription_not_found(self):
        self.authenticate()
        response = self.client.get(reverse('subscription', args=[99999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_subscription_not_found(self):
        self.authenticate()
        data = {'plan': self.standard_plan.id}
        response = self.client.put(reverse('subscription', args=[99999]), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
