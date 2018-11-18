"""
Local settings for on_time project.
"""
import socket

from .base import *  # noqa

# DEBUG
# -----------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', default=True)


# TEMPLATES
# -----------------------------------------------------------------------------
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG


# SECRET KEY
# -----------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env('DJANGO_SECRET_KEY', default='CHANGEME!!!')


# EMAIL
# -----------------------------------------------------------------------------
# EMAIL_PORT = 1025
# EMAIL_HOST = 'localhost'
# EMAIL_BACKEND = env(
#     'DJANGO_EMAIL_BACKEND',
#     default='django.core.mail.backends.console.EmailBackend',
# )


# CACHE
# -----------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}


# STATIC
# ----------------------------------------------------------------------------
STATIC_ROOT = None
STATICFILES_DIRS = [
    str(APPS_DIR('shared/static'))
]


# DJANGO DEBUG TOOLBAR
# -----------------------------------------------------------------------------
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
INSTALLED_APPS += ['debug_toolbar',]
INTERNAL_IPS = ['127.0.0.1', '10.0.2.2']
# tricks to have debug toolbar when developing with docker
ip = socket.gethostbyname(socket.gethostname())
INTERNAL_IPS += [ip[:-1] + '1']
DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}


# DJANGO EXTENSIONS
# -----------------------------------------------------------------------------
INSTALLED_APPS += ['django_extensions']


# CELERY
# -----------------------------------------------------------------------------
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True


# PROJECT SETTINGS
# -----------------------------------------------------------------------------
IPYTHON_ARGUMENTS = [
    '--TerminalInteractiveShell.editing_mode=vi',
    '--TerminalInteractiveShell.editor=vim',
]

