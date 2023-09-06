from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^)27yaph#4*r&e!@0r02bp7@mz!xolaxsvd%j8h_)4i88#ooyh'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['13.235.65.146', 'saeedrila.dev', 'www.saeedrila.dev', 'localhost', '127.0.0.1', 'https://saeedrila.dev/']


# Application definition

INSTALLED_APPS = [
#Default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

#Google auth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

#Project apps
    'auth_app',
    'product_app',
    'order_app',
    'report_app',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'deskly_2.urls'

import os

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

# Very important#
AUTH_USER_MODEL = 'auth_app.Account'

WSGI_APPLICATION = 'deskly_2.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'deskly_2',
        'USER': 'postgres',
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
if os.environ.get('SERVER_SOFTWARE', '').startswith('nginx'):
    # Running on the server
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'assets')
else:
    # Running locally
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'assets')
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static')
    ]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#Razorpay Payment Configuration
KEY = 'rzp_test_WGlv594z1DLEPO'
SECRET = 'rSzkwzdBivOZmQK0xu4q3UeD'


SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': '25014805493-0ci9d3qsdr2iuekfmtaj3g8ohhpdmqd7.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        }
    }
}

LOGIN_REDIRECT_URL = 'home'
