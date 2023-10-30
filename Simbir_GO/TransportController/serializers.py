from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Transport


class TransportSerializer(ModelSerializer):
    ownerId = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Transport
        fields = ['id', 'ownerId', 'canBeRented', 'transportType', 'model', 'color', 'identifier', 'description', 'latitude', 'longitude',
                  'minutePrice', 'dayPrice']
