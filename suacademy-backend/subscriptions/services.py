from django.utils import timezone


def set_user_premium(user, premium_until):
    user.premium_until = premium_until
    if premium_until:
        user.is_premium = premium_until > timezone.now()
    else:
        user.is_premium = False
    
    user.save(update_fields=["premium_until", "is_premium"])
