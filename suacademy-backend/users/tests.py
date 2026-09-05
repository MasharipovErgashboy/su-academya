from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User, EmailOTP

class AuthTests(APITestCase):
    def test_register_user(self):
        url = reverse('register')
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123",
            "nationality": "uz"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="test@example.com").exists())
        self.assertTrue(EmailOTP.objects.filter(user__email="test@example.com").exists())

    def test_verify_otp(self):
        user = User.objects.create_user(username="verify", email="verify@example.com", password="password")
        otp = EmailOTP.objects.create(user=user, code="123456")
        
        url = reverse('verify-otp')
        data = {
            "email": "verify@example.com",
            "code": "123456"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertTrue(user.is_verified)
        self.assertIn('access', response.data)

    def test_login(self):
        user = User.objects.create_user(username="login", email="login@example.com", password="password")
        user.is_verified = True
        user.save()

        url = reverse('login')
        data = {
            "username": "login",
            "password": "password"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
