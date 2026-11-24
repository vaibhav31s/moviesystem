"""Django settings for MovieFlex.

Configured through environment variables (see .env.example). The app has no
database models, so it runs without a database (handy on Vercel, where the
filesystem is read-only).
"""
import os
import warnings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(name, default=False):
    return os.environ.get(name, str(default)).strip().lower() in {"1", "true", "yes", "on"}


DEBUG = env_bool("DJANGO_DEBUG", False)

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "")
if not SECRET_KEY:
    if not DEBUG:
        raise RuntimeError("Set DJANGO_SECRET_KEY (or DJANGO_DEBUG=true for local development).")
    SECRET_KEY = "dev-only-insecure-key"

ALLOWED_HOSTS = ["localhost", "127.0.0.1", ".vercel.app"] + [
    h.strip() for h in os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",") if h.strip()
]
CSRF_TRUSTED_ORIGINS = [
    o.strip() for o in os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",") if o.strip()
] + ["https://*.vercel.app"]

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "trial",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "moviesystem.framing.FrameAncestorsMiddleware",
]

ROOT_URLCONF = "moviesystem.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "template"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "moviesystem.wsgi.application"

DATABASES = {}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = False
USE_TZ = True

# Static files are served by WhiteNoise straight from static/ (no collectstatic
# step needed, which keeps the Vercel build simple).
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
WHITENOISE_USE_FINDERS = True
WHITENOISE_MAX_AGE = 3600
# STATIC_ROOT only exists after collectstatic; WhiteNoise serves from finders otherwise.
warnings.filterwarnings("ignore", message="No directory at", module="whitenoise.base")

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_CONTENT_TYPE_NOSNIFF = True
CSRF_COOKIE_SECURE = not DEBUG

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "WARNING"},
}

# Sites allowed to show this app in an iframe (portfolio live previews); all others are blocked.
FRAME_ANCESTORS = ["'self'", "https://vaibhavgawad.com", "https://www.vaibhavgawad.com"]
