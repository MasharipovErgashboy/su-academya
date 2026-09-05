from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = 'Create a superuser account for admin access'

    def handle(self, *args, **options):
        username = '223341e@jdu.uz'
        email = '223341e@jdu.uz'
        password = 'ergashboy2004'

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'User {username} already exists'))
            return

        # Create superuser
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.is_verified = True
        user.save()

        self.stdout.write(self.style.SUCCESS(
            f'Successfully created superuser: {username}'
        ))
