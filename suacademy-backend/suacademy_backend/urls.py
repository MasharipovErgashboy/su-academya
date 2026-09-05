from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# =========================
# SWAGGER CONFIG
# =========================
schema_view = get_schema_view(
    openapi.Info(
        title="SU Academy API",
        default_version="v1",
        description="SU Academy Backend API dokumentatsiyasi",
        contact=openapi.Contact(email="support@suacademy.uz"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


# =========================
# URLS
# =========================
urlpatterns = [
    # Swagger UI as home
    path("", schema_view.with_ui("swagger", cache_timeout=0)),
    # ADMIN (custom path)
    path("su-academya-administration/", admin.site.urls),

    # AUTH
    path("auth/", include("users.urls")),

    # HOME
    path("home/", include("home.urls")),

    # BOOK (E-BOOK)
    path("ebooks/", include("ebooks.urls")),

    # VOCABULARY
    path("vocabulary/", include("vocabulary.urls")),

    # LESSONS
    path('lessons/', include('lessons.urls')),
    path('subscriptions/', include('subscriptions.urls')),
    # path('api/', include('ebooks.urls')), # Already defined above
    path('feedbacks/', include('feedbacks.urls')),


    # ❌ analytics BUTUNLAY O‘CHIRILDI

    # SWAGGER
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0)),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0)),
]


# =========================
# MEDIA (DEV ONLY)
# =========================
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
