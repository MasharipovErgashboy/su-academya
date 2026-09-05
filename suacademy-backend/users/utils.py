from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def send_otp_email(user, code):
    if user.nationality == "uz":
        subject = "SU Academy – Tasdiqlash kodi"
        template = "emails/otp_uz.html"
    else:
        subject = "SU Academy – 認証コード"
        template = "emails/otp_ja.html"

    html = render_to_string(
        template,
        {
            "code": code,
            "user": user,
        }
    )

    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None)

    email = EmailMultiAlternatives(
        subject,
        f"OTP: {code}",
        from_email,
        [user.email],
    )
    email.attach_alternative(html, "text/html")

    # email.send() integer qaytaradi (nechta email yuborildi).
    # Xatolik bo‘lsa exception ko‘taradi (Brevo/Gmail/SMTP muammo).
    sent_count = email.send(fail_silently=False)
    return sent_count


def send_password_reset_email(user, token):
    """
    TOKEN EMAILDA KO‘RINMAYDI ❌
    FAQAT RESET LINK YUBORILADI ✅
    """

    reset_link = f"{settings.FRONTEND_URL}/reset-password?token={token}"

    if user.nationality == "uz":
        subject = "SU Academy – Parolni tiklash"
        template = "emails/password_reset_uz.html"
    else:
        subject = "SU Academy – パスワード再設定"
        template = "emails/password_reset_ja.html"

    html = render_to_string(
        template,
        {
            "reset_link": reset_link,
            "user": user,
        }
    )

    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None)

    email = EmailMultiAlternatives(
        subject,
        "Parolni tiklash uchun emailni HTML ko‘rinishda oching",
        from_email,
        [user.email],
    )
    email.attach_alternative(html, "text/html")

    sent_count = email.send(fail_silently=False)
    return sent_count
