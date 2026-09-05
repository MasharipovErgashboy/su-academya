from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

from .models import AdminActionLog
from .utils import get_client_ip


@receiver(user_logged_in)
def log_admin_login(sender, request, user, **kwargs):
    if not user.is_staff:
        return

    AdminActionLog.objects.create(
        actor=user,
        action=AdminActionLog.ActionChoices.ADMIN_LOGIN,
        method="POST",
        path=(request.path or "")[:255],
        ip_address=get_client_ip(request),
        user_agent=(request.META.get("HTTP_USER_AGENT") or "")[:1000],
    )


@receiver(user_logged_out)
def log_admin_logout(sender, request, user, **kwargs):
    if not user or not user.is_staff:
        return

    AdminActionLog.objects.create(
        actor=user,
        action=AdminActionLog.ActionChoices.ADMIN_LOGOUT,
        method="POST",
        path=(request.path or "")[:255],
        ip_address=get_client_ip(request),
        user_agent=(request.META.get("HTTP_USER_AGENT") or "")[:1000],
    )
