from django.db import models


class VocabularyTopic(models.Model):
    NATIONALITY_CHOICES = (
        ("uz", "Uzbek"),
        ("ja", "Japanese"),
    )

    nationality = models.CharField(max_length=2, choices=NATIONALITY_CHOICES)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    order = models.PositiveIntegerField(default=1)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["nationality", "slug"],
                name="uniq_topic_slug_per_nationality",
            )
        ]

    def __str__(self):
        return f"[{self.nationality}] {self.title}"


class VocabularyWord(models.Model):
    topic = models.ForeignKey(
        VocabularyTopic,
        on_delete=models.CASCADE,
        related_name="words",
    )

    jp_word = models.CharField(max_length=255)
    uz_word = models.CharField(max_length=255)

    # optional (mp3/wav). MEDIA_ROOT ichiga saqlanadi
    audio = models.FileField(upload_to="vocabulary/audio/", null=True, blank=True)

    order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.jp_word} / {self.uz_word}"
