


from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django.db import IntegrityError
from rest_framework import status, permissions, serializers

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from drf_yasg.utils import swagger_auto_schema

from .models import User, EmailOTP, PasswordResetToken
from .serializers import (
    RegisterSerializer,
    VerifyOTPSerializer,
    LoginSerializer,
    ProfileSerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    PasswordResetConfirmSerializer,
)
from .utils import send_password_reset_email


# ======================================================
# AUTH – REGISTER
# POST /auth/register/
# ======================================================
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(tags=["auth"], request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # OTP yaratish + email yuborish serializer.create() ichida bo‘ladi.
        # SMTP/Brevo xato bo‘lsa API chiroyli error qaytarsin deb try/except qo‘shdik.
        try:
            serializer.save()
        except serializers.ValidationError as e:
            raise e
        except IntegrityError as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"IntegrityError during registration: {e}")
            return Response(
                {"error": "Ushbu email yoki foydalanuvchi nomi allaqachon mavjud."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Registration Error: {type(e).__name__}: {e}", exc_info=True)
            return Response(
                {"error": "Email yuborishda yoki tizimda xatolik yuz berdi. Iltimos, keyinroq urinib ko'ring."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {"detail": "Tasdiqlash kodi (OTP) emailga yuborildi"},
            status=status.HTTP_201_CREATED,
        )


# ======================================================
# AUTH – VERIFY OTP
# POST /auth/verify-otp/
# ======================================================
class VerifyOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(tags=["auth"], request_body=VerifyOTPSerializer)
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        code = serializer.validated_data["code"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Foydalanuvchi topilmadi"}, status=404)

        otp = EmailOTP.objects.filter(
            user=user,
            code=code,
            is_used=False,
        ).last()

        if not otp or otp.is_expired():
            return Response({"error": "OTP noto‘g‘ri yoki eskirgan"}, status=400)

        otp.is_used = True
        otp.save(update_fields=["is_used"])

        user.is_verified = True
        user.save(update_fields=["is_verified"])

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_200_OK,
        )


# ======================================================
# AUTH – LOGIN
# POST /auth/login/
# ======================================================
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(tags=["auth"], request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": ProfileSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )


# ======================================================
# AUTH – REFRESH TOKEN
# POST /auth/refresh/
# ======================================================
class RefreshTokenView(TokenRefreshView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(tags=["auth"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


# ======================================================
# AUTH – PROFILE
# GET /auth/profile/
# ======================================================
class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(tags=["auth"])
    def get(self, request):
        return Response(ProfileSerializer(request.user).data)

    @swagger_auto_schema(tags=["auth"], request_body=ProfileSerializer)
    def patch(self, request):
        user = request.user
        data = request.data

        # Allow updating username
        if "username" in data:
            user.username = data["username"]
        
        # Allow updating profile image
        if "image" in request.FILES:
            user.image = request.FILES["image"]

        user.save()
        return Response(ProfileSerializer(user).data)


# ======================================================
# AUTH – CHANGE PASSWORD
# POST /auth/change-password/
# ======================================================
class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(tags=["auth"], request_body=ChangePasswordSerializer)
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request.user.set_password(serializer.validated_data["password"])
        request.user.save()

        return Response(
            {"detail": "Parol muvaffaqiyatli yangilandi"},
            status=status.HTTP_200_OK,
        )


# ======================================================
# AUTH – FORGOT PASSWORD
# POST /auth/forgot-password/
# ======================================================
class ForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(tags=["auth"], request_body=ForgotPasswordSerializer)
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        try:
            user = User.objects.get(email=email)
            
            if not user.is_verified:
                return Response(
                    {"error": "Email manzilingiz hali tasdiqlanmagan. Iltimos, avval ro'yxatdan o'tishni yakunlang."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            token_obj = PasswordResetToken.objects.create(user=user)
            send_password_reset_email(user, token_obj.token)
        except User.DoesNotExist:
            return Response(
                {"error": "Ushbu email manzili bilan foydalanuvchi topilmadi."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            {"detail": "Parolni tiklash havolasi email manzilingizga yuborildi."},
            status=status.HTTP_200_OK,
        )


# ======================================================
# AUTH – PASSWORD RESET CONFIRM
# POST /auth/password-reset-confirm/
# ======================================================
class PasswordResetConfirmView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(tags=["auth"], request_body=PasswordResetConfirmSerializer)
    def post(self, request):
        token = request.headers.get("Token")

        if not token:
            return Response({"error": "Token yuborilmadi"}, status=400)

        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            token_obj = PasswordResetToken.objects.get(token=token)
        except PasswordResetToken.DoesNotExist:
            return Response({"error": "Token noto‘g‘ri"}, status=400)

        if token_obj.is_expired():
            return Response({"error": "Token eskirgan"}, status=400)

        user = token_obj.user
        user.set_password(serializer.validated_data["password"])
        user.save()

        token_obj.delete()

        return Response(
            {"detail": "Parol muvaffaqiyatli yangilandi"},
            status=status.HTTP_200_OK,
        )


# ======================================================
# NOTIFICATIONS
# GET /users/notifications/
# POST /users/notifications/{id}/read/
# ======================================================
class UserHistoryView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        from lessons.models import LessonFinished
        return LessonFinished.objects.filter(
            user=self.request.user
        ).select_related("lesson").order_by("-finished_at")

    def get_serializer_class(self):
        from .serializers import HistorySerializer
        return HistorySerializer


class NotificationListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Update imports inside method to avoid early import issues if any, or add to top
        from .models import Notification
        from .serializers import NotificationSerializer

        notifications = Notification.objects.filter(user=request.user)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)


class NotificationReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        from .models import Notification
        
        notification = get_object_or_404(Notification, pk=pk, user=request.user)
        notification.is_read = True
        notification.save()
        return Response({"status": "read"})
