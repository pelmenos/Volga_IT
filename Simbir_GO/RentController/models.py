from django.contrib.auth import get_user_model
from django.db import models

from TransportController.models import Transport

User = get_user_model()


class Rent(models.Model):
    RENT_TYPE_CHOICES = [
        ('Minutes', 'Minutes'),
        ('Days', 'Days')
    ]
    renter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rents')
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE, related_name='rents')
    priceType = models.CharField(choices=RENT_TYPE_CHOICES, max_length=10)
    priceOfUnit = models.FloatField()
    finalPrice = models.FloatField(null=True, default=0)
    timeStart = models.DateTimeField(auto_now_add=True)
    timeEnd = models.DateTimeField(null=True)
