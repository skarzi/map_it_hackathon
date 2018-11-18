from rest_framework import serializers

from . import models


class TransportEventSerializer(serializers.ModelSerializer):
    latlng = serializers.SerializerMethodField()
    desc = serializers.CharField(source='description')

    class Meta:
        model = models.TransportEvent
        fields = ('type', 'label', 'latlng', 'desc')

    def get_latlng(self, instance):
        return [instance.latitude, instance.longtitude]
