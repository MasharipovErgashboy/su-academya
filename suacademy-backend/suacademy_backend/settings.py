from pathlib import Path
from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

# ==================================================
# BASE DIR
# ==================================================
BASE_DIR = Path(__file__).resolve().parent.parent


# ==================================================
# SECURITY
# ==================================================
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
DEBUG = os.getenv("DEBUG", "True") == "True"
# Render + custom domains (env override recommended)
DEFAULT_ALLOWED_HOSTS = [
    "suacademy-backend.onrender.com",
    "localhost",
    "127.0.0.1",
    "suacademya.uz",
    "www.suacademya.uz",
]
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",") if os.getenv("ALLOWED_HOSTS") else DEFAULT_ALLOWED_HOSTS


# ==================================================
# APPLICATIONS
# ==================================================
INSTALLED_APPS = [
    # =======================
    # ADMIN UI
    # =======================
    "jazzmin",

    # =======================
    # DJANGO DEFAULT
    # =======================
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # =======================
    # THIRD-PARTY
    # =======================
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt.token_blacklist",
    "drf_yasg",

    # =======================
    # LOCAL APPS
    # =======================
    "users.apps.UsersConfig",
    "home.apps.HomeConfig",
    "ebooks.apps.EbooksConfig",
    "vocabulary.apps.VocabularyConfig",
    "lessons.apps.LessonsConfig",
    "subscriptions.apps.SubscriptionsConfig",
    "feedbacks.apps.FeedbacksConfig",

    # 🔐 ADMIN LOGS (YANGI)
    "admin_logs.apps.AdminLogsConfig",
]


# ==================================================
# MIDDLEWARE
# ==================================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    
    # 🌐 CORS Headers (frontend uchun)
    "corsheaders.middleware.CorsMiddleware",

    # 🌍 Nationality → language
    "users.middleware.NationalityMiddleware",

    # 🔐 ADMIN ACTION LOGGER (keyin yozamiz)
    "admin_logs.middleware.AdminActionLogMiddleware",

    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ==================================================
# URLS & WSGI
# ==================================================
ROOT_URLCONF = "suacademy_backend.urls"
WSGI_APPLICATION = "suacademy_backend.wsgi.application"


# ==================================================
# TEMPLATES
# ==================================================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# ==================================================
# DATABASE
# ==================================================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# ==================================================
# AUTH
# ==================================================
AUTH_USER_MODEL = "users.User"


# ==================================================
# INTERNATIONALIZATION
# ==================================================
USE_I18N = True
LANGUAGE_CODE = "uz"

LANGUAGES = [
    ("uz", "Uzbek"),
    ("ja", "Japanese"),
]

LOCALE_PATHS = [
    BASE_DIR / "locale",
]


# ==================================================
# AUTHENTICATION BACKENDS
# ==================================================
AUTHENTICATION_BACKENDS = [
    "users.backends.EmailOrUsernameBackend",
    "django.contrib.auth.backends.ModelBackend",
]


# ==================================================
# REST FRAMEWORK
# ==================================================
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.AllowAny",
    ),
}


# ==================================================
# JWT
# ==================================================
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}


# ==================================================
# SWAGGER
# ==================================================
SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": False,
    "SECURITY_DEFINITIONS": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Bearer <access_token>",
        }
    },
}


# ==================================================
# EMAIL (DEVELOPMENT vs PRODUCTION)
# ==================================================
if DEBUG:
    # Real email yuborish uchun (Gmail SMTP)
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_TIMEOUT = 10  # 10 soniyadan keyin timeout bo'ladi

DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "Su Academya <info@suacademya.uz>")

# FRONTEND
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")



# ==================================================
# STATIC & MEDIA
# ==================================================
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# ==================================================
# JAZZMIN CONFIG
# ==================================================
JAZZMIN_SETTINGS = {
    "site_title": "SU Academya Admin",
    "site_header": "SU Academya Administration",
    "site_brand": "SU Academya",
    "welcome_sign": "SU Academya boshqaruv paneliga xush kelibsiz",
    "show_sidebar": True,
    "navigation_expanded": True,

    "order_with_respect_to": [
        "users",
        "home",
        "ebooks",
        "vocabulary",
        "lessons",
        "subscriptions",
        "feedback",
        "admin_logs",
    ],

    "icons": {
        "users.User": "fas fa-user",
        "users.EmailOTP": "fas fa-envelope",

        "home.HomeIntro": "fas fa-home",
        "home.HomeSwiper": "fas fa-images",

        "ebooks.Book": "fas fa-book-open",

        "vocabulary.VocabularyTopic": "fas fa-book",
        "vocabulary.VocabularyWord": "fas fa-language",

        "lessons.Lesson": "fas fa-graduation-cap",
        "lessons.LessonFinished": "fas fa-check-circle",

        "subscriptions.SubscriptionPlan": "fas fa-credit-card",
        "subscriptions.UserSubscription": "fas fa-user-check",

        # 🔐 ADMIN LOGS ICON
        "admin_logs.AdminActionLog": "fas fa-user-shield",
        "feedback.Feedback": "fas fa-comment-dots",
    },
}


# ==================================================
# DEFAULT PK
# ==================================================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ==================================================
# CORS SETTINGS (Frontend uchun)
# ==================================================
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://suacademy-frontend.vercel.app",
    "https://suacademya.uz",
    "https://www.suacademya.uz",
]

CSRF_TRUSTED_ORIGINS = [
    "https://suacademy-frontend.vercel.app",
    "https://suacademy-backend.onrender.com",
    "https://suacademya.uz",
    "https://www.suacademya.uz",
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    "accept-language",
    "authorization",
    "content-type",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "token",  # Custom header for password reset
]


# ==================================================
# LOGGING
# ==================================================
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "users.backends": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}

