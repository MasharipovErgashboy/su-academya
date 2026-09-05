from django.urls import path
from .views import FeedbackCreateView

urlpatterns = [
    path('v1/feedbacks/', FeedbackCreateView.as_view(), name='feedback-create'),
]
