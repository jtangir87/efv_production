from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from django.conf import settings

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

class Domain(DomainMixin):
    pass

    def __str__(self):
        return self.domain

class BillingProfile(models.Model):
    tenant = models.OneToOneField("Client", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    address_one = models.CharField(max_length=100)
    address_two = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    zip_code = models.IntegerField()
    stripe_id = models.CharField(max_length=30, blank=True)

    class Meta:
        verbose_name_plural = 'subscriptions'

    def charge(self, request, email, fee):
        # Set your secret key: remember to change this to your live secret key
        # in production. See your keys here https://manage.stripe.com/account
        stripe.api_key = settings.STRIPE_SECRET_KEY

        # Get the credit card details submitted by the form
        token = request.POST['stripeToken']

        # Create a Customer
        stripe_customer = stripe.Customer.create(
            card=token,
            description=email
        )

        # Save the Stripe ID to the customer's profile
        self.stripe_id = stripe_customer.id
        self.save()

        # Charge the Customer instead of the card
        stripe.Charge.create(
            amount=fee, # in cents
            currency="usd",
            customer=stripe_customer.id
        )

        return stripe_customer
