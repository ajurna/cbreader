"""
Django settings for cbreader project.
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv, dotenv_values

BASE_DIR = Path(__file__).parent.parent.parent

load_dotenv(Path(BASE_DIR, '.env'))
print(BASE_DIR)
print(dotenv_values())
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", None)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DJANGO_DEBUG', False) == 'True'

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost").split(",")


# Application definition

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "snowpenguin.django.recaptcha2",
    'bootstrap4',
    "comic",
    "comic_auth",
    'django_extensions',
    'imagekit',
)

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'csp.middleware.CSPMiddleware',
]

ROOT_URLCONF = "cbreader.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "cbreader.wsgi.application"


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {"default": dj_database_url.config(conn_max_age=500)}
else:
    DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": os.path.join(BASE_DIR, "db.sqlite3")}}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = "en-ie"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    Path(BASE_DIR, "static")
]

STATIC_ROOT = os.getenv('STATIC_ROOT', None)


MEDIA_ROOT = os.getenv('MEDIA_ROOT', None)

MEDIA_URL = '/media/'

LOGIN_REDIRECT_URL = "/comic/"

LOGIN_URL = "/login/"

UNRAR_TOOL = os.getenv("DJANGO_UNRAR_TOOL", None)

CBREADER_USE_RECAPTCHA = os.getenv("DJANGO_CBREADER_USE_RECAPTCHA", False)
RECAPTCHA_PRIVATE_KEY = os.getenv("DJANGO_RECAPTCHA_PRIVATE_KEY", '')
RECAPTCHA_PUBLIC_KEY = os.getenv("DJANGO_RECAPTCHA_PUBLIC_KEY", '')

COMIC_BOOK_VOLUME = Path(os.getenv("COMIC_BOOK_VOLUME"))

from .logger import LOGGING

SILK_ENABLED = False

USE_X_FORWARDED_HOST = os.getenv('USE_X_FORWARDED_HOST', False) == 'True'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

MYLAR_API_KEY = os.getenv('MYLAR_API_KEY', None)

BOOTSTRAP4 = {
    "javascript_url": {
        "url": "https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/js/bootstrap.bundle.min.js",
        "integrity": "sha384-Piv4xVNRyMGpqkS2by6br4gNJ7DXjqk09RmUpJ8jgGtD7zP9yug3goQfGII0yAns",
        "crossorigin": "anonymous",
    },
}
CSP_DEFAULT_SRC = ("'none'")
CSP_STYLE_SRC = ("'self'", 'cdn.jsdelivr.net', 'cdn.datatables.net')
CSP_IMG_SRC = ("'self'", "data:")
CSP_FONT_SRC = ("'self'")
CSP_SCRIPT_SRC = ("'self'", 'code.jquery.com', 'cdn.jsdelivr.net', 'cdn.datatables.net')
CSP_CONNECT_SRC = ("'self'")
CSP_INCLUDE_NONCE_IN = ['script-src']
CSP_SCRIPT_SRC_ATTR = ("'self'", "'unsafe-inline'")