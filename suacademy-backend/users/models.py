from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid


class User(AbstractUser):
    NATIONALITY_CHOICES = (
        ("uz", "Uzbek"),
        ("ja", "Japanese"),
    )

    LANGUAGE_CHOICES = (
        ("uz", "Uzbek"),
        ("ja", "Japanese"),
    )

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)

    nationality = models.CharField(
        max_length=2,
        choices=NATIONALITY_CHOICES,
        default="uz",
    )

    interface_lang = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, blank=True)
    learning_lang = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, blank=True)

    is_verified = models.BooleanField(default=False)

    is_premium = models.BooleanField(default=False)
    premium_until = models.DateTimeField(null=True, blank=True)

    image = models.ImageField(
        upload_to="profile_images/",
        blank=True,
        null=True,
    )

    student_id = models.CharField(max_length=20, unique=True, null=True, blank=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def save(self, *args, **kwargs):
        if not self.student_id:
            # Simple ID generation: Year + ID (Conceptual, strictly robust version needs sequence table)
            # For simplicity in this project, we'll use a random or sequential approach after save if possible,
            # but here we can try a simple approximate: Year + Random/UUID subset
            # Or better: Year + count + 1
            year = timezone.now().year
            last_user = User.objects.filter(student_id__startswith=str(year)).order_by("student_id").last()
            if last_user and last_user.student_id:
                 try:
                    last_seq = int(last_user.student_id[4:])
                    new_seq = last_seq + 1
                 except ValueError:
                    new_seq = 1
            else:
                new_seq = 1
            
            self.student_id = f"{year}{new_seq:05d}" # e.g., 202400001

        # Auto-verify superuser/staff accounts
        if self.is_superuser or self.is_staff:
            self.is_verified = True

        if self.nationality == "uz":
            self.interface_lang = "uz"
            self.learning_lang = "ja"
        elif self.nationality == "ja":
            self.interface_lang = "ja"
            self.learning_lang = "uz"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.student_id})"


class EmailOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="email_otps")
    code = models.CharField(max_length=6)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=5)


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reset_tokens")
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=15)

    def __str__(self):
        return f"{self.user.email} - {self.token}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Notification for {self.user}: {self.title}"
