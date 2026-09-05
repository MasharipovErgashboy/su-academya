from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema

from .models import Feedback
from .serializers import (
    FeedbackCreateSerializer,
    FeedbackListSerializer,
)


# ======================================================
# USER – CREATE FEEDBACK
# ======================================================
class FeedbackCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["feedback"],
        request_body=FeedbackCreateSerializer,
    )
    def post(self, request):
        serializer = FeedbackCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        Feedback.objects.create(
            user=request.user,  # 👈 MUHIM
            rating=serializer.validated_data["rating"],
            comment=serializer.validated_data["comment"],
            sections=serializer.validated_data["sections"],
        )

        return Response(
            {"detail": "Feedback muvaffaqiyatli yuborildi"},
            status=status.HTTP_201_CREATED,
        )


# ======================================================
# USER – MY FEEDBACKS
# ======================================================
class MyFeedbackListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["feedback"],
        responses={200: FeedbackListSerializer(many=True)},
    )
    def get(self, request):
        feedbacks = Feedback.objects.filter(user=request.user)
        serializer = FeedbackListSerializer(feedbacks, many=True)
        return Response(serializer.data)
