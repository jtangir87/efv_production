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
from datetime import datetime
from django.http import HttpResponse

class Dashboard(ListView):
    model = FuelEntry
    template_name = 'dashboard.html'


    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
        context['recent_fuel'] = FuelEntry.objects.order_by('vehicle_id', '-date').distinct('vehicle_id')
        context['upcoming_service'] = ServiceRecord.objects.filter(completed=False).order_by('vehicle')[:5]
        context['recent_service'] = ServiceRecord.objects.filter(completed=True).order_by('-date')[:5]
        context ['recent_damage'] = DamageReport.objects.order_by('-date')[:5]
        context ['vehicle_count'] = Vehicle.objects.all().count()
        #Calculate ytd fuel total
        today = datetime.now()
        ytd_fuel_total = FuelEntry.objects.filter(date__year=today.year).aggregate(Sum('cost'))
        context['ytd_fuel_total'] = ytd_fuel_total['cost__sum']
        #Calculate ytd service total
        today = datetime.now()
        ytd_serv_total = ServiceRecord.objects.filter(date__year=today.year).aggregate(Sum('cost'))
        context['ytd_serv_total'] = ytd_serv_total['cost__sum']
        #Calculate lifetime service total
        lifetime_serv_total = ServiceRecord.objects.all().aggregate(Sum('cost'))
        context['lifetime_serv_total'] = lifetime_serv_total['cost__sum']

        return context


class Public(TemplateView):
    template_name = 'index.html'
    




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
                "Your website" +'',
                ['youremail@gmail.com'],
                headers = {'Reply-To': email }
            )
            email.send()
            return redirect('/')

    return render(request, 'index.html', {
        'form': form_class,
    })

