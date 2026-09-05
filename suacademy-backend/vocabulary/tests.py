from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from .models import VocabularyTopic, VocabularyWord

class VocabularyTests(APITestCase):
    def setUp(self):
        self.topic = VocabularyTopic.objects.create(
            nationality="uz",
            title="Topic 1",
            slug="topic-1"
        )
        self.word = VocabularyWord.objects.create(
            topic=self.topic,
            jp_word="Ohayou",
            uz_word="Xayrli tong"
        )

    def test_topic_list(self):
        user = User.objects.create_user(username="vocuser", password="password", nationality="uz")
        self.client.force_authenticate(user=user)
        # We need to set the language in headers because of NationalityMiddleware
        url = reverse('vocabulary-topics')
        response = self.client.get(url, HTTP_ACCEPT_LANGUAGE="uz")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_topic_detail(self):
        user = User.objects.create_user(username="vocuser_detail", password="password", nationality="uz")
        self.client.force_authenticate(user=user)
        url = reverse('vocabulary-topic-detail', kwargs={'topic_slug': self.topic.slug})
        response = self.client.get(url, HTTP_ACCEPT_LANGUAGE="uz")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['topic']['title'], "Topic 1")
