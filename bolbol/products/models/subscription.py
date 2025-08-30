from django.db import models
from django.utils import timezone
from datetime import timedelta


class Subscription(models.Model):
    subscription_name = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    availability_time = models.DurationField()
    
    def __str__(self):
        return self.subscription_name
