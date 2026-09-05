from django.contrib import admin
from django.http import HttpResponse
from zipfile import ZipFile
from io import BytesIO

from .models import (
    SubscriptionPlan,
    UserSubscription,
    QRCodeBook,
    QRCodeItem,
)
from .utils import generate_qr_png


# =========================
# SUBSCRIPTION PLAN
# =========================
@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "nationality", "duration_days", "is_active")
    list_filter = ("nationality", "is_active")
    search_fields = ("name",)


# =========================
# USER SUBSCRIPTION
# =========================
@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "plan",
        "payment_type",
        "start_date",
        "end_date",
        "is_active",
    )
    list_filter = ("payment_type", "is_active")
    search_fields = ("user__username",)

    def delete_queryset(self, request, queryset):
        """
        Bulk deleteda signallar ishlashi uchun har birini alohida o'chiramiz.
        """
        for obj in queryset:
            obj.delete()


# =========================
# QR CODE ITEM
# =========================
@admin.register(QRCodeItem)
class QRCodeItemAdmin(admin.ModelAdmin):
    list_display = ("code", "book", "is_used", "used_by")
    list_filter = ("is_used",)
    search_fields = ("code",)


# =========================
# QR CODE BOOK
# =========================
@admin.register(QRCodeBook)
class QRCodeBookAdmin(admin.ModelAdmin):
    list_display = ("title", "duration_days", "total_qr", "created_at")
    actions = ("generate_qr_codes", "download_qr_zip")

    def generate_qr_codes(self, request, queryset):
        for book in queryset:
            for _ in range(book.total_qr):
                qr = QRCodeItem.objects.create(book=book)
                generate_qr_png(qr)
                qr.save()
        self.message_user(request, "QR code'lar yaratildi.")

    generate_qr_codes.short_description = "Generate QR codes (PNG)"

    def download_qr_zip(self, request, queryset):
        buffer = BytesIO()
        zip_file = ZipFile(buffer, "w")

        for book in queryset:
            for qr in book.qr_codes.all():
                if qr.image:
                    zip_file.writestr(
                        f"{book.title}/{qr.image.name.split('/')[-1]}",
                        qr.image.read(),
                    )

        zip_file.close()

        response = HttpResponse(
            buffer.getvalue(),
            content_type="application/zip",
        )
        response["Content-Disposition"] = 'attachment; filename="qr_codes.zip"'
        return response

    download_qr_zip.short_description = "Download QR codes (ZIP)"
