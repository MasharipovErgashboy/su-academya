from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import VocabularyTopic, VocabularyWord
from .utils import generate_vocabulary_audio


from django import forms

class VocabularyWordForm(forms.ModelForm):
    class Meta:
        model = VocabularyWord
        fields = "__all__"
        widgets = {
            "audio": forms.HiddenInput(),
        }

class VocabularyWordInline(admin.TabularInline):
    model = VocabularyWord
    form = VocabularyWordForm
    extra = 1
    # User requested to remove audio field from manual editing, we use HiddenInput + JS
    fields = ("order", "jp_word", "uz_word", "audio", "is_active")
    ordering = ("order",)


@admin.register(VocabularyTopic)
class VocabularyTopicAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "nationality", "slug", "order", "is_active")
    list_filter = ("nationality", "is_active")
    search_fields = ("title", "slug")
    ordering = ("nationality", "order", "id")

    prepopulated_fields = {
        "slug": ("title",)
    }

    inlines = [VocabularyWordInline]

    class Media:
        js = ("vocabulary/js/admin_audio.js",)


@admin.register(VocabularyWord)
class VocabularyWordAdmin(admin.ModelAdmin):
    form = VocabularyWordForm
    list_display = ("id", "topic", "order", "jp_word", "uz_word", "is_active")
    list_filter = ("topic__nationality", "is_active", "topic")
    search_fields = ("jp_word", "uz_word", "topic__title")
    ordering = ("topic", "order", "id")
    # User requested to remove audio field from manual editing
    fields = ("topic", "order", "jp_word", "uz_word", "audio", "is_active")

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "generate-audio/",
                self.admin_site.admin_view(self.generate_audio_view),
                name="vocabulary-generate-audio",
            ),
        ]
        return custom_urls + urls

    def generate_audio_view(self, request):
        if request.method != "POST":
            return JsonResponse({"success": False, "error": "Only POST allowed"})

        text = request.POST.get("text")
        lang = request.POST.get("lang")

        if not text or not lang:
            return JsonResponse({"success": False, "error": "Missing text or lang"})

        try:
            rel_path = generate_vocabulary_audio(text, lang)
            # If word ID exists, we can save it to the database
            word_id = request.POST.get("word_id")
            if word_id:
                try:
                    word = VocabularyWord.objects.get(id=word_id)
                    word.audio = rel_path
                    word.save()
                except VocabularyWord.DoesNotExist:
                    pass
            
            # Even if word doesn't exist (new record), we return the path
            # The JS could potentially use this if we wanted to show a preview
            from django.conf import settings
            full_url = request.build_absolute_uri(settings.MEDIA_URL + rel_path)
            
            return JsonResponse({
                "success": True, 
                "url": full_url,
                "rel_path": rel_path
            })
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    class Media:
        js = ("vocabulary/js/admin_audio.js",)
