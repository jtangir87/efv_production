from customer.models import Client, BillingProfile
from django.conf import settings
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.db import connection
from django.contrib.auth.models import User
from .forms import BillingProfileForm
from django.views.generic import DetailView, TemplateView, CreateView, UpdateView, FormView
from django.contrib import messages
from django_tenants.utils import tenant_context, parse_tenant_config_path, schema_context
from django.contrib.auth import authenticate, login
from django.forms.forms import NON_FIELD_ERRORS
from django.conf import settings
from django.urls import reverse
import datetime
import stripe


# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY


class TenantDetail(TemplateView):
    model = Client
    template_name = 'customer/customer_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["stripe_key"] = settings.STRIPE_PUBLISHABLE_KEY
        return context
    


def billing_new(request):
    if request.method == 'POST':
        customer = stripe.Customer.create(
            email = request.POST['stripeEmail'],
            source = request.POST['stripeToken'],
        )

        subscription = stripe.Subscription.create(
            customer = customer.id,
            plan = 'plan_FbzG7WVV6fWTLm',
        )

        tenant = request.tenant

        BillingProfile.objects.create(tenant=tenant, email=customer.email, stripe_id=customer.id, subscription_id=subscription.id, plan='plan_FbzG7WVV6fWTLm')
        return render(request, 'customer/billingprofile_form.html')



def card_update(request):
   if request.method == 'POST':
       customer = request.tenant.billing.stripe_id
       token = request.POST['stripeToken']
       charge = stripe.Customer.modify(
           customer, 
           source = token,
       )

       return render(request, 'customer/subscription_success.html')

def cancel_subscription(request):
    errors = []

    try:
        sub = request.tenant.billing.subscription_id


        stripe.Subscription.modify(sub, cancel_at_period_end=True)
    

    except stripe.error.CardError as e:
        messages.error(request, e)

    return render(request, 'customer/cancel_subscription_success.html')

class SubscriptionSuccess(TemplateView):
    template_name = 'customer/subscription_success.html'

class SubscriptionCancelConfirm(TemplateView):
    template_name = 'customer/cancel_subscription_confirm.html'
    

class SubscriptionCancelSuccess(TemplateView):
    template_name = 'customer/cancel_subscription_complete.html'

