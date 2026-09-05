from django.contrib import admin
from .models import AdminActionLog


@admin.register(AdminActionLog)
class AdminActionLogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created_at",
        "action",
        "actor",
        "method",
        "path",
        "status_code",
        "ip_address",
    )

    list_filter = (
        "action",
        "method",
        "status_code",
        "created_at",
    )

    search_fields = (
        "actor__username",
        "actor__email",
        "path",
        "ip_address",
        "user_agent",
    )

    readonly_fields = (
        "actor",
        "action",
        "method",
        "path",
        "status_code",
        "ip_address",
        "user_agent",
        "extra",
        "created_at",
    )

    ordering = ("-created_at",)

    def has_view_permission(self, request, obj=None):
        # faqat superuser auditni ko‘ra oladi
        return request.user.is_active and request.user.is_superuser

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
