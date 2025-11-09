from pathlib import Path
from celery.schedules import crontab
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() == "true"

# Set these for your live host(s)
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",") if os.getenv("DJANGO_ALLOWED_HOSTS") else []
CSRF_TRUSTED_ORIGINS = os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",") if os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS") else []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "ip_tracking",
    # Swagger (if you expose /swagger/)
    "rest_framework",
    "drf_yasg",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "ip_tracking.middleware.IPLoggingMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "alx_backend_security.urls"

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

WSGI_APPLICATION = "alx_backend_security.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

# Internationalization / Timezone
LANGUAGE_CODE = "en-us"
TIME_ZONE = os.getenv("DJANGO_TIME_ZONE", "UTC")
USE_I18N = True
USE_TZ = True

# Static / Media
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"   # required for collectstatic in prod
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Ratelimit
RATELIMIT_ENABLE = True
# Remove RATELIMIT_VIEW unless you point it to a callable. Use @ratelimit(..., block=True) on views.

# Celery
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")          # e.g. amqps://... from CloudAMQP
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "rpc://")
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_ALWAYS_EAGER = False
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

CELERY_BEAT_SCHEDULE = {
    "detect-anomalies-hourly": {
        "task": "ip_tracking.tasks.detect_anomalies",
        "schedule": crontab(minute=0),  # every hour
    },
}
