from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from django.conf import settings
from datetime import datetime, date

import stripe  

class Client(TenantMixin):
    name = models.CharField(max_length=100)
    paid_until =  models.DateField()
    on_trial = models.BooleanField()
    created_on = models.DateField(auto_now_add=True)

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True

    def __str__(self):
        return self.name

    @property
    def subscription_expired(self):
        return date.today() < self.paid_until

class Domain(DomainMixin):
    pass

    def __str__(self):
        return self.domain

class BillingProfile(models.Model):
    tenant = models.OneToOneField("Client", related_name='billing' ,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    address_one = models.CharField(max_length=100)
    address_two = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=15)
    zip_code = models.IntegerField()
    stripe_id = models.CharField(max_length=255, blank=True)
    plan = models.CharField(max_length=50, blank=True)
    subscription_id = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name_plural = 'subscriptions'

    def __str__(self):
        return self.tenant.name + " - " + self.email
    
    def get_full_name(self):
        return self.first_name + ' ' + self.last_name