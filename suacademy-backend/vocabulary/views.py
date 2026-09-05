from django.db.models import Count, Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from .models import VocabularyTopic, VocabularyWord
from .serializers import VocabularyTopicListSerializer


class VocabularyTopicsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Vocabulary"],
        operation_summary="Vocabulary topics list",
        operation_description="Login bo'lgan user uchun nationality bo‘yicha vocabulary topics ro‘yxati",
        responses={200: VocabularyTopicListSerializer(many=True)},
    )
    def get(self, request):
        nat = request.user.nationality

        qs = (
            VocabularyTopic.objects
            .filter(nationality=nat, is_active=True)
            .annotate(words_count=Count("words", filter=Q(words__is_active=True)))
            .order_by("order", "id")
        )

        serializer = VocabularyTopicListSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VocabularyTopicDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Vocabulary"],
        operation_summary="Vocabulary topic detail",
        operation_description="Tanlangan topic bo‘yicha so‘zlar ro‘yxati (learning logic bilan)",
    )
    def get(self, request, topic_slug: str):
        nat = request.user.nationality

        try:
            topic = VocabularyTopic.objects.get(
                nationality=nat,
                slug=topic_slug,
                is_active=True,
            )
        except VocabularyTopic.DoesNotExist:
            return Response(
                {"detail": "Topic not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        q = (request.query_params.get("q") or "").strip()

        words_qs = VocabularyWord.objects.filter(
            topic=topic,
            is_active=True,
        )

        if q:
            words_qs = words_qs.filter(
                Q(jp_word__icontains=q) | Q(uz_word__icontains=q)
            )

        words_qs = words_qs.order_by("order", "id")

        data = {
            "topic": {
                "id": topic.id,
                "slug": topic.slug,
                "title": topic.title,
                "order": topic.order,
            },
            "words": [
                {
                    "id": w.id,
                    "word": w.jp_word if nat == "uz" else w.uz_word,
                    "translation": w.uz_word if nat == "uz" else w.jp_word,
                    "audio": request.build_absolute_uri(w.audio.url) if w.audio else None,
                }
                for w in words_qs
            ]
        }

        return Response(data, status=status.HTTP_200_OK)


class VocabularyDefaultTopicAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Vocabulary"],
        operation_summary="Default vocabulary topic",
        operation_description="User nationality bo‘yicha order=1 bo‘lgan default topic",
    )
    def get(self, request):
        nat = request.user.nationality

        topic = (
            VocabularyTopic.objects
            .filter(nationality=nat, is_active=True)
            .order_by("order", "id")
            .first()
        )

        if not topic:
            return Response(
                {"detail": "No vocabulary topics found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            {"default_slug": topic.slug},
            status=status.HTTP_200_OK,
        )
