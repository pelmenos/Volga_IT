from django.utils import timezone
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from TransportController.models import Transport
from TransportController.serializers import TransportSerializer

from .exceptions import NotSpecified
from .models import Rent
from .permissions import IsRenter, IsTransportOwner
from .serializers import RentSerializer


class RentTransportList(generics.ListAPIView):
    queryset = Transport.objects.all()
    serializer_class = TransportSerializer

    def get_queryset(self):
        queryset = self.queryset
        lat = self.request.query_params.get('lat')
        long = self.request.query_params.get('long')
        radius = self.request.query_params.get('radius')
        transport_type = [self.request.query_params.get('type')]

        if not transport_type[0]:
            raise NotSpecified({'message': 'The "type" must be specified'})
        if not lat:
            raise NotSpecified({'message': 'The "lat" must be specified'})
        if not long:
            raise NotSpecified({'message': 'The "long" must be specified'})
        if not radius:
            raise NotSpecified({'message': 'The "radius" must be specified'})

        if transport_type[0] == 'All':
            transport_type = ['Car', 'Bike', 'Scooter']
        lat, long, radius = float(lat), float(long), float(radius)
        query_set = queryset.filter(longitude__range=(long-radius, long+radius),
                                    latitude__range=(lat-radius, lat+radius),
                                    transportType__in=transport_type,
                                    canBeRented=True)
        return query_set


class RetrieveRent(generics.RetrieveAPIView):
    queryset = Rent.objects.all()
    serializer_class = RentSerializer
    permission_classes = (IsAuthenticated, IsRenter | IsTransportOwner)


class UserRentHistoryList(generics.ListAPIView):
    queryset = Rent.objects.all()
    serializer_class = RentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(renter=self.request.user)


class TransportRentHistoryList(generics.ListAPIView):
    queryset = Rent.objects.all()
    serializer_class = RentSerializer
    permission_classes = (IsAuthenticated, IsTransportOwner)

    def get_queryset(self):
        query_set = self.queryset.filter(transport_id=self.kwargs['pk'])
        return query_set


class CreateRent(APIView):
    permission_classes = (IsAuthenticated,)

    def get_price(self, priceType, pk):
        try:
            transport = Transport.objects.get(id=pk)
        except Exception:
            raise NotFound()
        if priceType == 'Minutes':
            return transport.minutePrice
        else:
            return transport.dayPrice

    def post(self, request, pk):
        user = request.user
        rent_type = self.request.query_params.get('rentType')
        price = self.get_price(rent_type, pk)
        if user.transports.filter(id=pk).exists():
            return Response({'message': 'You can`t rent your own transport'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = RentSerializer(data={'renter': user.id, 'transport': pk,
                                          'priceType': rent_type, 'priceOfUnit': price})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EndRent(APIView):
    permission_classes = (IsAuthenticated, IsRenter)

    def get_rent(self, pk):
        try:
            return Rent.objects.get(id=pk)
        except Exception:
            raise NotFound()

    def post(self, request, pk):
        lat = self.request.query_params.get('lat')
        long = self.request.query_params.get('long')
        rent = self.get_rent(pk)
        if not lat:
            raise NotSpecified({'message': 'The "lat" must be specified'})
        if not long:
            raise NotSpecified({'message': 'The "long" must be specified'})
        rent.timeEnd = timezone.now()
        rent.transport.longitude = long
        rent.transport.latitude = lat
        if rent.priceType == 'Minutes':
            time = (rent.timeEnd.minute - rent.timeStart.minute) or 1
            price = time * rent.priceOfUnit
        else:
            time = (rent.timeEnd.day - rent.timeStart.day) or 1
            price = time * rent.priceOfUnit
        rent.finalPrice = price
        rent.transport.save()
        rent.save()
        serializer = RentSerializer(rent)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
