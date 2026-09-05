from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import UserSubscription
from .services import set_user_premium

@receiver(post_save, sender=UserSubscription)
@receiver(post_delete, sender=UserSubscription)
def recalculate_user_premium(sender, instance, **kwargs):
    """
    UserSubscription o'zgarganda (yaratilganda, o'chirilganda, yangilanganda)
    userming premium statusini qayta hisoblash.
    """
    user = instance.user
    
    # Userning barcha faol obunalarini olish
    active_subs = user.subscriptions.filter(
        is_active=True,
        end_date__gt=timezone.now()
    ).order_by("-end_date")

    if active_subs.exists():
        # Eng uzoq muddatli obunani olish
        latest_sub = active_subs.first()
        set_user_premium(user, latest_sub.end_date)
    else:
        # Hozirgi vaqtda faol obuna yo'q -> Premium o'chiriladi
        set_user_premium(user, None)
