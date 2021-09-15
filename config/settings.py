from pathlib import Path

from environs import Env

env = Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str(
    "SECRET_KEY", "django-insecure-v&k135eg$wz=b+pr6h6^=uw0xzmi)qvjakzr=m1x-)2mg@4cmj"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG", False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", ["*"], str)


# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
]

EXTERNAL_APPS = [
    "drf_spectacular",
    "rest_framework",
]

PROJECT_APPS = [
    "apps.users",
]

INSTALLED_APPS = [
    # This is special: This ensures we are running with minimum differences between development and
    # production environments. Whitenoise serves static files for us.
    "whitenoise.runserver_nostatic",
    *DJANGO_APPS,
    *EXTERNAL_APPS,
    *PROJECT_APPS,
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

FRONTEND_DIST_DIR = BASE_DIR / "frontend" / "dist" / "frontend"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
        "DIRS": [
            FRONTEND_DIST_DIR,
        ],
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": env.dj_db_url(
        "DATABASE_URL",
        "sqlite:///{sqlite_db_file}".format(
            sqlite_db_file=BASE_DIR / "var" / "db.sqlite3",
        ),
    ),
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = False

USE_L10N = False

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
if not DEBUG:
    # Serve the frontend application only in production, not in local development.
    WHITENOISE_ROOT = FRONTEND_DIST_DIR
STATIC_ROOT = env.str(
    "STATIC_FILES_DIR",
    str(BASE_DIR / "var" / "staticfiles"),
)


# Uploaded files settings:
if not DEBUG:
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    AWS_S3_ENDPOINT_URL = env.str("S3_ENDPOINT_URL", None)
    AWS_ACCESS_KEY_ID = env.str("AWS_ACCESS_KEY_ID", None)
    AWS_SECRET_ACCESS_KEY = env.str("AWS_SECRET_KEY", None)
else:
    MEDIA_ROOT = env.str(
        "UPLOADED_FILES_DIR",
        str(BASE_DIR / "var" / "media"),
    )
    MEDIA_URL = "/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Custom user model definition:
AUTH_USER_MODEL = "users.user"

REST_FRAMEWORK = {
    # YOUR SETTINGS
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {"COMPONENT_SPLIT_REQUEST": True}
