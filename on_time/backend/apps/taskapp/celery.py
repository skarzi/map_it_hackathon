import os

from django.apps import (
    AppConfig,
    apps,
)
from django.conf import settings

from celery import Celery

if not settings.configured:
    # set the default Django settings module for the 'celery' program.
    os.environ.setdefault(
        'DJANGO_SETTINGS_MODULE',
        'config.settings.local',
    )


app = Celery('on_time')


class CeleryConfig(AppConfig):
    name = 'apps.taskapp'
    verbose_name = 'Celery Config'

    def ready(self):
        app.config_from_object('django.conf:settings', namespace="CELERY")
        installed_apps = [
            app_config.name for app_config in apps.get_app_configs()
        ]
        app.autodiscover_tasks(lambda: installed_apps, force=True)


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
