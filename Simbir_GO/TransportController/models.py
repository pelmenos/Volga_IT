from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Transport(models.Model):
    TRANSPORT_TYPE_CHOICES = [
        ('Car', 'Car'),
        ('Bike', 'Bike'),
        ('Scooter', 'Scooter')
    ]
    owner = models.ForeignKey(User, related_name='transports', on_delete=models.CASCADE)
    canBeRented = models.BooleanField()
    transportType = models.CharField(choices=TRANSPORT_TYPE_CHOICES, max_length=10)
    model = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    identifier = models.CharField(max_length=50)
    description = models.TextField(null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    minutePrice = models.FloatField(null=True)
    dayPrice = models.FloatField(null=True)

    def __str__(self):
        return self.model
