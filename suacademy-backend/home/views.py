from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema

from .models import Swiper, Intro
from .serializers import SwiperSerializer, IntroSerializer


def get_nationality(request):
    """
    Nationality ni quyidagi tartibda oladi:
    1. Authenticated user bo'lsa -> user.nationality
    2. Accept-Language header bo'lsa -> header qiymati
    3. Session'da bo'lsa -> session.nationality
    4. Default -> 'uz'
    """
    if request.user.is_authenticated:
        return request.user.nationality
    
    # Accept-Language header'dan olish
    accept_lang = request.META.get('HTTP_ACCEPT_LANGUAGE', '').lower()
    if 'ja' in accept_lang:
        return 'ja'
    elif 'uz' in accept_lang:
        return 'uz'
    
    # Session'dan olish
    return request.session.get("nationality", "uz")


# ======================================================
# HOME – SWIPER
# ======================================================
class HomeSwiperView(APIView):
    """
    Home sahifadagi slider (swiper)
    Platforma tanlangan nationality bo‘yicha qaytadi
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        tags=["home"],
        responses={200: SwiperSerializer(many=True)},
    )
    def get(self, request):
        nationality = get_nationality(request)

        swipers = (
            Swiper.objects.filter(
                nationality=nationality,
                is_active=True,
            )
            .order_by("order")
        )

        serializer = SwiperSerializer(swipers, many=True)

        return Response(
            {
                "count": swipers.count(),
                "results": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ======================================================
# HOME – INTRO
# ======================================================
class HomeIntroView(APIView):
    """
    Home sahifadagi intro (title, description, video)
    Har bir nationality uchun bittadan
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        tags=["home"],
        responses={200: IntroSerializer},
    )
    def get(self, request):
        nationality = get_nationality(request)

        intro = Intro.objects.filter(
            nationality=nationality,
            is_active=True,
        ).first()

        if not intro:
            return Response(
                {"detail": "Intro topilmadi"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = IntroSerializer(intro)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


# ======================================================
# HOME – STATS
# ======================================================
from users.models import User
from ebooks.models import Book
from lessons.models import Lesson
from vocabulary.models import VocabularyWord

class HomeStatsView(APIView):
    """
    Home sahifadagi statistika
    Real vaqt rejimida ma'lumotlarni hisoblaydi
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        tags=["home"],
        responses={200: "Stats object"},
    )
    def get(self, request):
        nationality = get_nationality(request)

        # Users count (Real users only, filtering out admins if needed, but for stats 'all users' is fine or verified ones)
        # Assuming we count all registered users
        users_count = User.objects.count()

        # Books count (Active books, filtered by nationality if desired, but total platform power is better)
        books_count = Book.objects.filter(is_active=True).count()

        # Lessons count
        lessons_count = Lesson.objects.count()

        # Vocabulary count
        vocabulary_count = VocabularyWord.objects.count()

        return Response(
            {
                "users": users_count,
                "books": books_count,
                "lessons": lessons_count,
                "vocabulary": vocabulary_count,
            },
            status=status.HTTP_200_OK,
        )
