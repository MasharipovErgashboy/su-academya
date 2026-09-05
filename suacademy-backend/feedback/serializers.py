from rest_framework import serializers
from .models import Feedback


class FeedbackCreateSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(
        min_value=1,
        max_value=5,
    )

    sections = serializers.ListField(
        child=serializers.ChoiceField(
            choices=["lessons", "ebook", "vocabulary", "ai", "all"]
        )
    )

    class Meta:
        model = Feedback
        fields = ("rating", "comment", "sections")


class FeedbackListSerializer(serializers.ModelSerializer):
    nationality = serializers.CharField(
        source="user.nationality",
        read_only=True,
    )

    class Meta:
        model = Feedback
        fields = (
            "id",
            "rating",
            "comment",
            "sections",
            "nationality",
            "admin_reply",
            "created_at",
            "replied_at",
        )
