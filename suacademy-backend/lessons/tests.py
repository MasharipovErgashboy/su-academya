from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from .models import Lesson

class LessonTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.lesson = Lesson.objects.create(
            title="Lesson 1",
            youtube_url="https://youtube.com/test",
            nationality="uz",
            is_free=True
        )

    def test_lesson_list(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('lesson-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_lesson_detail(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('lesson-detail', kwargs={'slug': self.lesson.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['current_lesson']['title'], "Lesson 1")
