from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions, status
from django.shortcuts import get_object_or_404

from .models import Lesson
from .serializers import (
    LessonListItemSerializer,
    LessonDetailSerializer,
    LessonFinishedSerializer,
)


class LessonPagination(PageNumberPagination):
    page_size = 10


# =================================================
# LESSONS LIST (Pagination bilan)
# GET /lessons/list/
# =================================================
class LessonListView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LessonListItemSerializer
    pagination_class = LessonPagination

    def get_queryset(self):
        return Lesson.objects.filter(
            nationality=self.request.user.nationality
        ).order_by("order")


# =================================================
# LESSON DETAIL + LIST
# GET /lessons/{slug}/
# =================================================
class LessonDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, slug):
        user = request.user

        # 1️⃣ HOZIRGI VIDEO
        lesson = get_object_or_404(
            Lesson,
            slug=slug,
            nationality=user.nationality,
        )

        # 🔒 LOCK LOGIC
        is_locked = False
        if not lesson.is_free and not user.is_premium:
            is_locked = True

        lesson_data = LessonDetailSerializer(
            lesson,
            context={"request": request},
        ).data
        lesson_data["is_locked"] = is_locked

        # 2️⃣ 25 TA VIDEO RO‘YXATI
        lessons = Lesson.objects.filter(
            nationality=user.nationality
        ).order_by("order")

        lessons_list = LessonListItemSerializer(
            lessons,
            many=True,
            context={"request": request},
        ).data

        return Response(
            {
                "current_lesson": lesson_data,
                "lessons": lessons_list,
                "is_premium": user.is_premium,
            },
            status=status.HTTP_200_OK,
        )


# =================================================
# FINISH LESSON
# POST /lessons/finished/
# =================================================
class LessonFinishedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            print(f"DEBUG: LessonFinished received data: {request.data}")
            serializer = LessonFinishedSerializer(
                data=request.data,
                context={"request": request},
            )
            if not serializer.is_valid():
                print(f"DEBUG: Serializer Errors: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()

            return Response(
                {"detail": "Lesson yakunlandi"},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response(
                {"error": str(e), "type": type(e).__name__},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
