from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.py

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.user.first_name + self.user.last_name

    