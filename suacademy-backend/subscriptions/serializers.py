from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta

from .models import (
    SubscriptionPlan,
    UserSubscription,
    QRCodeItem,
)
from .services import set_user_premium


# =================================================
# SUBSCRIPTION PLANS
# =================================================

class SubscriptionPlanListSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    currency = serializers.SerializerMethodField()

    class Meta:
        model = SubscriptionPlan
        fields = (
            "id",
            "name",
            "duration_days",
            "price",
            "currency",
        )

    def get_price(self, obj):
        # 🔥 MUHIM: uzbek / japanese
        if obj.nationality == "uzbek":
            return obj.price_uzs
        return obj.price_usd

    def get_currency(self, obj):
        if obj.nationality == "uzbek":
            return "UZS"
        return "USD"


class SubscriptionPlanDetailSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    currency = serializers.SerializerMethodField()

    class Meta:
        model = SubscriptionPlan
        fields = "__all__"

    def get_price(self, obj):
        if obj.nationality == "uzbek":
            return obj.price_uzs
        return obj.price_usd

    def get_currency(self, obj):
        if obj.nationality == "uzbek":
            return "UZS"
        return "USD"


# =================================================
# SUBSCRIPTION PAY (FAKE PAYMENT)
# =================================================

class SubscriptionPaySerializer(serializers.Serializer):
    plan_id = serializers.IntegerField()

    def validate(self, attrs):
        user = self.context["request"].user

        # Nationality mapping
        user_nat = user.nationality
        if user_nat == "uz":
             plan_nat = "uzbek"
        elif user_nat == "ja":
             plan_nat = "japanese"
        else:
             plan_nat = user_nat

        try:
            plan = SubscriptionPlan.objects.get(
                id=attrs["plan_id"],
                is_active=True,
                nationality=plan_nat,  # 🔥 MOS
            )
        except SubscriptionPlan.DoesNotExist:
            raise serializers.ValidationError("Plan topilmadi yoki siz uchun emas.")

        attrs["plan"] = plan
        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        plan = validated_data["plan"]

        now = timezone.now()
        end = now + timedelta(days=plan.duration_days)

        subscription = UserSubscription.objects.create(
            user=user,
            plan=plan,
            start_date=now,
            end_date=end,
            is_active=True,
            payment_type="fake",
        )

        set_user_premium(user, end)
        return subscription


# =================================================
# BOOK QR SCAN (ONE-TIME)
# =================================================

class BookQRScanSerializer(serializers.Serializer):
    qr_code = serializers.UUIDField()

    def validate(self, attrs):
        try:
            qr = QRCodeItem.objects.select_related("book").get(
                code=attrs["qr_code"]
            )
        except QRCodeItem.DoesNotExist:
            raise serializers.ValidationError("QR code topilmadi.")

        if qr.is_used:
            raise serializers.ValidationError("Bu QR code allaqachon ishlatilgan.")

        attrs["qr"] = qr
        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        qr = validated_data["qr"]

        now = timezone.now()
        end = now + timedelta(days=qr.book.duration_days)

        # QR ni ishlatilgan deb belgilash
        qr.is_used = True
        qr.used_by = user
        qr.used_at = now
        qr.save(update_fields=["is_used", "used_by", "used_at"])

        # Book QR uchun avtomatik subscription plan
        plan, _ = SubscriptionPlan.objects.get_or_create(
            name="Book QR Subscription",
            nationality=user.nationality,  # 🔥 MOS
            defaults={
                "duration_days": qr.book.duration_days,
                "price_uzs": 0,
                "price_usd": 0,
                "is_active": True,
            },
        )

        subscription = UserSubscription.objects.create(
            user=user,
            plan=plan,
            start_date=now,
            end_date=end,
            is_active=True,
            payment_type="book_qr",
        )

        set_user_premium(user, end)
        return subscription
