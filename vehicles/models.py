from django.db import models
from django.urls import reverse
import datetime
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class Vehicle(models.Model):
    name = models.CharField(blank=True, max_length=100)
    make = models.CharField(blank=True, max_length=100)
    model = models.CharField(blank=True, max_length=100)
    year = models.IntegerField(blank=True, null=True)
    vin = models.CharField(blank=True, max_length=17, verbose_name="VIN")
    gvw = models.IntegerField(blank=True, null=True, verbose_name="GVW")
    license_plate = models.CharField(blank=True, max_length=100)
    purchase_date = models.DateField()
    current_mileage = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('vehicles:vehicle_detail', kwargs={'pk': self.pk})

    
    def get_current_mileage(self):
        return int(self.current_mileage)

    


class DamageReport(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.datetime.today)
    driver = models.CharField(blank=True, max_length=100)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.vehicle.name + self.driver

    def get_absolute_url(self):
        return reverse('vehicles:damage_detail', kwargs={'pk': self.pk})


class DamageImages(models.Model):
    report = models.ForeignKey(DamageReport, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="photos/%Y/%m/%d", blank=True, null=True)

    def __str__(self):
        return self.report.vehicle.name
