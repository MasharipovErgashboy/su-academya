from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid

User = settings.AUTH_USER_MODEL


# ===============================
# SUBSCRIPTION PLAN
# ===============================
class SubscriptionPlan(models.Model):
    NATIONALITY_CHOICES = (
        ("uzbek", "Uzbek"),
        ("japanese", "Japanese"),
    )

    name = models.CharField(max_length=255)
    nationality = models.CharField(
        max_length=20,
        choices=NATIONALITY_CHOICES,
    )

    duration_days = models.PositiveIntegerField()
    price_uzs = models.PositiveIntegerField(default=0)
    price_usd = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} ({self.nationality})"


# ===============================
# USER SUBSCRIPTION
# ===============================
class UserSubscription(models.Model):
    PAYMENT_TYPE_CHOICES = (
        ("fake", "Fake"),
        ("book_qr", "Book QR"),
        ("admin", "Admin"),
        ("payme", "Payme"),
        ("click", "Click"),
        ("stripe", "Stripe"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscriptions",
    )
    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.CASCADE,
        related_name="user_subscriptions",
    )

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    is_active = models.BooleanField(default=True)
    payment_type = models.CharField(
        max_length=20,
        choices=PAYMENT_TYPE_CHOICES,
    )

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user} → {self.plan.name}"


# ===============================
# QR CODE BOOK
# ===============================
class QRCodeBook(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    duration_days = models.PositiveIntegerField(default=3)
    total_qr = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


# ===============================
# QR CODE ITEM (ONE TIME)
# ===============================
class QRCodeItem(models.Model):
    book = models.ForeignKey(
        QRCodeBook,
        on_delete=models.CASCADE,
        related_name="qr_codes",
    )

    code = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    image = models.ImageField(
        upload_to="qr_codes/",
        blank=True,
        null=True,
    )

    is_used = models.BooleanField(default=False)
    used_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    used_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.code)
