from django.contrib import admin
from .models import Lesson, LessonFinished


# =========================
# LESSON ADMIN
# =========================
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "nationality",
        "is_free",
        "order",
        "created_at",
    )

    list_filter = (
        "nationality",
        "is_free",
    )

    search_fields = (
        "title",
        "slug",
    )

    prepopulated_fields = {
        "slug": ("title",),
    }

    ordering = ("order",)

    list_editable = (
        "order",
        "is_free",
    )

    readonly_fields = (
        "created_at",
    )


# =========================
# LESSON FINISHED ADMIN
# =========================
@admin.register(LessonFinished)
class LessonFinishedAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "lesson",
        "finished_at",
        "rating",
        "comment",
    )

    list_filter = (
        "lesson__nationality",
        "finished_at",
    )

    search_fields = (
        "user__username",
        "lesson__title",
    )

    readonly_fields = (
        "finished_at",
    )
