import json
import os

from datetime import datetime

from django.conf import settings
from django.db import migrations

from apps.transports.tasks.utils import is_in_circle


def load_bus_stops(apps, schema_editor):
    TransportType = apps.get_model('transports', 'TransportType')
    TransportEvent = apps.get_model('transports', 'TransportEvent')
    now = datetime.now()
    stop_type = TransportType.objects.get(name='stop')
    TransportEvent.objects.filter(type=stop_type).delete()
    with open(os.path.join(str(settings.APPS_DIR), 'shared', 'stops.json')) as f:
        stops_data = json.load(f)
    events = list()
    for data in stops_data:
        if is_in_circle((data['latitude'], data['longitude']), 5_500):
            events.append(TransportEvent(
                type=stop_type,
                latitude=data['latitude'],
                longtitude=data['longitude'],
                timestamp=now,
                description=data['name'],
            ))
    TransportEvent.objects.bulk_create(events)


class Migration(migrations.Migration):
    dependencies = [
        ('transports', '0003_auto_20181118_0420'),
    ]

    operations = [
        migrations.RunPython(load_bus_stops, migrations.RunPython.noop),
    ]
