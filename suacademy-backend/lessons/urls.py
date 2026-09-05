from django.urls import path
from .views import (
    LessonListView,
    LessonDetailView,
    LessonFinishedView,
)

urlpatterns = [
    path("list/", LessonListView.as_view(), name="lesson-list"),
    path("finished/", LessonFinishedView.as_view(), name="lesson-finished"),
    path("<slug:slug>/", LessonDetailView.as_view(), name="lesson-detail"),
]
