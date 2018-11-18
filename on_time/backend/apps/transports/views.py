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
        queryset = models.TransportEvent.objects.all()
        queryset = queryset.select_related('type')
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({'objects': serializer.data})
