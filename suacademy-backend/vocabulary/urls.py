from django.urls import path
from .views import (
    VocabularyTopicsAPIView,
    VocabularyTopicDetailAPIView,
    VocabularyDefaultTopicAPIView,
)

urlpatterns = [
    path("topics/", VocabularyTopicsAPIView.as_view(), name="vocabulary-topics"),
    path("default", VocabularyDefaultTopicAPIView.as_view(), name="vocabulary-default"),
    path("<slug:topic_slug>/", VocabularyTopicDetailAPIView.as_view(), name="vocabulary-topic-detail"),
]
