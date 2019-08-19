from customer.models import Client, BillingProfile
from django.conf import settings
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.db import connection
from django.contrib.auth.models import User
from .forms import BillingProfileForm, BillingProfileFormTest
from django.views.generic import DetailView, TemplateView, CreateView, UpdateView
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


def billing_new(request):
    if request.method == 'POST':
        form = BillingProfileForm(request.POST)
        if form.is_valid():
            try:
                profile = form.save(commit=False)
                profile.tenant = request.tenant
                cus = form.save()

                customer = stripe.Customer.create(
                    email = cus.email,
                    card = cus.stripe_id,
                )

                subscription = stripe.Subscription.create(
                    customer = customer.id,
                    plan = 'plan_FbzG7WVV6fWTLm',
                )

                cus.stripe_id = customer.id
                cus.subscription_id = subscription.id
                cus.plan = 'plan_FbzG7WVV6fWTLm'
                cus.save()


                return redirect('client:subscription_success')

            except stripe.error.CardError as e:
                form.add_error("The card has been declined")
    else:
        form = BillingProfileForm()

    args = {}
    args.update(csrf(request))
    args['form'] = form
    args['publishable'] = settings.STRIPE_PUBLISHABLE_KEY
    args['months'] = range(1,13)
    args['years'] = range(2019, 2039)
    args['soon'] = datetime.date.today() + datetime.timedelta(days=30)

    return render(request, 'customer/billingprofile_form.html', args)


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