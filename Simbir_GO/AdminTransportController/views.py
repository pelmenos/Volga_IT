from rest_framework import generics

from TransportController.models import Transport
from TransportController.serializers import TransportSerializer
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAdmin


class TransportListCreate(generics.ListCreateAPIView):
    queryset = Transport.objects.all()
    serializer_class = TransportSerializer
    permission_classes = (IsAuthenticated, IsAdmin)

    def get_queryset(self):
        queryset = self.queryset
        start = int(self.request.query_params.get('start') or 0)
        count = int(self.request.query_params.get('count') or 0)
        transport_type = self.request.query_params.get('transportType') or None

        if transport_type:
            queryset = queryset.filter(transportType=transport_type)

        if start and count:
            query_set = queryset[start:start+count]
        elif start:
            query_set = queryset[start:]
        elif count:
            query_set = queryset[:count]
        else:
            query_set = queryset[:]

        return query_set

    def perform_create(self, serializer):
        try:
            serializer.save(owner_id=self.request.data.get('ownerId'))
        except Exception:
            raise NotFound({'message': 'Owner with this id not found!'})


class TransportDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transport.objects.all()
    serializer_class = TransportSerializer
    permission_classes = (IsAuthenticated, IsAdmin)
