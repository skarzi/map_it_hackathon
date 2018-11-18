from django.contrib.postgres.fields import JSONField
from django.db import models


class TransportType(models.Model):
    name = models.CharField(max_length=127)
    icon = models.ImageField(upload_to='icons')

    def __str__(self):
        return self.name


class TransportEvent(models.Model):
    type = models.ForeignKey(
        TransportType,
        related_name='events',
        on_delete=models.CASCADE,
    )
    timestamp = models.DateTimeField()
    latitude = models.FloatField()
    longtitude = models.FloatField()
    label = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    data = JSONField(default={})
