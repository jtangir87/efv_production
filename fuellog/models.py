from django.db import models
from vehicles.models import Vehicle
from django.urls import reverse
from django.db.models.signals import post_save
from datetime import datetime
from django.contrib.auth import get_user_model
from django.db.models import Sum
User = get_user_model()

# Create your models here.
class FuelEntry(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    fuel_choices = (
        ('EMPTY', 'Empty'),
        ('1/8', '1/8'),
        ('1/4', '1/4'),
        ('1/2', '1/2'),
        ('3/4', '3/4'),
        ('FULL', 'Full'),
    )
    current = models.CharField(max_length=5, choices=fuel_choices)
    after = models.CharField(max_length=5, choices=fuel_choices, blank=True)
    gallons = models.DecimalField(decimal_places=2, max_digits=5, blank=True, default='0')
    cost = models.DecimalField(decimal_places=2, max_digits=5, blank=True, default='0')
    mileage = models.IntegerField(blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date', 'vehicle']

    def __str__(self):
        return self.vehicle.name

    def get_absolute_url(self):
        return reverse('fuellog:entry_detail', kwargs={'pk': self.pk})

    



    
