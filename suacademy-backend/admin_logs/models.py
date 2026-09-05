from django.conf import settings
from django.db import models


class AdminActionLog(models.Model):
    """
    Admin va staff userlarning barcha muhim harakatlari logi
    """

    class ActionChoices(models.TextChoices):
        ADMIN_LOGIN = "ADMIN_LOGIN", "Admin Login"
        ADMIN_LOGOUT = "ADMIN_LOGOUT", "Admin Logout"
        ADMIN_REQUEST = "ADMIN_REQUEST", "Admin Panel Request"
        API_REQUEST = "API_REQUEST", "API Request"

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="admin_action_logs",
        verbose_name="Actor (Admin)",
    )

    action = models.CharField(
        max_length=50,
        choices=ActionChoices.choices,
        default=ActionChoices.ADMIN_REQUEST,
    )

    method = models.CharField("HTTP Method", max_length=10, blank=True)
    path = models.CharField("Request Path", max_length=255, blank=True)

    status_code = models.PositiveIntegerField(null=True, blank=True)

    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    extra = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Admin Action Log"
        verbose_name_plural = "Admin Action Logs"
        indexes = [
            models.Index(fields=["-created_at"]),
            models.Index(fields=["action"]),
            models.Index(fields=["path"]),
        ]

    def __str__(self):
        return f"{self.created_at} | {self.action} | {self.actor}"
