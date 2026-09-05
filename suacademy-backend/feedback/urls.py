from django.urls import path
from .views import (
    FeedbackCreateView,
    MyFeedbackListView,
)

urlpatterns = [
    path("create/", FeedbackCreateView.as_view()),
    path("my/", MyFeedbackListView.as_view()),
]
