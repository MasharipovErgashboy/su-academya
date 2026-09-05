from django.contrib import admin
from .models import Swiper, Intro


@admin.register(Swiper)
class SwiperAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "nationality",
        "order",
        "is_active",
        "created_at",
    )
    list_filter = ("nationality", "is_active")
    search_fields = ("title", "description")
    list_editable = ("order", "is_active")
    ordering = ("order",)

    fieldsets = (
        ("Language", {
            "fields": ("nationality",),
        }),
        ("Content", {
            "fields": (
                "title",
                "description",
                "image",
            ),
        }),
        ("Button", {
            "fields": (
                "button_text",
                "button_url",
            ),
        }),
        ("Settings", {
            "fields": (
                "order",
                "is_active",
            ),
        }),
    )


@admin.register(Intro)
class IntroAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "nationality",
        "is_active",
        "created_at",
    )
    list_filter = ("nationality", "is_active")
    search_fields = ("title", "content")

    fieldsets = (
        ("Language", {
            "fields": ("nationality",),
        }),
        ("Intro Content", {
            "fields": (
                "title",
                "content",
                "youtube_video_url",
            ),
        }),
        ("Settings", {
            "fields": ("is_active",),
        }),
    )
