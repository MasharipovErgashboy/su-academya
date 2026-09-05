from django.urls import path
from .views import (
    SubscriptionPlanListView,
    SubscriptionPlanDetailView,
    SubscriptionPayView,
    BookQRScanView,
)

urlpatterns = [
    path("plans/", SubscriptionPlanListView.as_view(), name="plan-list"),
    path("plans/<int:pk>/", SubscriptionPlanDetailView.as_view(), name="plan-detail"),
    path("pay/", SubscriptionPayView.as_view(), name="pay"),
    path("book/scan/", BookQRScanView.as_view(), name="book-scan"),
]
