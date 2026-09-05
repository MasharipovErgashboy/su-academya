from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


class EmailOrUsernameBackend(ModelBackend):
    """
    Allow login with email or username
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        logger.info(f"Attempting authentication with: {username}")
        
        try:
            # Try to get user by email first
            user = User.objects.get(email=username)
            logger.info(f"User found by email: {user.username}")
        except User.DoesNotExist:
            # If not found by email, try by username
            try:
                user = User.objects.get(username=username)
                logger.info(f"User found by username: {user.username}")
            except User.DoesNotExist:
                logger.warning(f"User not found: {username}")
                return None

        # Check password
        if user.check_password(password):
            if self.user_can_authenticate(user):
                logger.info(f"Authentication successful for: {user.username}")
                return user
            else:
                logger.warning(f"User cannot authenticate (inactive/disabled): {user.username}")
        else:
            logger.warning(f"Invalid password for: {username}")

        return None
