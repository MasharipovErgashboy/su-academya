# users/urls.py
from django.urls import path
from .views import (
    RegisterView,
    VerifyOTPView,
    LoginView,
    RefreshTokenView,
    ProfileView,
    ChangePasswordView,
    ForgotPasswordView,
    PasswordResetConfirmView,
    NotificationListView,
    NotificationReadView,
    UserHistoryView,
)

urlpatterns = [
    # AUTH
    path("register/", RegisterView.as_view(), name="register"),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", RefreshTokenView.as_view(), name="refresh"),
    path("profile/", ProfileView.as_view(), name="profile"),

    # PASSWORD FLOW
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path("password-reset-confirm/", PasswordResetConfirmView.as_view(), name="password-reset-confirm"),

    # NOTIFICATIONS & HISTORY
    path("history/", UserHistoryView.as_view(), name="user-history"),
    path("notifications/", NotificationListView.as_view(), name="notifications-list"),
    path("notifications/<int:pk>/read/", NotificationReadView.as_view(), name="notifications-read"),
]
