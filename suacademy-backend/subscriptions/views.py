from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from .models import SubscriptionPlan
from .serializers import (
    SubscriptionPlanListSerializer,
    SubscriptionPlanDetailSerializer,
    SubscriptionPaySerializer,
    BookQRScanSerializer,
)


# =================================================
# HELPERS
# =================================================

def map_user_nationality(user_nat: str) -> str:
    """
    User nationality (ja/uz) -> SubscriptionPlan nationality (japanese/uzbek)
    """
    if user_nat == "ja":
        return "japanese"
    if user_nat == "uz":
        return "uzbek"
    return user_nat


# =================================================
# SUBSCRIPTION PLANS
# =================================================

class SubscriptionPlanListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SubscriptionPlanListSerializer

    def get_queryset(self):
        user_nat = map_user_nationality(self.request.user.nationality)

        return SubscriptionPlan.objects.filter(
            is_active=True,
            nationality=user_nat,
        )


class SubscriptionPlanDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SubscriptionPlanDetailSerializer
    queryset = SubscriptionPlan.objects.filter(is_active=True)


# =================================================
# SUBSCRIPTION PAY (FAKE)
# =================================================

class SubscriptionPayView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(request_body=SubscriptionPaySerializer)
    def post(self, request):
        serializer = SubscriptionPaySerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        sub = serializer.save()

        return Response(
            {
                "message": "Subscription activated (FAKE payment).",
                "subscription_id": sub.id,
                "end_date": sub.end_date,
            },
            status=status.HTTP_201_CREATED,
        )


# =================================================
# BOOK QR SCAN ✅ SWAGGER FIX
# =================================================

class BookQRScanView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(request_body=BookQRScanSerializer)
    def post(self, request):
        serializer = BookQRScanSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        sub = serializer.save()

        return Response(
            {
                "message": "QR accepted. Subscription activated.",
                "subscription_id": sub.id,
                "end_date": sub.end_date,
            },
            status=status.HTTP_201_CREATED,
        )
