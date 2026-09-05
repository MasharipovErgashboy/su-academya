from django.db import models
from django.conf import settings


class Feedback(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="feedbacks",
    )

    rating = models.PositiveSmallIntegerField(
        help_text="1 dan 5 gacha baho"
    )

    comment = models.TextField(
        help_text="Foydalanuvchi fikri"
    )

    sections = models.JSONField(
        help_text="Qaysi bo‘limlar haqida: lessons, ebook, vocabulary, ai, all"
    )

    # Admin javobi
    admin_reply = models.TextField(
        blank=True,
        help_text="Admin javobi"
    )
    replied_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"

    def __str__(self):
        return f"{self.user.email} | ⭐ {self.rating}"
