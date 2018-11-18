from datetime import datetime

from django.conf import settings

import celery
import requests

from apps.adapters import bustram
from apps.taskapp.celery import app

from .. import models


@app.task
def fetch_bustram_data(type_):
    bustram_client = bustram.BusTramSdk(settings.BUSTRAM_API_KEY)
    transport_type = models.TransportType.objects.get(name=type_)
    # delete historical data
    models.TransportEvent.objects.filter(type=transport_type).delete()

    type_name = 'Autobus' if type_ == 'bus' else 'Tramwaj'
    transport_events = list()
    for data in bustram_client.get_by_type(type_):
        transport_events.append(
            models.TransportEvent(
                type=transport_type,
                timestamp=datetime.strptime(
                    data['Time'],
                    settings.BUSTRAM_DATETIME_FORMAT,
                ),
                latitude=data['Lat'],
                longtitude=data['Lon'],
                label=data['Lines'],
                description=(
                    f"{type_name} nr. {data['Lines']}, Brygada nr. "
                    f"{data['Brigade']}.\n"
                    f"Dane z godziny: {data['Time'].split(' ', 1)[-1]}."
                )
            )
        )
    models.TransportEvent.objects.bulk_create(transport_events)


@app.task
def fetch_all_bustram_data():
    group = celery.group(
        fetch_bustram_data.s('bus'),
        fetch_bustram_data.s('tram'),
    )
    group.delay()
