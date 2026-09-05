from django.db import models
from django.conf import settings
from django.utils.text import slugify

User = settings.AUTH_USER_MODEL


# =========================
# LESSON
# =========================
class Lesson(models.Model):
    NATIONALITY_CHOICES = (
        ("uz", "Uzbek"),
        ("ja", "Japanese"),
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)

    description = models.TextField(
        blank=True,
        null=True,
        help_text="Dars tavsifi (ixtiyoriy)",
    )

    youtube_url = models.URLField(
        help_text="YouTube private/unlisted video link"
    )

    image = models.ImageField(
        upload_to="lessons/covers/",
        blank=True,
        null=True,
        help_text="Dars muqovasi (ixtiyoriy)",
    )

    nationality = models.CharField(
        max_length=2,
        choices=NATIONALITY_CHOICES,
    )

    is_free = models.BooleanField(
        default=False,
        help_text="Bepul darsmi?",
    )

    order = models.PositiveIntegerField(
        default=0,
        help_text="Dars tartib raqami",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# =========================
# FINISHED LESSON
# =========================
class LessonFinished(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="finished_lessons",
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="finished_by",
    )
    finished_at = models.DateTimeField(auto_now_add=True)
    
    rating = models.PositiveSmallIntegerField(
        null=True, 
        blank=True,
        help_text="Baho (1-5)"
    )
    comment = models.TextField(
        blank=True, 
        null=True,
        help_text="Foydalanuvchi izohi"
    )

    class Meta:
        unique_together = ("user", "lesson")

    def __str__(self):
        return f"{self.user} → {self.lesson}"
