from datetime import datetime

from django.db import transaction

import pytz

from apps.adapters import nextbike
from apps.taskapp.celery import app

from .. import models
from .utils import is_in_circle


@app.task
def fetch_nextbike_data():
    nextbike_client = nextbike.NextBikeSdk()
    transport_type = models.TransportType.objects.get(name='bike')
    with transaction.atomic():
        models.TransportEvent.objects.filter(type=transport_type).delete()

    transport_events = list()
    timezone = pytz.timezone('Europe/Warsaw')
    now = datetime.now(timezone)
    hour = now.strftime('%H:%M:%S')
    for data in nextbike_client.bikes():
        if 'number' not in data:
            continue
        if is_in_circle((data['lat'], data['lng'])):
            transport_events.append(
                models.TransportEvent(
                    type=transport_type,
                    timestamp=now,
                    latitude=data['lat'],
                    longtitude=data['lng'],
                    description=(
                        f"Stacja numer {data['number']}\n"
                        f"{data['name']}\n\n"
                        f"Dostępne rowery: {data['bikes']}\n"
                        f"Wolne stojaki: {data['free_racks']}\n"
                        f'Dane z godziny: {hour}.'
                    )
                )
            )
    with transaction.atomic():
        models.TransportEvent.objects.bulk_create(transport_events)
