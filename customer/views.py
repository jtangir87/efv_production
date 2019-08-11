from customer.models import Client, BillingProfile
from django.conf import settings
from django.shortcuts import render
from django.db import connection
from .forms import BillingProfileForm
from django.views.generic import DetailView, TemplateView, CreateView
from django_tenants.utils import tenant_context, parse_tenant_config_path, schema_context
from django.contrib.auth import authenticate, login
from django.forms.forms import NON_FIELD_ERRORS
from django.conf import settings
from django.urls import reverse

import stripe
# Create your views here.

class TenantDetail(TemplateView):
    model = Client
    template_name = 'customer/customer_detail.html'
    

def billing_new(request, template='customer/billingprofile_form.html'):
    if request.method == 'POST':
        form = BillingProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.tenant = request.tenant

            # Create the User record
            # Create BillingProfile Record
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            address_one = form.cleaned_data['address_one']
            address_two = form.cleaned_data['address_two']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zip_code = form.cleaned_data['zip_code']
            prof = BillingProfile(first_name=first_name, last_name=last_name, email=email,
                 address_one=address_one, address_two=address_two,
                    city=city, state=state, zip_code=zip_code, tenant=profile.tenant)
            prof.save()
            # Process payment (via Stripe)
            # fee = settings.SUBSCRIPTION_PRICE
            # try:
            #     stripe_customer = prof.charge(request, email, fee)
            # except stripe.StripeError as e:
            #     form._errors[NON_FIELD_ERRORS] = form.error_class([e.args[0]])
            #     return render(request, template,
            #         {'form':form,
            #         'STRIPE_PUBLISHABLE_KEY':settings.STRIPE_PUBLISHABLE_KEY}
            #     )
            # Auto login the user
            return HttpResponseRedirect('/')

    else:
        form = BillingProfileForm()

    return render(request, template,
        {'form':form,
         'stripe_key':settings.STRIPE_PUBLISHABLE_KEY})