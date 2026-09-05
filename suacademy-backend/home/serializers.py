from rest_framework import serializers
from .models import Swiper, Intro


class SwiperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Swiper
        fields = (
            "id",
            "title",
            "description",
            "button_text",
            "button_url",
            "image",
            "order",
        )


class IntroSerializer(serializers.ModelSerializer):
    youtube_id = serializers.SerializerMethodField()

    class Meta:
        model = Intro
        fields = (
            "id",
            "title",
            "content",
            "youtube_video_url",
            "youtube_id",
        )

    def get_youtube_id(self, obj):
        if not obj.youtube_video_url:
            return None
        
        import re
        regex = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
        match = re.search(regex, obj.youtube_video_url)
        
        if match:
            return match.group(1)
        return None
