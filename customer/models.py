from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from django.conf import settings
from datetime import datetime, date

import stripe  
stripe.api_key = settings.STRIPE_SECRET_KEY

class Client(TenantMixin):
    name = models.CharField(max_length=100)
    paid_until =  models.DateField()
    on_trial = models.BooleanField()
    created_on = models.DateField(auto_now_add=True)

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True

    def __str__(self):
        return self.name



class Domain(DomainMixin):
    pass

    def __str__(self):
        return self.domain

class BillingProfile(models.Model):
    tenant = models.OneToOneField("Client", related_name='billing' ,on_delete=models.CASCADE)
    email = models.EmailField(max_length=254)
    stripe_id = models.CharField(max_length=255, blank=True)
    plan = models.CharField(max_length=50, blank=True)
    subscription_id = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name_plural = 'subscriptions'

    def __str__(self):
        return self.tenant.name + " - " + self.email
    
    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    @property
    def get_created_date(self):
        subscription = stripe.Subscription.retrieve(
            self.subscription_id)
        return date.fromtimestamp(subscription.created)

    @property
    def get_next_billing_date(self):
        subscription = stripe.Subscription.retrieve(
            self.subscription_id)
        return date.fromtimestamp(subscription.current_period_end)

    @property
    def subscription_expired(self):
        subscription = stripe.Subscription.retrieve(
            self.subscription_id)
        return date.today() > date.fromtimestamp(subscription.created)

    @property
    def get_card(self):
        customer = stripe.Customer.retrieve(
            self.stripe_id)
        card = customer.sources.retrieve(customer.default_source)
        return card

    @property
    def get_account_email(self):
        customer = stripe.Customer.retrieve(
            self.stripe_id)
        return customer.email