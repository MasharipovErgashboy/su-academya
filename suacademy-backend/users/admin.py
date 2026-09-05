from django.contrib import admin
from .models import User, EmailOTP, Notification


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "nationality",
        "interface_lang",
        "learning_lang",
        "is_verified",
        "is_premium",
    )
    list_filter = (
        "nationality",
        "is_verified",
        "is_premium",
    )
    search_fields = (
        "username",
        "email",
    )
    ordering = ("-id",)


@admin.register(EmailOTP)
class EmailOTPAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "code",
        "is_used",
        "created_at",
    )
    list_filter = (
        "is_used",
        "created_at",
    )
    search_fields = (
        "user__email",
        "code",
    )
    ordering = ("-created_at",)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "is_read", "created_at")
    list_filter = ("is_read", "created_at")
    search_fields = ("user__username", "user__email", "title", "message")
    ordering = ("-created_at",)
