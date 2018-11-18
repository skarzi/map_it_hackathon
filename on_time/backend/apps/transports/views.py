from rest_framework import (
    mixins,
    viewsets,
)
from rest_framework.response import Response

from . import (
    models,
    serializers,
)


class TransportEventsViewSet(
        mixins.ListModelMixin,
        viewsets.GenericViewSet,
):
    serializer_class = serializers.TransportEventSerializer

    def get_queryset(self):
        return models.TransportEvent.objects.all().defer('timestamp', 'data')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        events = self.drop_too_closest(list(queryset))
        serializer = self.get_serializer(events, many=True)
        return Response({'objects': serializer.data})

    def drop_too_closest(self, events):
        cleaned_events = set()
        for event0 in events:
            if event0.type_id == 6:
                cleaned_events.add(event0)
                continue

            for event1 in cleaned_events:
                if (
                        event0 in cleaned_events
                        or self.is_too_close(event0, event1)
                ):
                    break
            else:
                cleaned_events.add(event0)
        return cleaned_events


    def is_too_close(self, event0, event1):
        return (
            event0.type_id == event1.type_id
            and (
                abs(event1.latitude - event0.latitude) < 0.0002
                or abs(event1.longtitude - event0.longtitude) < 0.0002
            )
        )
