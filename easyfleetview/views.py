from django.shortcuts import render
from django.views.generic import TemplateView, ListView, TemplateView, CreateView
from fuellog.models import FuelEntry
from vehicles.models import Vehicle, DamageReport
from service.models import ServiceRecord
from django_tenants.utils import remove_www

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
    




