from django.db import models
from django.db.models import Sum
from vehicles.models import Vehicle
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, date, timedelta
from django.contrib.auth import get_user_model
from fuellog.models import FuelEntry
User = get_user_model()

# Create your models here.

class ServiceRecord(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='vehicle')
    date = models.DateField(blank=True, null=True)
    servicer = models.CharField(blank=True, max_length=100)
    invoice = models.CharField(blank=True, max_length=100)
    cost = models.DecimalField(decimal_places=2, max_digits=7, blank=True, default='0')
    mileage = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.vehicle.name

    def get_absolute_url(self):
        return reverse('service:record_detail', kwargs={'pk': self.pk})

    @property
    def is_completed(self):
        return self.completed == True

    @property
    def is_scheduled(self):
        return self.completed == False
    
    @property
    def is_past_due(self):
        return date.today() > self.date

    @property
    def is_past_mileage(self):
        return self.vehicle.current_mileage > self.mileage

    @property
    def miles_due_soon(self):
        return self.vehicle.five_hundred_miles > self.mileage

    @property
    def date_due_soon(self):
        ninety_days = (date.today()+timedelta(days=90)).isoformat()
        return self.date.isoformat() <= ninety_days
    





