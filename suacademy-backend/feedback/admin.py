from django.contrib import admin
from django.utils import timezone
from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "get_nationality",
        "rating",
        "created_at",
        "replied_at",
    )

    list_filter = (
        "rating",
        "created_at",
        "user__nationality",
    )

    readonly_fields = (
        "user",
        "get_nationality",
        "rating",
        "comment",
        "sections",
        "created_at",
    )

    fieldsets = (
        ("User maʼlumotlari", {
            "fields": ("user", "get_nationality")
        }),
        ("Feedback", {
            "fields": ("rating", "comment", "sections", "created_at")
        }),
        ("Admin javobi", {
            "fields": ("admin_reply", "replied_at")
        }),
    )

    def get_nationality(self, obj):
        return obj.user.nationality

    get_nationality.short_description = "Nationality"

    def save_model(self, request, obj, form, change):
        if obj.admin_reply and not obj.replied_at:
            obj.replied_at = timezone.now()
        super().save_model(request, obj, form, change)
