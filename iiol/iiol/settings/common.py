from datetime import timedelta
from pathlib import Path
import os
from os.path import abspath, dirname
from django.contrib.messages import constants as messages
from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv


# Build paths inside the project like this: BASE_DIR / 'subdir'.

# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = dirname(dirname(dirname(abspath(__file__))))
dotenv_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path)

FORCE_SCRIPT_NAME = os.environ.get('MY_URL_PREFIX')
ACCESS_FROM = os.environ.get('ACCESS_FROM')
print(f"ACCESS  {ACCESS_FROM}, Serviced on Prefix : {FORCE_SCRIPT_NAME}")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

if os.environ.get('TARGET_ENV').lower() == 'prod':
    DEBUG = False
else:
    DEBUG = True


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', 'thecloudpark.xyz', '192.168.0.2']


# Application definition

INSTALLED_APPS = [
    # Django Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'rest_framework',    # Third Apps
    'rest_framework_simplejwt',
    'django_bootstrap5',
    'debug_toolbar',
    'drf_yasg',
    # Myapps
    'iiol',
    'accounts',
    'barcode',
    'library',
    'books',
    'mybookwishlist',
]


MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'iiol.urls'

CACHE_TTL = 60 * 60 * 24  # 24h

if ACCESS_FROM == 'outside':
    redis_location = 'redis://thecloudpark.xyz:16379'
else:
    redis_location = 'redis://192.168.0.10:6379'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': redis_location,
        'KEY_PREFIX': 'D_CACHE',
    },
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'iiol', 'templates')
        ],
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

WSGI_APPLICATION = 'iiol.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if ACCESS_FROM == 'outside':
    DB_HOST = 'thecloudpark.xyz'
    DB_PORT = '15432'
else:
    DB_HOST = '192.168.0.10'
    DB_PORT = '5432'

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'iiol',
        'USER': 'django_user',
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}

AUTH_USER_MODEL = "accounts.User"

REST_FRAMEWORK = {
	'PAGE_SIZE' : 10,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_PERMISSION_CLASSES' : [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
        'iiol.authentication.JWTCookieAuthentication',
    ],
    'DEFAULT_THROTTLE_CLASSES' : [
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES' : {
        'anon' : '500/hour',
        'user' : '3/sec',
    }
}

if ACCESS_FROM == 'outside':
    COOKIE_DOMAIN = None
else:
    COOKIE_DOMAIN = 'thecloudpark.xyz'

SIMPLE_JWT = {
    'AUTH_COOKIE': 'access_token',  # Cookie name. Enables cookies if value is set.
    'AUTH_COOKIE_DOMAIN': COOKIE_DOMAIN,     # A string like "example.com", or None for standard domain cookie.
    'AUTH_COOKIE_SECURE': True,    # Whether the auth cookies should be secure (https:// only).
    'AUTH_COOKIE_HTTP_ONLY' : True, # Http only cookie flag.It's not fetch by javascript.
    'AUTH_COOKIE_PATH': f'{FORCE_SCRIPT_NAME}/accounts/token/',        # The path of the auth cookie.
    'AUTH_COOKIE_SAMESITE': 'Lax',  # Whether to set the flag restricting cookie leaks on cross-site requests.
                                    # This can be 'Lax', 'Strict', or None to disable the flag.
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=20),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=5),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

INTERNAL_IPS = ['127.0.0.1']
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

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


STATIC_URL = f'{FORCE_SCRIPT_NAME}/static/'
# STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'iiol', 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, '.static_root')
#
MEDIA_URL = f'/{FORCE_SCRIPT_NAME}/media/'
# MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CSRF_TRUSTED_ORIGINS = ['https://thecloudpark.xyz']
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_REDIRECT_URL = f'{FORCE_SCRIPT_NAME}/mybookwishlist/mylist'

CELERY_ALWAYS_EAGER = True
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TAST_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Seoul'
