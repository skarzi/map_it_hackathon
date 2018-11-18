"""
Base settings for on_time project.
For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
import logging

from itertools import chain

import environ

logger = logging.getLogger(__name__)

# (on_time/backend/config/settings/base.py - 3 = on_time/backend)
# or inside docker container - `/app`
APPS_DIR = environ.Path(__file__) - 3

# Load operating system environment variables and then prepare to use them
env = environ.Env()

# .env file, should load only in development environment
READ_DOT_ENV_FILE = env.bool('DJANGO_READ_DOT_ENV_FILE', default=False)

if READ_DOT_ENV_FILE:
    # Operating System Environment variables have precedence over variables
    # defined in the .env file, that is to say variables from the .env files
    # will only be used if not defined as OS environment variables.
    env_file = str(APPS_DIR.path('.env'))
    logger.info(f'Loading: {env_file}')
    env.read_env(env_file)
    logger.info(
        'The .env file has been loaded. See base.py for more information.'
    )


# APPS
# -----------------------------------------------------------------------------
DJANGO_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.admin',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'corsheaders',
]

LOCAL_APPS = [
    'apps.transports.apps.TransportsConfig',
]

# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = list(chain(
    DJANGO_APPS,
    THIRD_PARTY_APPS,
    LOCAL_APPS,
))


# MIDDLEWARE
# -----------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# MIGRATIONS
# -----------------------------------------------------------------------------
MIGRATION_MODULES = {
    'sites': 'apps.contrib.sites.migrations'
}


# DEBUG
# -----------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool('DJANGO_DEBUG', False)


# FIXTURE
# -----------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
    str(APPS_DIR.path('shared/fixtures')),
)


# EMAIL
# -----------------------------------------------------------------------------
# EMAIL_BACKEND = env(
#     'DJANGO_EMAIL_BACKEND',
#     default='django.core.mail.backends.smtp.EmailBackend',
# )
# EMAIL_PORT = env('EMAIL_PORT')
# EMAIL_HOST = env('EMAIL_HOST')
# EMAIL_HOST_USER = env('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
# EMAIL_USE_TLS = env('EMAIL_USE_TLS')


# MANAGER
# -----------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
# ADMINS = [
#     ("""{{cookiecutter.author_name}}""", '{{cookiecutter.email}}'),
# ]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
# MANAGERS = ADMINS


# DATABASE
# -----------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
# Uses django-environ to accept URI format
# https://django-environ.readthedocs.io/en/latest/#supported-types
DATABASES = {
    'default': {
        'ENGINE': env(
            'POSTGRES_ENGINE',
            default='django.db.backends.postgresql',
        ),
        'NAME': env('POSTGRES_DB', default='127.0.0.1'),
        'USER': env('POSTGRES_USER', default='postgres'),
        'PASSWORD': env('POSTGRES_PASSWORD', default=None),
        'HOST': env('POSTGRES_HOST', default='localhost'),
        'PORT': env.int('POSTGRES_PORT', default=5430),
        'ATOMIC_REQUESTS': True,
    },
}
DATABASES['default']['ATOMIC_REQUESTS'] = True


# LOCALES
# -----------------------------------------------------------------------------
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'UTC'
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'
# LANGUAGES = (
# )
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = False


# TEMPLATES
# -----------------------------------------------------------------------------
#  https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        'DIRS': [
            str(APPS_DIR.path('shared/templates')),
        ],
        'OPTIONS': {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            'debug': DEBUG,
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# STATIC
# -----------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(APPS_DIR('shared/static'))
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [
]
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]


# MEDIA
# -----------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR('shared/media'))
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'


# URLS
# -----------------------------------------------------------------------------
ROOT_URLCONF = 'config.urls'


# HTTP
# -----------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'config.wsgi.application'
APPEND_SLASH = True


# PASSWORD STORAGES
# -----------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]


# PASSWORD VALIDATION
# -----------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation'
            '.UserAttributeSimilarityValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.MinimumLengthValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.CommonPasswordValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.NumericPasswordValidator'
        ),
    },
]


# AUTHENTICATION
# -----------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]
# AUTH_USER_MODEL = 'users.User'
# LOGIN_REDIRECT_URL = 'users:redirect'
# LOGIN_URL = 'account_login'


# SLUGLIFIER
# -----------------------------------------------------------------------------
# AUTOSLUG_SLUGIFY_FUNCTION = 'slugify.slugify'


# ADMIN
# -----------------------------------------------------------------------------
# Use `{% raw %}{% url 'admin:index' %}{% endraw %}` in templates.
# ADMIN_URL = r'^admin/'


# REST FRAMEWORK
# -----------------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
    ),
    'DEFAULT_PAGINATION_CLASS': None,
    'SEARCH_PARAM': 'search',
    'ORDERING_PARAM': 'ordering',
    'COERCE_DECIMAL_TO_STRING': True,
}


# CELERY
# -----------------------------------------------------------------------------
from celery.schedules import crontab

INSTALLED_APPS.append(
    'apps.taskapp.celery.CeleryConfig',
)

if USE_TZ:
    CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='django://')
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERYD_TASK_TIME_LIMIT = 5 * 60
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-soft-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERYD_TASK_SOFT_TIME_LIMIT = 60
CELERY_BEAT_SCHEDULE = {
    'fetch-bustram-data': {
        'task': 'apps.transports.tasks.bustram.fetch_all_bustram_data',
        'schedule': 10,  # schedule every 10 seconds
    },
    'fetch-nexbike-data': {
        'task': 'apps.transports.tasks.nextbike.fetch_nextbike_data',
        'schedule': 90,  # schedule every 1 minute
    },
    'fetch-traficar-data': {
        'task': 'apps.transports.tasks.traficar.fetch_traficar_data',
        'schedule': 30,  # schedule every 1 minute
    },
}

# DJANGO CORS
# -----------------------------------------------------------------------------
ALLOWED_HOSTS = ['192.168.43.231','localhost', '127.0.0.1', '0.0.0.0']
CORS_ORIGIN_ALLOW_ALL = True


# PROJECT SETTINGS
# -----------------------------------------------------------------------------
BUSTRAM_API_KEY = '0ff9826d-f5b2-4826-ae51-05d516d5991a'
BUSTRAM_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
