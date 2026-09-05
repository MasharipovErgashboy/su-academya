from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    rating = models.IntegerField(default=5)
    benefits = models.TextField(blank=True, null=True, verbose_name="Platforma foydasi")
    useful_sections = models.JSONField(verbose_name="Foydali bo'limlar", default=list)
    suggestions = models.TextField(blank=True, null=True, verbose_name="Takliflar")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Fikr-mulohaza"
        verbose_name_plural = "Fikr-mulohazalar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.rating}⭐️"
