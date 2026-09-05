from rest_framework import serializers
from .models import Lesson, LessonFinished


class LessonListItemSerializer(serializers.ModelSerializer):
    is_locked = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = (
            "id",
            "title",
            "slug",
            "order",
            "is_free",
            "is_locked",
            "image",
        )

    def get_is_locked(self, obj):
        request = self.context["request"]
        user = request.user

        if obj.is_free:
            return False

        if user.is_authenticated and user.is_premium:
            return False

        return True



class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.username", read_only=True)
    user_image = serializers.ImageField(source="user.image", read_only=True)

    class Meta:
        model = LessonFinished
        fields = ("id", "user_name", "user_image", "rating", "comment", "finished_at")


class LessonDetailSerializer(serializers.ModelSerializer):
    is_locked = serializers.SerializerMethodField()
    youtube_url = serializers.SerializerMethodField()
    youtube_id = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = (
            "id",
            "title",
            "description",
            "slug",
            "order",
            "is_free",
            "is_locked",
            "youtube_url",
            "youtube_id",
            "image",
            "reviews",
        )

    def get_is_locked(self, obj):
        user = self.context["request"].user

        if obj.is_free:
            return False

        if user.is_authenticated and user.is_premium:
            return False

        return True

    def get_youtube_url(self, obj):
        """
        Agar lesson qulflangan bo‘lsa → video qaytmaydi
        """
        if self.get_is_locked(obj):
            return None
        return obj.youtube_url

    def get_youtube_id(self, obj):
        """
        YouTube URL dan ID ni ajratib olish
        """
        if not obj.youtube_url:
            return None
        
        # Oddiy URL: https://www.youtube.com/watch?v=VIDEO_ID
        import re
        regex = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
        match = re.search(regex, obj.youtube_url)
        
        if match:
            return match.group(1)
        return None

    def get_reviews(self, obj):
        reviews = LessonFinished.objects.filter(
            lesson=obj, 
            comment__isnull=False
        ).exclude(comment="").order_by("-finished_at")[:3]
        return ReviewSerializer(reviews, many=True).data


class LessonFinishedSerializer(serializers.Serializer):
    lesson_id = serializers.IntegerField()
    rating = serializers.IntegerField(min_value=1, max_value=5, required=False)
    comment = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        user = self.context["request"].user
        lesson_id = attrs["lesson_id"]

        try:
            lesson = Lesson.objects.get(
                id=lesson_id,
            )
        except Lesson.DoesNotExist:
            raise serializers.ValidationError("Lesson topilmadi")

        if not lesson.is_free and not user.is_premium:
            raise serializers.ValidationError(
                "Bu dars premium obuna talab qiladi"
            )

        attrs["lesson"] = lesson
        return attrs

    def create(self, validated_data):
        from django.utils import timezone
        user = self.context["request"].user
        lesson = validated_data["lesson"]
        rating = validated_data.get("rating")
        comment = validated_data.get("comment", "")

        defaults = {
            "finished_at": timezone.now() # Force update timestamp
        }
        if rating is not None:
             defaults["rating"] = rating
        if comment is not None:
             defaults["comment"] = comment

        obj, created = LessonFinished.objects.update_or_create(
            user=user,
            lesson=lesson,
            defaults=defaults
        )
        return obj
