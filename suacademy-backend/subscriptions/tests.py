from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from .models import SubscriptionPlan

class SubscriptionTests(APITestCase):
    def setUp(self):
        self.plan = SubscriptionPlan.objects.create(
            name="Test Plan",
            nationality="uzbek",
            duration_days=30,
            price_uzs=100000
        )

    def test_plan_list(self):
        user = User.objects.create_user(username="subuser", password="password")
        self.client.force_authenticate(user=user)
        url = reverse('plan-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # We need to make sure the user nationality matches the plan
        # The plan created in setUp is 'uzbek', and user default is 'uz'
        self.assertEqual(len(response.data), 1)
