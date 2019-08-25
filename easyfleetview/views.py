import operator
from django.shortcuts import render,redirect
from django.views.generic import TemplateView, ListView, TemplateView, CreateView
from fuellog.models import FuelEntry
from vehicles.models import Vehicle, DamageReport
from service.models import ServiceRecord
from .forms import TrialSignUpForm
from django_tenants.utils import remove_www
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.db.models import Sum
from django.db.models.functions import Extract
from datetime import datetime, date, timedelta
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from customer.models import BillingProfile
from django.conf import settings
import json
import stripe

class Dashboard(ListView):
    model = FuelEntry
    template_name = 'dashboard.html'


    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
        today = datetime.now()
        last_fuel = FuelEntry.objects.order_by('vehicle_id', '-date').distinct('vehicle_id')
        context['recent_fuel'] = FuelEntry.objects.filter(id__in=last_fuel).order_by('vehicle')
        context['upcoming_service'] = ServiceRecord.objects.filter(completed=False).order_by('vehicle')
        context['recent_service'] = ServiceRecord.objects.filter(completed=True).order_by('-date')[:5]
        context ['recent_damage'] = DamageReport.objects.order_by('-date')[:5]
        context ['vehicle_count'] = Vehicle.objects.all().count()
        #Calculate ytd fuel total
        ytd_fuel_total = FuelEntry.objects.filter(date__year=today.year).aggregate(Sum('cost'))
        context['ytd_fuel_total'] = ytd_fuel_total['cost__sum']
        #Calculate ytd service total
        ytd_serv_total = ServiceRecord.objects.filter(date__year=today.year).aggregate(Sum('cost'))
        context['ytd_serv_total'] = ytd_serv_total['cost__sum']
        #Calculate lifetime service total
        lifetime_serv_total = ServiceRecord.objects.all().aggregate(Sum('cost'))
        context['lifetime_serv_total'] = lifetime_serv_total['cost__sum']
        context["stripe_key"] = settings.STRIPE_PUBLISHABLE_KEY

        return context


class SignUpComplete(TemplateView):
    template_name = 'signup_complete.html'
    




def trialsignup(request):
    form_class = TrialSignUpForm

    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            first_name = request.POST.get(
                'first_name'
            , '')
            last_name = request.POST.get(
                'last_name'
            , '')    
            company_name = request.POST.get(
                'company_name'
            , '')                   
            email = request.POST.get(
                'email'
            , '')
            phone_number = request.POST.get(
                'phone_number'
            , '')            
            form_content = request.POST.get('content', '')

            # Email the profile with the
            # contact information
            template = get_template('trial_template.txt')
            context = {
                'first_name': first_name,
                'last_name': last_name,
                'company_name': company_name,
                'email': email,
                'phone_number': phone_number,
            }
            content = template.render(context)

            email = EmailMessage(
                "New tial sign up",
                content,
                "Easy Fleet View" +'',
                ['support@easyfleetview.com'],
                headers = {'Reply-To': email }
            )
            email.send()
            return redirect('signup_complete')

    return render(request, 'public_index.html', {
        'form': form_class,
    })


# STRIPE WEBHOOOKS

@csrf_exempt
def stripe_webhooks(request):
  payload = request.body
  event = None

  try:
    event = stripe.Event.construct_from(
      json.loads(payload), stripe.api_key
    )
  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)

  # Handle the event
  if event.type == 'payment_method.attached':
    payment_method = event.data.object # contains a stripe.PaymentMethod
    customer = payment_method.customer
    BillingProfile.objects.filter(stripe_id=customer).update(
        name_on_card = payment_method.billing_details.name,
        street_one = payment_method.billing_details.address.line1,
        street_two = payment_method.billing_details.address.line2,
        city = payment_method.billing_details.address.city,
        state = payment_method.billing_details.address.state,
        zip = payment_method.billing_details.address.postal_code,
        brand = payment_method.card.brand,
        last_4 = payment_method.card.last4,
    )  
  elif event.type == 'customer.subscription.created':
    sub = event.data.object # contains a stripe.Invoice
    customer = sub.customer
    next_payment = date.fromtimestamp(sub.current_period_end)
    BillingProfile.objects.filter(stripe_id=customer).update(paid_until=next_payment)

  elif event.type == 'customer.subscription.updated':
    sub = event.data.object # contains a stripe.Invoice
    customer = sub.customer
    next_payment = date.fromtimestamp(sub.current_period_end)
    BillingProfile.objects.filter(stripe_id=customer).update(paid_until=next_payment, canceled=sub.cancel_at_period_end)

  elif event.type == 'customer.updated':
    update = event.data.object
    customer = update.id
    prof = BillingProfile.objects.get(stripe_id=customer)
    sub_id = prof.subscription_id
    stripe_subscription = stripe.Subscription.retrieve(sub_id)
    next_payment = date.fromtimestamp(stripe_subscription.current_period_end)
    BillingProfile.objects.filter(stripe_id=customer).update(email=update.email, paid_until=next_payment)

  
  else:
    # Unexpected event type
    return HttpResponse(status=400)

  return HttpResponse(status=200)