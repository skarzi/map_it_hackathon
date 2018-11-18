from datetime import datetime

from django.db import transaction

import pytz

from apps.adapters import traficar
from apps.taskapp.celery import app

from .. import models
from .utils import is_in_circle


@app.task
def fetch_traficar_data():
    traficar_client = traficar.TraficarSdk()
    transport_type = models.TransportType.objects.get(name='traficar')
    with transaction.atomic():
        models.TransportEvent.objects.filter(type=transport_type).delete()

    timezone = pytz.timezone('Europe/Warsaw')
    now = datetime.now(timezone)
    hour = now.strftime('%H:%M:%S')
    transport_events = list()
    for data in traficar_client.cars():
        if is_in_circle((data['latitude'], data['longitude'])):
            transport_events.append(
                models.TransportEvent(
                    type=transport_type,
                    timestamp=now,
                    latitude=data['latitude'],
                    longtitude=data['longitude'],
                    description=(
                        f"{data['model']} - {data['regNumber']}\n\n"
                        f"Stan paliwa: {data['fuel']} l.\n"
                        f'Dane z godziny: {hour}'
                    )
                )
            )
    with transaction.atomic():
        models.TransportEvent.objects.bulk_create(transport_events)
