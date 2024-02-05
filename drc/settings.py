"""
Django settings for drc project.

Generated by 'django-admin startproject' using Django 4.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-06ei#444!q7-!_hf8jzyrygqve1$*r)346ize$v$onc=a%nl(5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'authentication.User'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'storages',

    'drc.apps.authentication',
    'drc.apps.authentication.apps',
    'drc.apps.core',
    'drc.apps.profiles',
    'drc.apps.follow',
    'drc.apps.recipes',
    'drc.apps.likes',
    'drc.apps.saves',
    'drc.apps.cooked',
    'drc.apps.completed_instructions',
    'drc.apps.notes',
    'drc.apps.curated_collections',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'drc.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'drc.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'recipe_app_api_refresh_database_1',
        'USER': 'nashlomeli',
        'PASSWORD': 'password',
        'HOST': 'recipe-app-api-refresh-database-1.cxi6am64c46v.us-east-2.rds.amazonaws.com',
        'PORT': '5432',
    }
}

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'drc.apps.core.exceptions.core_exception_handler',
    'NON_FIELD_ERRORS_KEY': 'error',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'drc.apps.authentication.backends.JWTAuthentication',
    ),
}

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        # "OPTIONS": {
        #     "AWS_ACCESS_KEY_ID": 'AKIA5FTZC3FKLTBAORXM',
        #     "AWS_SECRET_ACCESS_KEY": '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',
        #     "AWS_STORAGE_BUCKET_NAME": 'recipe-app-api-refresh-recipe-images-1',

        #     "AWS_S3_FILE_OVERWRITE": False,
        # },
    },
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AWS_ACCESS_KEY_ID = 'AKIA5FTZC3FKLTBAORXM'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'recipe-app-api-refresh-recipe-images-1'

AWS_S3_FILE_OVERWRITE = False
# AWS_DEFAULT_ACL = None
