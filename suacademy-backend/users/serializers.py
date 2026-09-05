import random
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User, EmailOTP, Notification
from .utils import send_otp_email


# ============================
# REGISTER
# ============================
class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(label=_("Username"))
    email = serializers.EmailField(label=_("Email"))
    password = serializers.CharField(label=_("Password"), write_only=True)
    nationality = serializers.ChoiceField(
        choices=[("uz", "Uzbek"), ("ja", "Japanese")],
        label=_("Nationality"),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password", "nationality")

    def validate_username(self, value):
        """Check if username already exists"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                _("Bu foydalanuvchi nomi allaqachon mavjud")
            )
        return value

    def validate_email(self, value):
        """Check if email already exists"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                _("Bu email manzili allaqachon mavjud")
            )
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.is_verified = False
        user.save(update_fields=["is_verified"])

        # Har bir user uchun eski OTP larni tozalash
        EmailOTP.objects.filter(user=user).delete()

        # 6 xonali OTP (aniq format)
        code = f"{random.randint(0, 999999):06d}"

        EmailOTP.objects.create(user=user, code=code)

        # OTP email yuborish (Brevo SMTP settings.py orqali ishlaydi)
        try:
            send_otp_email(user, code)
        except Exception:
            # SMTP xatolikni userga oshkor qilmaymiz
            raise serializers.ValidationError(
                {"email": _("Email yuborishda xatolik. Keyinroq qayta urinib ko‘ring.")}
            )

        return user


# ============================
# LOGIN
# ============================
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(label=_("Username"))
    password = serializers.CharField(label=_("Password"), write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data["username"],
            password=data["password"],
        )

        if not user:
            raise serializers.ValidationError(_("Login yoki parol noto‘g‘ri"))

        if not user.is_verified:
            raise serializers.ValidationError(_("Email tasdiqlanmagan"))

        return {"user": user}


# ============================
# OTP VERIFY
# ============================
class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(label=_("Email"))
    code = serializers.CharField(label=_("Verification code"), max_length=6)


# ============================
# PASSWORD
# ============================
class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(label=_("New password"), min_length=6)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(label=_("Email"))


class PasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(label=_("New password"), min_length=6)


# ============================
# PROFILE
# ============================
class ProfileSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(read_only=True)
    subscription = serializers.SerializerMethodField()
    stats = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "nationality",
            "interface_lang",
            "learning_lang",
            "is_verified",
            "is_premium",
            "student_id",
            "image",
            "subscription",
            "stats",
        )

    def get_subscription(self, obj):
        from django.utils import timezone
        active_sub = obj.subscriptions.filter(
            is_active=True,
            end_date__gt=timezone.now()
        ).order_by("-end_date").first()

        if active_sub:
            return {
                "plan": active_sub.plan.name,
                "end_date": active_sub.end_date,
                "is_active": True,
            }
        return None

    def get_stats(self, obj):
        return {
            "watched_count": obj.finished_lessons.count(),
            # history is now fetched via separate API, but we keep a small subset here if needed, or just count
            "history": [] 
        }


class HistorySerializer(serializers.ModelSerializer):
    lesson_title = serializers.CharField(source="lesson.title", read_only=True)
    lesson_slug = serializers.CharField(source="lesson.slug", read_only=True)
    lesson_image = serializers.SerializerMethodField()

    class Meta:
        from lessons.models import LessonFinished
        model = LessonFinished
        fields = (
            "id",
            "lesson_title",
            "lesson_slug",
            "lesson_image",
            "rating",
            "comment",
            "finished_at",
        )

    def get_lesson_image(self, obj):
        if obj.lesson.image:
            return obj.lesson.image.url
        return None


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ("id", "title", "message", "is_read", "created_at")
        read_only_fields = ("id", "created_at")
