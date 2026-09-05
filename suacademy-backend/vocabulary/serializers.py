from rest_framework import serializers
from .models import VocabularyTopic, VocabularyWord


class VocabularyTopicListSerializer(serializers.ModelSerializer):
    words_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = VocabularyTopic
        fields = ("id", "slug", "title", "order", "words_count")


class VocabularyWordSerializer(serializers.ModelSerializer):
    word = serializers.SerializerMethodField()
    translation = serializers.SerializerMethodField()

    class Meta:
        model = VocabularyWord
        fields = ("id", "word", "translation", "audio")

    def _get_user_nationality(self):
        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            return request.user.nationality
        return "uz"

    def get_word(self, obj: VocabularyWord) -> str:
        # Uzbek user -> jp_word (learn JP)
        # Japanese user -> uz_word (learn UZ)
        nat = self._get_user_nationality()
        return obj.jp_word if nat == "uz" else obj.uz_word

    def get_translation(self, obj: VocabularyWord) -> str:
        nat = self._get_user_nationality()
        return obj.uz_word if nat == "uz" else obj.jp_word


class VocabularyTopicDetailSerializer(serializers.ModelSerializer):
    words = VocabularyWordSerializer(many=True)

    class Meta:
        model = VocabularyTopic
        fields = ("id", "slug", "title", "order", "words")
