from datetime import datetime

import celery

from apps.adapters import nextbike
from apps.taskapp.celery import app

from .. import models


@app.task
def fetch_nextbike_data():
    nextbike_client = nextbike.NextBikeSdk()
    transport_type = models.TransportType.objects.get(name='bike')
    # delete historical data
    models.TransportEvent.objects.filter(type=transport_type).delete()

    transport_events = list()
    now = datetime.now()
    hour = now.strftime('%H:%M:%S')
    for data in nextbike_client.bikes():
        if 'number' not in data:
            continue
        transport_events.append(
            models.TransportEvent(
                type=transport_type,
                timestamp=now,
                latitude=data['lat'],
                longtitude=data['lng'],
                label=data['name'],
                description=(
                    f"Stacja numer {data['number']}\n"
                    f"{data['name']}\n\n"
                    f"Dostępne rowery: {data['bikes']}\n"
                    f"Wolne stojaki: {data['free_racks']}\n"
                    f'Dane z godziny: {hour}.'
                )
            )
        )
    models.TransportEvent.objects.bulk_create(transport_events)
