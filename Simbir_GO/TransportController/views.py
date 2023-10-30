from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .models import Transport
from .permissions import IsOwnerOrReadOnly
from .serializers import TransportSerializer


class CreateTransport(generics.CreateAPIView):
    queryset = Transport.objects.all()
    serializer_class = TransportSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TransportDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transport.objects.all()
    serializer_class = TransportSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
