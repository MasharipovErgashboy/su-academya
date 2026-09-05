from django.db import models


class Swiper(models.Model):
    NATIONALITY_CHOICES = (
        ("uz", "Uzbek"),
        ("ja", "Japanese"),
    )

    nationality = models.CharField(
        max_length=2,
        choices=NATIONALITY_CHOICES
    )

    title = models.CharField(max_length=255)

    description = models.TextField(
        blank=True,
        null=True
    )

    button_text = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    button_url = models.URLField(
        blank=True,
        null=True
    )

    image = models.ImageField(
        upload_to="home/swiper/",
        blank=True,
        null=True
    )

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Home Swiper"
        verbose_name_plural = "Home Swipers"

    def __str__(self):
        return f"{self.title} ({self.nationality})"


class Intro(models.Model):
    NATIONALITY_CHOICES = (
        ("uz", "Uzbek"),
        ("ja", "Japanese"),
    )

    nationality = models.CharField(
        max_length=2,
        choices=NATIONALITY_CHOICES
    )

    title = models.CharField(max_length=255)

    content = models.TextField(
        blank=True,
        null=True
    )

    youtube_video_url = models.URLField(
        blank=True,
        null=True,
        help_text="YouTube video link"
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Home Intro"
        verbose_name_plural = "Home Intros"

    def __str__(self):
        return f"{self.title} ({self.nationality})"
