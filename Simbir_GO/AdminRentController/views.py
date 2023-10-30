from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView

from RentController.models import Rent
from RentController.serializers import RentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsAdmin
from RentController.exceptions import NotSpecified

User = get_user_model()


class RentDetail(RetrieveUpdateDestroyAPIView):
    queryset = Rent.objects.all()
    serializer_class = RentSerializer
    permission_classes = (IsAuthenticated, IsAdmin)


class UserRentHistory(ListAPIView):
    queryset = Rent.objects.all()
    serializer_class = RentSerializer
    permission_classes = (IsAuthenticated, IsAdmin)

    def get_queryset(self):
        try:
            return self.queryset.filter(renter_id=self.kwargs['pk'])
        except Exception:
            raise NotFound({'message': 'Renter with this id not found'})


class TransportRentHistory(ListAPIView):
    queryset = Rent.objects.all()
    serializer_class = RentSerializer
    permission_classes = (IsAuthenticated, IsAdmin)

    def get_queryset(self):
        try:
            return self.queryset.filter(transport_id=self.kwargs['pk'])
        except Exception:
            raise NotFound({'message': 'Transport with this id not found'})


class CreateRent(CreateAPIView):
    queryset = Rent.objects.all()
    serializer_class = RentSerializer
    permission_classes = (IsAuthenticated, IsAdmin)


class EndRent(APIView):
    permission_classes = (IsAuthenticated, IsAdmin)

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
