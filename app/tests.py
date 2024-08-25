from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from app.models import App
from plans.models import Plan
from subscriptions.models import Subscription
from django.contrib.auth.models import User


class AppViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        self.free_plan = Plan.objects.create(name="Free", price=0)

        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)

        self.app = App.objects.create(
            name="Test App", description="Test App Description", user=self.user
        )

        self.list_url = reverse("apps")
        self.retrieve_url = reverse("app", args=[self.app.id])
        self.update_url = reverse("app", args=[self.app.id])
        self.destroy_url = reverse("app", args=[self.app.id])

    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)

    def test_create_app(self):
        self.authenticate()
        data = {"name": "New App", "description": "New App Description"}
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        app_id = response.data["id"]
        subscription = Subscription.objects.get(app_id=app_id)
        self.assertTrue(subscription.is_active)
        self.assertEqual(subscription.plan, self.free_plan)

    def test_list_apps(self):
        self.authenticate()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], self.app.name)

    def test_retrieve_app(self):
        self.authenticate()
        response = self.client.get(self.retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.app.name)

    def test_update_app(self):
        self.authenticate()
        data = {"name": "Updated App", "description": "Updated App Description"}
        response = self.client.put(self.update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated App")

    def test_destroy_app(self):
        self.authenticate()
        response = self.client.delete(self.destroy_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(App.DoesNotExist):
            App.objects.get(id=self.app.id)

    def test_list_apps_for_authenticated_user_only(self):
        self.authenticate()
        another_user = User.objects.create_user(
            username="anotheruser", password="anotherpassword"
        )
        App.objects.create(
            name="Another User App",
            description="Another User App Description",
            user=another_user,
        )

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_app_unauthorized(self):
        response = self.client.post(
            self.list_url,
            {"name": "Unauthorized App", "description": "Unauthorized App Description"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
